import sqlite3

DATABASE = "rnc.db"


def buscar_rnc(numero_rnc):
    conexion = sqlite3.connect(DATABASE)
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

    return resultado


rnc = input("Introduce el RNC: ")

resultado = buscar_rnc(rnc)

if resultado:
    print("\nRNC encontrado:")
    print(f"RNC: {resultado[0]}")
    print(f"Nombre: {resultado[1]}")
    print(f"Nombre comercial: {resultado[2]}")
    print(f"Actividad económica: {resultado[3]}")
    print(f"Fecha de inicio: {resultado[4]}")
    print(f"Estado: {resultado[5]}")
    print(f"Régimen de pago: {resultado[6]}")
else:
    print("\nRNC no encontrado.")