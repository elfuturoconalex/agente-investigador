# Agente Investigador 🔎

Agente de IA que recibe un tema, busca en la web, resume la información y guarda un informe estructurado.

## Fases del proyecto

- [x] **Fase 1:** Agente funcionando en local
- [x] **Fase 2:** Desplegado en AWS (Lambda + API Gateway + S3)
- [x] **Fase 3:** Observabilidad (trazas, herramientas usadas, tokens y costo)

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

## Cómo usarlo

### En local (mi Mac)

```bash
python agente.py "el tema que quieras investigar"
```

El informe se guarda en la carpeta `informes/`.

### En la nube (AWS)

En varios renglones:

```bash
curl -X POST https://<TU-API>.execute-api.us-east-1.amazonaws.com/investigar \
  -H "Content-Type: application/json" \
  -d '{"tema": "el tema que quieras"}'
```

O en un solo renglón:

```bash
curl -X POST https://<TU-API>.execute-api.us-east-1.amazonaws.com/investigar -H "Content-Type: application/json" -d '{"tema": "el tema que quieras"}'
```

La API responde al instante con el nombre del informe, y el agente trabaja en segundo plano. El informe se guarda en S3, en la carpeta `informes/`.

## Arquitectura en AWS

```
curl → API Gateway → Lambda (responde "recibido")
                       ↓ se llama a sí misma en segundo plano
                     Lambda → Parameter Store (llaves cifradas)
                            → Claude + Tavily (investigación)
                            → S3 (guarda el informe .md y su traza .json)
                            → CloudWatch Logs (renglón TRAZA para reportes)
```

## Observabilidad

Cada investigación guarda una **traza** en S3, al lado del informe y con el mismo nombre, pero `.json`. Por cada vuelta registra:

- segundos que tardó Claude
- tokens de entrada y salida, y costo en USD
- herramientas usadas, qué buscó y cuánto tardó cada una

También guarda los totales (vueltas, búsquedas, tokens, costo y segundos) y el estado (`ok` o `error`).

### Optimización encontrada con las trazas

La primera traza mostró una vuelta extra **después** de guardar el informe, solo para que Claude dijera "listo". Esa vuelta reenviaba todo el informe y costaba ~27% del total. Ahora el agente termina en cuanto guarda el informe.

| | Antes (4 vueltas) | Después (3 vueltas) | Cambio |
|---|---|---|---|
| Costo promedio por informe | $0.0274 | $0.0214 | **−22%** |
| Tokens de entrada promedio | 12,989 | 7,689 | **−41%** |
| Segundos promedio | 34.7 | 33.9 | −2% |

*Medido con CloudWatch Logs Insights: 1 informe antes y 4 después.*

### Reporte de costo (CloudWatch Logs Insights)

Grupo de logs: `/aws/lambda/agente-investigador`

```
filter @message like /TRAZA/
| parse @message /"vueltas": (?<vueltas>\d+)/
| parse @message /"tokens_entrada": (?<entrada>\d+)/
| parse @message /"costo_usd": (?<costo>[\d.]+)/
| parse @message /"segundos": (?<segundos>[\d.]+)/
| stats count() as informes, avg(costo) as costo_promedio, sum(costo) as costo_total, avg(entrada) as tokens_entrada_promedio, avg(segundos) as segundos_promedio by vueltas
```
