import sqlite3

ARCHIVO_RNC = "data/DGII_RNC.TXT"
DATABASE = "rnc.db"


def importar_rnc():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    contador = 0

    with open(ARCHIVO_RNC, "r", encoding="latin-1") as archivo:

        for linea in archivo:
            campos = linea.strip().split("|")

            if len(campos) < 11:
                continue

            rnc = campos[0].strip()
            nombre = campos[1].strip()
            nombre_comercial = campos[2].strip()
            actividad_economica = campos[3].strip()
            fecha_inicio = campos[8].strip()
            estado = campos[9].strip()
            regimen_pago = campos[10].strip()

            cursor.execute("""
                INSERT OR REPLACE INTO rnc (
                    rnc,
                    nombre,
                    nombre_comercial,
                    actividad_economica,
                    fecha_inicio,
                    estado,
                    regimen_pago
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                rnc,
                nombre,
                nombre_comercial,
                actividad_economica,
                fecha_inicio,
                estado,
                regimen_pago
            ))

            contador += 1

            if contador % 10000 == 0:
                conexion.commit()
                print(f"Registros importados: {contador}")

    conexion.commit()
    conexion.close()

    print(f"\nImportación terminada.")
    print(f"Total de registros: {contador}")


if __name__ == "__main__":
    importar_rnc()