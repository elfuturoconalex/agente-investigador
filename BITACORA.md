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

## Día 2: Claude Code, API y Git

### Qué hice
- Creé mi cuenta en la **Claude Console**, cargué USD 5 de crédito y dejé
  **apagada la recarga automática** (para no gastar de más).
- Instalé **Claude Code** con el instalador oficial (`curl`) e inicié sesión
  con mi **plan Pro** (no con la Console, para no gastar los créditos de la API).
- Cambié el modelo a **Sonnet** (`/model`) y el modo a **manual** (Shift + Tab).
- Con Claude Code convertí la carpeta en **repositorio de Git** e hice mi
  **primer commit**: "Configuración inicial del proyecto".

### Qué aprendí
- **API vs plan Pro:** la API es el "cerebro" de mi agente y se paga por uso
  (prepago). El plan Pro es para el asistente que me ayuda a programar.
- **Tokens:** pedacitos de palabras. Me cobran por lo que mando y lo que recibo.
- **Terminal = teléfono:** una terminal nueva le habla a la Mac. Si escribo
  `claude` o `copilot`, "llamo" a ese asistente.
- **Manual mode:** Claude Code me pide permiso antes de cada acción. Así veo y aprendo.
- **Commit:** un punto de guardado con un código único (el mío: `ec0226c`).

### Problemas y cómo los resolví
- **Me confundía si estaba en Claude, Copilot o la terminal normal.**
  → Una terminal nueva es "ninguno"; reviso las señales (logo, modelo, modo).
- **Con `cd ..` me salí del proyecto sin darme cuenta.**
  → Antes de abrir un asistente reviso que la línea diga `agente-investigador %`.

## Día 2 (continuación): GitHub, llaves y .env

### Qué hice
- Agregué mi proyecto a **GitHub Desktop** ("Add Existing Repository"), hice el
  commit `Bitácora: Día 2` y lo **publiqué en GitHub** como repositorio privado.
- Creé mi **API key de Anthropic** y la guardé en la app **Contraseñas** de mi Mac.
- Creé mi cuenta en **Tavily** con el plan **Free** (1,000 búsquedas/mes, sin tarjeta)
  y guardé su API key también en Contraseñas.
- Creé el archivo **`.env`** con mis dos llaves y confirmé con `git status`
  que Git lo ignora ("working tree clean").

### Qué aprendí
- **History en GitHub Desktop:** es mi "máquina del tiempo"; ahí veo cada commit,
  quién lo hizo y qué cambió (verde = agregado, rojo = quitado).
- **`.gitignore`:** una "lista negra" para Git. Por eso `.venv` y `.env`
  nunca se suben. En VS Code esos archivos aparecen en gris.
- **`requirements.txt`:** la "lista del súper" de mi proyecto; con ella
  cualquiera (o AWS) recrea mi `.venv`.
- **"M" en VS Code:** archivo modificado desde el último commit.
- **Ciclo de trabajo:** editar → commit → push.

### Problemas y cómo los resolví
- **Expuse mi API key en una captura de pantalla.**
  → La eliminé en la Console y creé una nueva. Ahora guardo mis llaves en la app
  Contraseñas y no tomo capturas con llaves visibles.
- **La app Contraseñas puso una contraseña inventada automáticamente.**
  → La reemplacé por mi llave real y verifiqué que empezara con `sk-ant-`.
- **Al elegir el plan de Tavily, me llevó a una pantalla de pago (Stripe).**
  → No metí ningún dato, regresé y elegí "Continue on Free".
- **Escribí `git status` dentro de Claude Code en vez de la terminal normal.**
  → Funcionó igual (Claude lo ejecutó por mí), pero aprendí a distinguir ambas.

### Pendiente para mañana
- Crear y correr `hola_claude.py`: mi primera llamada a Claude desde código.

## Día 3: Mi primera llamada a Claude

### Qué hice
- Creé `hola_claude.py` y lo ejecuté con `python hola_claude.py`.
- Claude me respondió desde mi propio código: 27 tokens de entrada,
  116 de salida (≈ $0.0006 USD con Haiku).

### Qué aprendí
- **Editor vs terminal:** arriba se escribe el código; abajo se ejecuta.
- **Hay que guardar (Cmd + S) antes de ejecutar**, o Python lee la versión vieja.
- **Archivo vs carpeta:** las carpetas tienen flechita (> o ⌄); los archivos no.
- **"U" en VS Code:** archivo nuevo que Git todavía no conoce.
- **Markdown en la terminal:** `#` y `**` se ven tal cual; en un `.md` se ven con formato.

### Problemas y cómo los resolví
- **VS Code me sugirió instalar PowerShell.** → No hace falta en Mac; lo cerré.