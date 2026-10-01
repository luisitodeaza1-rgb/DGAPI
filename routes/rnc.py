from typing import List

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from database import obtener_conexion


router = APIRouter(
    prefix="/rnc",
    tags=["RNC"]
)


class RNCResponse(BaseModel):
    encontrado: bool
    rnc: str
    nombre: str | None = None
    nombre_comercial: str | None = None
    actividad_economica: str | None = None
    fecha_inicio: str | None = None
    estado: str | None = None
    regimen_pago: str | None = None
    mensaje: str | None = None


class RNCBusquedaResponse(BaseModel):
    cantidad: int
    busqueda: str
    limite: int
    offset: int
    resultados: List[RNCResponse]


class RNCValidacionResponse(BaseModel):
    valido: bool
    existe: bool
    rnc: str
    nombre: str | None = None
    estado: str | None = None
    mensaje: str


@router.get("/buscar", response_model=RNCBusquedaResponse)
def buscar_por_nombre(
    nombre: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):

    nombre = nombre.strip()

    if not nombre:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar un nombre para realizar la búsqueda"
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            rnc,
            nombre,
            nombre_comercial,
            actividad_economica,
            fecha_inicio,
            estado,
            regimen_pago
        FROM rnc
        WHERE UPPER(nombre) LIKE UPPER(?)
        ORDER BY nombre ASC
        LIMIT ? OFFSET ?
    """, (f"{nombre}%", limit, offset))

    resultados = cursor.fetchall()

    conexion.close()

    return {
        "cantidad": len(resultados),
        "busqueda": nombre,
        "limite": limit,
        "offset": offset,
        "resultados": [
            {
                "encontrado": True,
                "rnc": resultado[0],
                "nombre": resultado[1],
                "nombre_comercial": resultado[2],
                "actividad_economica": resultado[3],
                "fecha_inicio": resultado[4],
                "estado": resultado[5],
                "regimen_pago": resultado[6]
            }
            for resultado in resultados
        ]
    }


@router.get("/validar", response_model=RNCValidacionResponse)
def validar_rnc(numero_rnc: str):

    numero_rnc = numero_rnc.replace("-", "").replace(" ", "")

    if not numero_rnc.isdigit():
        raise HTTPException(
            status_code=400,
            detail="El RNC debe contener solamente números"
        )

    if len(numero_rnc) not in [9, 11]:
        raise HTTPException(
            status_code=400,
            detail="El RNC debe tener 9 u 11 dígitos"
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT rnc, nombre, estado FROM rnc WHERE rnc = ?",
        (numero_rnc,)
    )

    resultado = cursor.fetchone()

    conexion.close()

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail={
                "valido": True,
                "existe": False,
                "rnc": numero_rnc,
                "mensaje": "El formato del RNC es válido, pero no existe en la base de datos"
            }
        )

    return {
        "valido": True,
        "existe": True,
        "rnc": resultado[0],
        "nombre": resultado[1],
        "estado": resultado[2],
        "mensaje": "El RNC tiene un formato válido y existe en la base de datos"
    }


@router.get("/{numero_rnc}", response_model=RNCResponse)
def consultar_rnc(numero_rnc: str):

    numero_rnc = numero_rnc.replace("-", "").replace(" ", "")

    if not numero_rnc.isdigit():
        raise HTTPException(
            status_code=400,
            detail="El RNC debe contener solamente números"
        )

    if len(numero_rnc) not in [9, 11]:
        raise HTTPException(
            status_code=400,
            detail="El RNC debe tener 9 u 11 dígitos"
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            rnc,
            nombre,
            nombre_comercial,
            actividad_economica,
            fecha_inicio,
            estado,
            regimen_pago
        FROM rnc
        WHERE rnc = ?
    """, (numero_rnc,))

    resultado = cursor.fetchone()

    conexion.close()

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="RNC no encontrado en la base de datos"
        )

    return {
        "encontrado": True,
        "rnc": resultado[0],
        "nombre": resultado[1],
        "nombre_comercial": resultado[2],
        "actividad_economica": resultado[3],
        "fecha_inicio": resultado[4],
        "estado": resultado[5],
        "regimen_pago": resultado[6]
    }