import os
import sys
from datetime import date
from dotenv import load_dotenv
from anthropic import Anthropic
from tavily import TavilyClient

load_dotenv()
claude = Anthropic()
buscador = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODELO = "claude-haiku-4-5"
MAX_PASOS = 10   # Freno de seguridad: el agente nunca da más de 10 vueltas

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
        "description": "Guarda el informe final en un archivo Markdown (.md).",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre_archivo": {"type": "string", "description": "Nombre corto, por ejemplo: aws-lambda-2026.md"},
                "contenido": {"type": "string", "description": "El informe completo en formato Markdown"},
            },
            "required": ["nombre_archivo", "contenido"],
        },
    },
]

# ---------- 2. LA COCINA: lo que hace cada herramienta de verdad ----------
def buscar_web(consulta):
    resultados = buscador.search(consulta, max_results=3)
    texto = ""
    for r in resultados["results"]:
        texto += f"- {r['title']} ({r['url']}): {r['content'][:500]}\n"
    return texto

def guardar_informe(nombre_archivo, contenido):
    os.makedirs("informes", exist_ok=True)       # Crea la carpeta "informes" si no existe
    nombre = os.path.basename(nombre_archivo)     # Seguridad: solo el nombre, sin rutas raras
    if not nombre.endswith(".md"):
        nombre += ".md"
    ruta = os.path.join("informes", nombre)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return f"Informe guardado en {ruta}"

# El "mesero": según lo que pida Claude, ejecuta la receta correcta
def ejecutar_herramienta(nombre, datos):
    if nombre == "buscar_web":
        print(f"   🔎 Buscando: {datos['consulta']}")
        return buscar_web(datos["consulta"])
    if nombre == "guardar_informe":
        print(f"   💾 Guardando: {datos['nombre_archivo']}")
        return guardar_informe(datos["nombre_archivo"], datos["contenido"])
    return f"No conozco la herramienta {nombre}"

# ---------- 3. EL LOOP: el corazón del agente ----------
def investigar(tema):
    instrucciones = f"""Eres un agente de investigación. Hoy es {date.today()}.
Investiga el tema que te den usando buscar_web (puedes buscar varias veces, máximo 5).
Cuando tengas suficiente información, usa guardar_informe para guardar un informe en Markdown con:
título, resumen, hallazgos principales y fuentes (con sus links).
No le hagas preguntas al usuario: trabaja solo y termina guardando el informe."""

    mensajes = [{"role": "user", "content": f"Investiga este tema: {tema}"}]
    tokens_entrada = 0
    tokens_salida = 0

    print(f"🤖 Investigando: {tema}\n")

    for paso in range(1, MAX_PASOS + 1):
        respuesta = claude.messages.create(
            model=MODELO, max_tokens=4000,
            system=instrucciones, tools=herramientas, messages=mensajes,
        )
        tokens_entrada += respuesta.usage.input_tokens
        tokens_salida += respuesta.usage.output_tokens
        mensajes.append({"role": "assistant", "content": respuesta.content})

        # Si Claude ya no pide herramientas, terminó
        if respuesta.stop_reason != "tool_use":
            break

        # Ejecutar cada herramienta que pidió y devolverle los resultados
        print(f"🔁 Vuelta {paso}")
        resultados = []
        for bloque in respuesta.content:
            if bloque.type == "tool_use":
                resultado = ejecutar_herramienta(bloque.name, bloque.input)
                resultados.append({"type": "tool_result", "tool_use_id": bloque.id, "content": resultado})
        mensajes.append({"role": "user", "content": resultados})

    # ---------- 4. RESUMEN: cuánto trabajó y cuánto costó ----------
    costo = tokens_entrada * 1 / 1_000_000 + tokens_salida * 5 / 1_000_000
    print("\n✅ Listo")
    print(f"   Vueltas: {paso}")
    print(f"   Tokens: {tokens_entrada} de entrada, {tokens_salida} de salida")
    print(f"   Costo aproximado: ${costo:.4f} USD")

# ---------- 5. ARRANCAR desde la terminal ----------
if __name__ == "__main__":
    tema = " ".join(sys.argv[1:]) or "novedades de AWS Lambda"
    investigar(tema)