# Bitácora de aprendizaje

## Día 1: Preparar mi Mac (Fase 0)

### Qué hice
- Instalé **Homebrew**, un instalador de programas desde la terminal.
- Agregué Homebrew al **PATH**.
- Instalé **Python 3.12** con Homebrew.
- Creé la carpeta del proyecto con un **entorno virtual (.venv)** y 3 librerías:
  - `anthropic`: para hablar con Claude.
  - `tavily-python`: para buscar en internet.
  - `python-dotenv`: para leer mis API keys de forma segura.
- Creé `requirements.txt`, `.gitignore` y `README.md`.

### Qué aprendí
- **PATH:** la lista de "cajones" donde la Mac busca los programas. Si un programa
  está en un cajón que no está en la lista, la Mac dice que no existe.
- **Homebrew vs brew:** Homebrew es el nombre del programa; `brew` es el comando que escribo.
- **Entorno virtual:** una "caja de herramientas" propia de cada proyecto, para que
  las librerías no se mezclen.
- **.gitignore:** la lista de archivos que nunca se suben a GitHub (como mis llaves secretas).
- **Git:** repositorio = carpeta con memoria; commit = punto de guardado; push = subirlo a la nube.
- En VS Code, el **●** en una pestaña significa "sin guardar" → Cmd + S.

### Problemas y cómo los resolví
- **Copilot no pudo instalar Homebrew** porque pide la contraseña de administrador.
  → Lo instalé yo mismo desde la Terminal.
- **El comando `brew` no funcionaba** después de instalarlo.
  → Faltaba agregarlo al PATH en `~/.zprofile`.
- **Mi Mac tenía Python 3.9.6**, que es viejo y AWS Lambda ya no lo soporta.
  → Instalé Python 3.12 sin borrar el del sistema.
- **No veía `.venv` ni `.gitignore` en Finder.**
  → macOS esconde los archivos que empiezan con punto. En VS Code sí aparecen.