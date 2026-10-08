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

## Día 4: Mi agente completo (Fase 1 terminada) 

### Qué hice
- Creé `buscar.py` y probé **Tavily** solo: 3 resultados reales de internet.
- Creé `agente.py`: le di a Claude la herramienta `buscar_web` y él decidió
  solo qué buscar.
- Convertí `agente.py` en un **agente completo**:
  - **Loop**: Claude puede buscar varias veces (hizo 5 búsquedas en 3 vueltas).
  - Segunda herramienta, **`guardar_informe`**: guarda el informe en `informes/`.
  - **Instrucciones (system)** con la fecha de hoy y el formato del informe.
  - **Freno de seguridad**: máximo 10 vueltas.
  - **Resumen final**: vueltas, tokens y costo.
- Lo corrí con: `python agente.py "5 maneras de hacerte rico con agentes de IA"`
  → 4 vueltas, 14,838 tokens de entrada, 3,046 de salida, **$0.03 USD**.

### Qué aprendí
- **Cómo funciona un agente:**
  1. Escribo una pregunta y Python se la manda a Claude con el **menú de herramientas**.
  2. Claude lee el menú y le pide a Python: "busca X en internet".
  3. Python usa Tavily para buscar en la web real.
  4. Tavily le regresa la información a Python.
  5. Python se la pasa a Claude.
  6. Claude escribe la respuesta final y Python me la muestra.
- **Claude nunca toca internet**: solo piensa y pide. Mi código (el "asistente")
  es quien ejecuta.
- **Las 3 piezas de una herramienta**: el menú (descripción), la cocina
  (`def`, la función real) y el mesero (el código que ejecuta lo que Claude pide).
- **Archivo vs nombre en el código**: `buscar.py` es un archivo; `buscar_web`
  es un nombre que solo existe dentro del código.
- **`sys.argv`**: el tema se escribe al correr el programa, entre comillas.
  Si no escribo nada, usa un tema de respaldo.
- **VS Code y GitHub Desktop miran la misma carpeta**: VS Code guarda,
  GitHub Desktop detecta los cambios y los sube con commit + push.
- **Claude Pro vs mi agente**: Claude Pro es una herramienta para mí; mi agente
  se conecta a otros sistemas, se automatiza y se puede vender.

### Problemas y cómo los resolví
- **Claude buscó "2024" aunque estamos en 2026.**
  → Claude no sabe la fecha de hoy. Se la doy en las instrucciones con `date.today()`.
- **Al final Claude preguntaba "¿Te gustaría que profundice?".**
  → Mi agente no tiene ida y vuelta. En las instrucciones le pedí que no haga
  preguntas y que termine guardando el informe.
- **Confundía `buscar_web` con una carpeta.**
  → Es solo un nombre dentro del código, no aparece en la barra izquierda.

### Siguiente: Fase 2
- Llevar el agente a AWS: Lambda + API Gateway + S3.

## Día 5: Mi perfil de GitHub y el inicio de la Fase 2 (AWS)

### Qué hice

**GitHub**
- Agregué `informes/` al `.gitignore`: mis investigaciones se quedan en mi Mac
  y solo el código se sube a GitHub.
- Creé mi **perfil de GitHub** (`elfuturoconalex`) con un repositorio especial
  del mismo nombre:
  - `README.md`: mi presentación en inglés (versión corta).
  - `MY-STORY.md`: mi historia completa en inglés.
  - `MI-HISTORIA.md`: mi historia completa en español.
- Agregué mi nombre y una bio profesional al perfil.

**Fase 2, Paso 0: seguridad de la cuenta de AWS**
- Confirmé que mi usuario **root** tiene MFA (Duo) y no tiene claves de acceso.
- Creé una **alarma de presupuesto de $5 USD** (AWS Budgets): me avisa por correo
  al 85%, al 100% y si el gasto previsto supera $5.
- Creé el grupo **`administradores`** con la política `AdministratorAccess`.
- Creé mi usuario de trabajo **`alejandro-admin`** dentro de ese grupo,
  con **MFA** (Duo), y entré con él. Desde ahora ya no uso root para trabajar.

**Fase 2, Paso 2: almacenamiento**
- Creé el bucket de S3 `agente-investigador-informes-XXXXXXXXXXXX`
  en `us-east-1`, con acceso público bloqueado y cifrado SSE-S3.

**Fase 2, Paso 3: llaves seguras**
- Guardé mis 2 API keys en **Parameter Store** como **SecureString**:
  - `/agente-investigador/anthropic-api-key`
  - `/agente-investigador/tavily-api-key`

### Qué aprendí
- **Diff en GitHub:** fondo rojo con `-` = línea quitada; fondo verde con `+` = línea agregada.
  El color de las letras solo indica el tipo de palabra (no cambios).
- **Root vs usuario IAM:** root es la llave maestra (puede cerrar la cuenta).
  Se guarda para facturación y emergencias. Para el día a día uso un usuario IAM.
- **Grupos de IAM:** los permisos se asignan a un "puesto" (grupo) y las personas
  se agregan al grupo. Es la práctica recomendada en empresas.
- **Regiones:** un grupo de centros de datos en un lugar del mundo. Elegí
  `us-east-1` porque es barata, recibe novedades primero y la usan casi todos
  los tutoriales. Regla de oro: todo el proyecto en la misma región.
- **Bucket de S3:** el "cajón" donde se guardan archivos. Su nombre es único
  en todo el mundo, por eso le agregué mi número de cuenta.
- **ACL deshabilitadas:** los permisos se manejan en un solo lugar (políticas de IAM)
  y no archivo por archivo. Es como centralizar la política en un firewall
  en lugar de poner una ACL en cada puerto.
- **Control de versiones:** lo dejé desactivado; cada informe tendrá fecha y hora
  en el nombre, así nunca se sobrescribe.
- **Cifrado:** convierte los datos en texto ilegible sin la llave.
  En tránsito (HTTPS) y en reposo (SSE-S3). AWS lo hace gratis y automático.
- **Parameter Store:** es el `.env` de la nube. Guarda mis llaves cifradas y
  mi Lambda las lee solo si tiene permiso. Es gratis en su versión estándar
  (Secrets Manager cuesta $0.40/mes por llave).
- **Systems Manager:** la "navaja suiza" de AWS para administrar recursos;
  Parameter Store es una de sus herramientas.
- **Idiomas en GitHub:** perfil y README en inglés para un público internacional;
  la bitácora en español porque es mi diario de aprendizaje.

### Problemas y cómo los resolví
- **El buscador de AWS no encontraba "Budgets".**
  → Entré por Facturación → Monitor de costos → "Se requiere configuración".
- **El buscador tampoco encontraba "Parameter Store".**
  → Está dentro de Systems Manager.
- **No encontraba el botón para crear usuarios.**
  → Estaba en el Panel de IAM; el botón está en "Usuarios de IAM".
- **La app Contraseñas puso una contraseña inventada al crear un elemento.**
  → La reemplacé por la real y verifiqué cómo empezaba.

### Siguiente
- Crear `lambda_function.py` (el agente adaptado para la nube).
- Empaquetarlo con sus librerías y crear la Lambda.
- Crear la API con API Gateway y probar.

## Día 6: Mi agente vive en la nube (Fase 2 completa)
*5 y 6 de octubre de 2026*

### Qué hice
- Creé `lambda_function.py`: el mismo agente, adaptado para AWS (lee llaves de Parameter Store y guarda informes en S3).
- Empaqueté el código con sus librerías en un zip y agregué `paquete/` y `*.zip` al `.gitignore`.
- Creé la Lambda `agente-investigador` (Python 3.12) con 5 minutos de tiempo máximo y la variable `BUCKET_NAME`.
- Le di solo 3 permisos: leer mis llaves, guardar en S3 y llamarse a sí misma.
- Creé una HTTP API en API Gateway con la ruta `POST /investigar` y le puse límite de solicitudes (throttling).
- La probé con `curl` y el informe llegó a S3.
- Actualicé el README e hice el commit "Fase 2 completa: agente en AWS".

### Qué aprendí
- **Lambda:** código que solo se ejecuta cuando alguien lo llama; pago solo por los segundos que trabaja.
- **Rol de IAM:** el "gafete" de la Lambda; dice a qué puertas puede entrar.
- **API Gateway:** la "recepción" que recibe solicitudes de internet y se las pasa a la Lambda.
- **Throttling:** límite de solicitudes por segundo, como QoS.
- **Patrón tintorería:** la API solo espera ~30 segundos, así que la Lambda entrega un "ticket" al instante y trabaja en segundo plano.
- **curl:** un "navegador" de la Terminal para enviar solicitudes.
- **Costo:** AWS casi $0; Claude unos $0.03 por informe.

### Problemas y cómo los resolví
- El campo de integración tenía un texto extra ("X$") → lo borré y elegí la Lambda de la lista.
- No sabía dónde estaba la URL de mi API → API Gateway → Stages → $default → Invoke URL.
- El README se veía mal → sobraban unas comillas de código y un párrafo repetido; los borré.

### Siguiente
- Fase 3: observabilidad (búsquedas, vueltas, herramientas, tokens y costo de cada informe).

## Día 7: Observabilidad (Fase 3 completa)
*7 y 8 de octubre de 2026*

### Qué hice
- Revisé los logs de mi Lambda en CloudWatch para ver qué registraba ya el agente.
- Agregué una **traza** a `lambda_function.py`: en cada vuelta anota segundos, tokens, costo y herramientas usadas.
- La traza se guarda en S3 como `.json`, al lado de cada informe, y se guarda aunque haya un error.
- Empaqueté de nuevo, subí el zip a la Lambda y probé con `curl`.
- Con la primera traza encontré una **vuelta inútil**: después de guardar el informe, Claude solo decía "listo".
- Hice que el agente termine en cuanto guarda el informe y lo comprobé con una traza nueva.
- Usé **CloudWatch Logs Insights** para sacar promedios de todos los informes, y guardé la consulta como `costo-por-informe`.

### Qué aprendí
- **Observabilidad:** poder ver qué hizo el sistema sin adivinar. Como NetFlow o syslog, pero para un agente.
- **Traza:** la "bitácora de vuelo" de cada investigación.
- **La API de Claude no tiene memoria:** en cada vuelta se reenvía toda la conversación, por eso los tokens de entrada crecen.
- **Los tokens de salida cuestan 5 veces más:** la vuelta más cara es cuando Claude escribe el informe.
- **try / except / finally:** intentar, anotar el error si algo falla y, pase lo que pase, guardar la traza.
- **Logs Insights:** un "Excel para logs" que filtra, extrae números y saca promedios.
- **Medir antes de optimizar:** primero los datos, luego el cambio, y después comprobar con más de una muestra.

### Resultados
- Costo promedio por informe: **$0.0274 → $0.0214 (−22%)**.
- Tokens de entrada promedio: **12,989 → 7,689 (−41%)**.
- Con 1 dólar puedo generar unos 45 informes.

### Problemas y cómo los resolví
- La consulta de Logs Insights solo mostraba la última hora → cambié `START=-3600s` por `START=-604800s` (una semana).
- El `.gitignore` no tenía `__pycache__/` → lo agregué.

### Siguiente
- Agente #2.

## Día 8: Claude a través de Amazon Bedrock (Fase 4)
*8 de octubre de 2026*

### Qué hice
- Probé Claude Haiku 4.5 en el **Playground de Bedrock** y llené el formulario de uso de Anthropic (se pide una sola vez por cuenta).
- Esperé la **verificación de la cuenta** para usar Bedrock (la primera vez tarda hasta 2 horas).
- Agregué al rol de la Lambda el permiso `bedrock:InvokeModel`, solo para Claude Haiku 4.5.
- Cambié el código: `AnthropicBedrock` en lugar de `Anthropic`, y el modelo ahora es el perfil Global.
- Probé con el mismo tema y comparé la traza con la de Anthropic directo.
- Borré la llave de Claude de Parameter Store, porque ya no se usa.
- Actualicé el README y el diagrama de arquitectura.

### Qué aprendí
- **Amazon Bedrock:** la "tienda de modelos" de AWS. Usas Claude (y otros modelos) con tu cuenta, tus permisos y tu factura de AWS.
- **Perfil de inferencia:** por dónde viaja la pregunta. **Global** = más disponibilidad y mejor precio; **US** = los datos se quedan en EE. UU.
- **Autenticación con rol de IAM:** sin llaves que guardar. Una credencial menos que se pueda filtrar.
- **Mínimo privilegio también para modelos:** el permiso solo deja usar Haiku 4.5, no modelos más caros.
- **Validar costos contra la factura:** la traza calcula el costo con un precio fijo; hay que confirmarlo en Billing.

### Resultados
- Mismo comportamiento (3 vueltas, 5 búsquedas) y mismo tiempo (~32 s).
- Costo calculado: $0.0199 (Anthropic) contra $0.0206 (Bedrock). La diferencia viene del largo del informe.

### Problemas y cómo los resolví
- **AccessDeniedException: la cuenta se estaba verificando** → no era un error mío; esperé a que AWS terminara.

### Siguiente
- Revisar en Billing el costo real de Bedrock.
- Agente #2: soporte interno con RAG.

