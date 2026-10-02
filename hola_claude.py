from dotenv import load_dotenv
from anthropic import Anthropic

# 1. Abrir la caja fuerte (.env) y cargar las llaves
load_dotenv()

# 2. Crear el "teléfono" para hablar con Claude
cliente = Anthropic()

# 3. Hacer la pregunta
respuesta = cliente.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "Explícame en 3 líneas qué es un agente de IA."}
    ],
)

# 4. Mostrar la respuesta
print(respuesta.content[0].text)

# 5. Mostrar cuántos tokens gastó
print("---")
print("Tokens de entrada:", respuesta.usage.input_tokens)
print("Tokens de salida:", respuesta.usage.output_tokens)