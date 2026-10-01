import sqlite3

DATABASE = "rnc.db"


def obtener_conexion():
    return sqlite3.connect(DATABASE)


def crear_base_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rnc (
            rnc TEXT PRIMARY KEY,
            nombre TEXT,
            nombre_comercial TEXT,
            actividad_economica TEXT,
            fecha_inicio TEXT,
            estado TEXT,
            regimen_pago TEXT
        )
    """)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos creada correctamente.")