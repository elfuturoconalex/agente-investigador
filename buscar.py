import os
from dotenv import load_dotenv
from tavily import TavilyClient

# 1. Abrir la caja fuerte y cargar las llaves
load_dotenv()

# 2. Crear el "buscador" con tu llave de Tavily
buscador = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 3. Buscar algo en internet (máximo 3 resultados)
resultados = buscador.search("qué es AWS Lambda", max_results=3)

# 4. Mostrar cada resultado: título, link y un pedacito del texto
for r in resultados["results"]:
    print("📄", r["title"])
    print("🔗", r["url"])
    print(r["content"][:200], "...")
    print("---")