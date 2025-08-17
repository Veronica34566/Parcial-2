# 📊 API de Vacunación contra el Sarampión en Panamá

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

API RESTful pública **(solo lectura, GET-only)** para consultar datos históricos de cobertura de vacunación contra el **sarampión en niños de 12–23 meses en Panamá**.  

Fuente: **Banco Mundial** – Indicador `SH.IMM.MEAS`.

---

## 🚀 Tecnologías usadas
- **Python 3.10+**
- **FastAPI** (framework web)
- **Uvicorn** (servidor ASGI)
- **Pydantic** (modelado de datos)
- **Pytest** (pruebas unitarias)

---

## 📦 Instalación y ejecución

```bash
# 1. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor
uvicorn app.main:app --reload
📌 La documentación interactiva estará disponible en:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

📡 Endpoints disponibles
Método	Ruta	Descripción
GET	/vacunas	Devuelve todos los registros nacionales.
GET	/vacunas/{anio}	Devuelve el registro para el año especificado.
GET	/vacunas/provincia/{nombre}	(Opcional/simulado) Devuelve un valor estimado por provincia/comarca para un año dado.

🔹 Nota: El Banco Mundial no ofrece datos regionales. El endpoint /vacunas/provincia/{nombre} genera valores simulados determinísticos a partir del dato nacional.

🗂️ Estructura del proyecto
bash
Copiar
Editar
panama-measles-api/
├─ app/
│  ├─ __init__.py
│  ├─ main.py          # Rutas y FastAPI app
│  ├─ service.py       # Carga de datos (Banco Mundial + cache local)
│  ├─ schemas.py       # Modelos de datos (Pydantic)
│  └─ utils.py         # Provincias + simulación
├─ data/
│  └─ local_cache.json # Cache local (offline)
├─ tests/
│  └─ test_api.py      # Pruebas unitarias con pytest
├─ requirements.txt
├─ README.md
└─ .gitignore
🔗 Fuente de datos
API del Banco Mundial:
https://api.worldbank.org/v2/country/PAN/indicator/SH.IMM.MEAS?format=json&per_page=20000

País: Panamá (PAN)

Indicador: Cobertura de vacunación contra el sarampión (SH.IMM.MEAS)

📌 Para refrescar datos desde el Banco Mundial en tiempo de ejecución:

bash
Copiar
Editar
WB_REFRESH=1 uvicorn app.main:app --reload
Y para guardar el resultado en data/local_cache.json:

bash
Copiar
Editar
WB_REFRESH=1 WB_WRITE_CACHE=1 uvicorn app.main:app --reload
🧪 Pruebas
Ejecutar pruebas unitarias con pytest:

bash
Copiar
Editar
pytest -q
Incluye pruebas para:

/health

/vacunas

/vacunas/{anio}

/vacunas/provincia/{nombre}

📄 Licencia
Este proyecto se distribuye bajo licencia MIT.
Uso libre con fines académicos.
