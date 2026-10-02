# Agente Investigador 🔎

Agente de IA que recibe un tema, busca en la web, resume la información y guarda un informe estructurado.

## Fases del proyecto

- [x] **Fase 1:** Agente funcionando en local
- [ ] **Fase 2:** Desplegado en AWS (Lambda + API Gateway + S3)
- [ ] **Fase 3:** Observabilidad (trazas, herramientas usadas y tokens consumidos)

## Requisitos

- macOS
- [Homebrew](https://brew.sh)
- Python 3.12
- API key de [Anthropic](https://console.anthropic.com)
- API key de [Tavily](https://tavily.com)

## Instalación

1. Instalar Homebrew:
```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Agregar `brew` al PATH:
```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
```
3. Instalar Python 3.12:
```bash
   brew install python@3.12
```
4. Crear el entorno virtual e instalar dependencias:
```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```