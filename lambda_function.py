import os
import re
import json
import time
import base64
import unicodedata
from datetime import date, datetime, timezone

import boto3
from anthropic import Anthropic
from tavily import TavilyClient

# ---------- 0. CONFIGURACIÓN ----------
BUCKET = os.environ["BUCKET_NAME"]   # El nombre del bucket se configura en Lambda
MODELO = "claude-haiku-4-5"
MAX_PASOS = 10                       # Freno de seguridad

ssm = boto3.client("ssm")            # Para leer Parameter Store
s3 = boto3.client("s3")              # Para guardar en S3
lambda_client = boto3.client("lambda")  # Para llamarse a sí misma en segundo plano

def leer_llave(nombre):
    """Abre la caja fuerte (Parameter Store) y saca una llave descifrada."""
    respuesta = ssm.get_parameter(Name=nombre, WithDecryption=True)
    return respuesta["Parameter"]["Value"]

claude = Anthropic(api_key=leer_llave("/agente-investigador/anthropic-api-key"))
buscador = TavilyClient(api_key=leer_llave("/agente-investigador/tavily-api-key"))

# ---------- 1. EL MENÚ: las herramientas que Claude puede pedir ----------
herramientas = [
    {
        "name": "buscar_web",
        "description": "Busca información actual en internet sobre un tema.",
        "input_schema": {
            "type": "object",
            "properties": {
                "consulta": {"type": "string", "description": "Lo que hay que buscar"}
            },
            "required": ["consulta"],
        },
    },
    {
        "name": "guardar_informe",
        "description": "Guarda el informe final en Markdown.",
        "input_schema": {
            "type": "object",
            "properties": {
                "contenido": {"type": "string", "description": "El informe completo en formato Markdown"}
            },
            "required": ["contenido"],
        },
    },
]

# ---------- 2. LA COCINA: lo que hace cada herramienta ----------
def buscar_web(consulta):
    resultados = buscador.search(consulta, max_results=3)
    texto = ""
    for r in resultados["results"]:
        texto += f"- {r['title']} ({r['url']}): {r['content'][:500]}\n"
    return texto

def guardar_informe(clave, contenido):
    s3.put_object(
        Bucket=BUCKET,
        Key=clave,
        Body=contenido.encode("utf-8"),
        ContentType="text/markdown; charset=utf-8",
    )
    return f"Informe guardado en s3://{BUCKET}/{clave}"

def ejecutar_herramienta(nombre, datos, clave):
    if nombre == "buscar_web":
        print(f"🔎 Buscando: {datos['consulta']}")
        return buscar_web(datos["consulta"])
    if nombre == "guardar_informe":
        print(f"💾 Guardando: {clave}")
        return guardar_informe(clave, datos["contenido"])
    return f"No conozco la herramienta {nombre}"

# ---------- 3. LA TRAZA: la "bitácora de vuelo" de cada investigación (Fase 3) ----------
def calcular_costo(tokens_entrada, tokens_salida):
    """Precio de Haiku 4.5: $1 por millón de tokens de entrada y $5 por millón de salida."""
    return tokens_entrada * 1 / 1_000_000 + tokens_salida * 5 / 1_000_000

def guardar_traza(clave, traza):
    """Guarda la traza en S3, al lado del informe, con el mismo nombre pero .json."""
    s3.put_object(
        Bucket=BUCKET,
        Key=clave.replace(".md", ".json"),
        Body=json.dumps(traza, ensure_ascii=False, indent=2).encode("utf-8"),
        ContentType="application/json; charset=utf-8",
    )

# ---------- 4. EL LOOP: el corazón del agente, ahora anotando todo ----------
def investigar(tema, clave):
    instrucciones = f"""Eres un agente de investigación. Hoy es {date.today()}.
Investiga el tema que te den usando buscar_web (puedes buscar varias veces, máximo 5).
Cuando tengas suficiente información, usa guardar_informe para guardar un informe en Markdown con:
título, resumen, hallazgos principales y fuentes (con sus links).
No le hagas preguntas al usuario: trabaja solo y termina guardando el informe."""

    mensajes = [{"role": "user", "content": f"Investiga este tema: {tema}"}]

    # 📒 La traza empieza vacía y se va llenando en cada vuelta
    traza = {
        "tema": tema,
        "informe": clave,
        "modelo": MODELO,
        "inicio": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "estado": "en curso",
        "vueltas": [],
    }
    reloj_total = time.time()
    print(f"🤖 Investigando: {tema}")

    try:
        for paso in range(1, MAX_PASOS + 1):
            reloj_claude = time.time()
            respuesta = claude.messages.create(
                model=MODELO, max_tokens=4000,
                system=instrucciones, tools=herramientas, messages=mensajes,
            )
            # 📝 Anotamos lo que pasó en esta vuelta
            vuelta = {
                "numero": paso,
                "segundos_claude": round(time.time() - reloj_claude, 1),
                "tokens_entrada": respuesta.usage.input_tokens,
                "tokens_salida": respuesta.usage.output_tokens,
                "costo_usd": round(calcular_costo(respuesta.usage.input_tokens, respuesta.usage.output_tokens), 5),
                "herramientas": [],
            }
            traza["vueltas"].append(vuelta)
            mensajes.append({"role": "assistant", "content": respuesta.content})

            if respuesta.stop_reason != "tool_use":
                break

            print(f"🔁 Vuelta {paso}")
            resultados = []
            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    reloj_herramienta = time.time()
                    resultado = ejecutar_herramienta(bloque.name, bloque.input, clave)
                    # 📝 Anotamos qué herramienta usó, qué buscó y cuánto tardó
                    vuelta["herramientas"].append({
                        "nombre": bloque.name,
                        "consulta": bloque.input.get("consulta", ""),
                        "segundos": round(time.time() - reloj_herramienta, 1),
                    })
                    resultados.append({"type": "tool_result", "tool_use_id": bloque.id, "content": resultado})

            # 💡 Mejora Fase 3: si ya guardó el informe, terminamos aquí.
            # Así nos ahorramos una vuelta extra solo para que Claude diga "listo".
            if any(h["nombre"] == "guardar_informe" for h in vuelta["herramientas"]):
                break

            mensajes.append({"role": "user", "content": resultados})

        traza["estado"] = "ok"

    except Exception as error:
        # Si algo falla, lo anotamos en la traza en lugar de perderlo
        traza["estado"] = "error"
        traza["error"] = str(error)
        print(f"❌ Error: {error}")

    finally:
        # 🧮 Totales: se calculan siempre, aunque haya habido error
        entrada = sum(v["tokens_entrada"] for v in traza["vueltas"])
        salida = sum(v["tokens_salida"] for v in traza["vueltas"])
        traza["totales"] = {
            "vueltas": len(traza["vueltas"]),
            "busquedas": sum(1 for v in traza["vueltas"] for h in v["herramientas"] if h["nombre"] == "buscar_web"),
            "tokens_entrada": entrada,
            "tokens_salida": salida,
            "costo_usd": round(calcular_costo(entrada, salida), 4),
            "segundos": round(time.time() - reloj_total, 1),
        }
        guardar_traza(clave, traza)
        t = traza["totales"]
        print(f"✅ {traza['estado']} | Vueltas: {t['vueltas']} | Búsquedas: {t['busquedas']} | "
              f"Tokens: {t['tokens_entrada']} entrada, {t['tokens_salida']} salida | "
              f"Costo: ${t['costo_usd']} USD | {t['segundos']} s")
        # Un renglón en JSON para CloudWatch: así después podemos sumar y sacar promedios
        print("TRAZA " + json.dumps({"tema": tema, "estado": traza["estado"], **t}, ensure_ascii=False))

# ---------- 5. UTILIDADES ----------
def nombre_seguro(texto):
    """Convierte 'IA en Medicina' en 'ia-en-medicina' para usarlo como nombre de archivo."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")[:50] or "informe"

def respuesta_http(codigo, datos):
    return {
        "statusCode": codigo,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(datos, ensure_ascii=False),
    }

# ---------- 6. LA PUERTA DE ENTRADA: lo que Lambda ejecuta ----------
def lambda_handler(event, context):
    # Caso A: llega una petición desde la API → responder rápido y trabajar en segundo plano
    if "body" in event:
        cuerpo = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            cuerpo = base64.b64decode(cuerpo).decode("utf-8")
        try:
            tema = json.loads(cuerpo).get("tema", "").strip()
        except json.JSONDecodeError:
            tema = ""
        if not tema:
            return respuesta_http(400, {"error": 'Falta el tema. Ejemplo: {"tema": "IA en medicina"}'})

        ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        clave = f"informes/{ahora}_{nombre_seguro(tema)}.md"

        # La Lambda se llama a sí misma "sin esperar" (InvocationType="Event")
        lambda_client.invoke(
            FunctionName=context.function_name,
            InvocationType="Event",
            Payload=json.dumps({"tema": tema, "clave": clave}),
        )
        return respuesta_http(202, {
            "mensaje": "Investigación iniciada. El informe estará listo en 1 o 2 minutos.",
            "tema": tema,
            "informe": f"s3://{BUCKET}/{clave}",
        })

    # Caso B: la llamada en segundo plano → aquí sí se investiga
    investigar(event["tema"], event["clave"])
    return {"ok": True}