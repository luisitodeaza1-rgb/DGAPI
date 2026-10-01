from fastapi import FastAPI

from database import obtener_conexion
from routes.rnc import router as rnc_router


app = FastAPI(
    title="API RNC DGII",
    description="API personal para consulta de RNC",
    version="1.0.0"
)


app.include_router(rnc_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API RNC DGII funcionando"
    }


@app.get("/health")
def health_check():

    try:
        conexion = obtener_conexion()
        conexion.execute("SELECT 1")
        conexion.close()

        return {
            "estado": "ok",
            "api": "funcionando",
            "base_de_datos": "conectada"
        }

    except Exception:
        return {
            "estado": "error",
            "api": "funcionando",
            "base_de_datos": "no disponible"
        }