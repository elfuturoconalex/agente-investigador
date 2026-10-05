import os
import re
import json
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

# ---------- 3. EL LOOP: el corazón del agente (igual que en tu Mac) ----------
def investigar(tema, clave):
    instrucciones = f"""Eres un agente de investigación. Hoy es {date.today()}.
Investiga el tema que te den usando buscar_web (puedes buscar varias veces, máximo 5).
Cuando tengas suficiente información, usa guardar_informe para guardar un informe en Markdown con:
título, resumen, hallazgos principales y fuentes (con sus links).
No le hagas preguntas al usuario: trabaja solo y termina guardando el informe."""

    mensajes = [{"role": "user", "content": f"Investiga este tema: {tema}"}]
    tokens_entrada = 0
    tokens_salida = 0

    print(f"🤖 Investigando: {tema}")

    for paso in range(1, MAX_PASOS + 1):
        respuesta = claude.messages.create(
            model=MODELO, max_tokens=4000,
            system=instrucciones, tools=herramientas, messages=mensajes,
        )
        tokens_entrada += respuesta.usage.input_tokens
        tokens_salida += respuesta.usage.output_tokens
        mensajes.append({"role": "assistant", "content": respuesta.content})

        if respuesta.stop_reason != "tool_use":
            break

        print(f"🔁 Vuelta {paso}")
        resultados = []
        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                resultado = ejecutar_herramienta(bloque.name, bloque.input, clave)
                resultados.append({"type": "tool_result", "tool_use_id": bloque.id, "content": resultado})
        mensajes.append({"role": "user", "content": resultados})

    costo = tokens_entrada * 1 / 1_000_000 + tokens_salida * 5 / 1_000_000
    print(f"✅ Listo | Vueltas: {paso} | Tokens: {tokens_entrada} entrada, {tokens_salida} salida | Costo: ${costo:.4f} USD")

# ---------- 4. UTILIDADES ----------
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

# ---------- 5. LA PUERTA DE ENTRADA: lo que Lambda ejecuta ----------
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