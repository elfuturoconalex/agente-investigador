import os
from dotenv import load_dotenv
from anthropic import Anthropic
from tavily import TavilyClient

load_dotenv()
claude = Anthropic()
buscador = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 1. El "menú": le describimos a Claude la herramienta que puede pedir
herramientas = [{
    "name": "buscar_web",
    "description": "Busca información actual en internet sobre un tema.",
    "input_schema": {
        "type": "object",
        "properties": {
            "consulta": {"type": "string", "description": "Lo que hay que buscar"}
        },
        "required": ["consulta"],
    },
}]

# 2. La función real que hace la búsqueda cuando Claude la pide
def buscar_web(consulta):
    resultados = buscador.search(consulta, max_results=3)
    texto = ""
    for r in resultados["results"]:
        texto += f"- {r['title']} ({r['url']}): {r['content'][:500]}\n"
    return texto

# 3. La pregunta
mensajes = [{"role": "user", "content": "¿Cuáles son las novedades más recientes de AWS Lambda?"}]

# 4. Primera llamada: Claude decide si necesita buscar
respuesta = claude.messages.create(
    model="claude-haiku-4-5", max_tokens=1000,
    tools=herramientas, messages=mensajes,
)

# 5. Si Claude pidió usar la herramienta, la ejecutamos y le devolvemos el resultado
if respuesta.stop_reason == "tool_use":
    pedido = next(b for b in respuesta.content if b.type == "tool_use")
    print("🔧 Claude quiere usar:", pedido.name, "→", pedido.input)

    resultado = buscar_web(pedido.input["consulta"])

    mensajes.append({"role": "assistant", "content": respuesta.content})
    mensajes.append({"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": pedido.id, "content": resultado}
    ]})

    # 6. Segunda llamada: Claude escribe la respuesta con lo que encontró
    respuesta = claude.messages.create(
        model="claude-haiku-4-5", max_tokens=1000,
        tools=herramientas, messages=mensajes,
    )

# 7. Mostrar la respuesta final
print("".join(b.text for b in respuesta.content if b.type == "text"))