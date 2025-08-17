# API de Vacunación contra Sarampión en Panamá (GET-only)

API RESTful pública (solo lectura) para consultar datos históricos de cobertura de vacunación contra el sarampión en niños de 12–23 meses en Panamá.  
Fuente: **Banco Mundial** — Indicador `SH.IMM.MEAS`.

## 🚀 Stack
- **Python** + **FastAPI**
- **Pydantic** para modelos
- **Uvicorn** como ASGI server
- **Pytest** para pruebas

## 📦 Instalación
```bash
python -m venv .venv && source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Ejecución
```bash
uvicorn app.main:app --reload
```
La documentación interactiva estará en:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🔗 Fuente de datos (World Bank API)
- Indicador: `SH.IMM.MEAS`
- País: `PAN`
- Endpoint (JSON): `https://api.worldbank.org/v2/country/PAN/indicator/SH.IMM.MEAS?format=json&per_page=20000`

> La app incluye un pequeño **cache local** en `data/local_cache.json` para que funcione sin internet.  
> Si quieres forzar la actualización desde el Banco Mundial en tiempo de ejecución, ejecuta el servidor con:
> ```bash
> WB_REFRESH=1 uvicorn app.main:app --reload
> ```
> Y, si además quieres **persistir** el resultado al archivo `data/local_cache.json`:
> ```bash
> WB_REFRESH=1 WB_WRITE_CACHE=1 uvicorn app.main:app --reload
> ```

## 📡 Endpoints (GET-only)
- `GET /vacunas` → Lista de todos los registros (año, valor).
- `GET /vacunas/{anio}` → Registro para el año especificado (ej. `2001`).
- `GET /vacunas/provincia/{nombre}?year=YYYY` → **Opcional/simulado**. Devuelve un valor **estimado** por provincia/comarca para el año dado (o el último disponible).  
  > Nota: El Banco Mundial **no** ofrece datos regionales; esta ruta genera valores determinísticos simulados a partir del dato nacional del año.

## 🧪 Pruebas
```bash
pytest -q
```

## 🗂️ Estructura del proyecto
```text
panama-measles-api/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ service.py
│  ├─ schemas.py
│  └─ utils.py
├─ data/
│  └─ local_cache.json        # cache mínimo para funcionar offline
├─ tests/
│  └─ test_api.py
├─ requirements.txt
├─ README.md
└─ .gitignore
```

## 📄 Licencia
MIT – libre uso académico.
