# DGAPI — RNC Data & Validation API

REST API desarrollada en Python para consultar, buscar y validar información de contribuyentes registrados mediante datos de RNC de la República Dominicana.

El proyecto utiliza **FastAPI**, **Pydantic** y **SQLite** para proporcionar una API REST modular, documentada y reutilizable.

> Proyecto personal orientado a la integración de servicios de consulta de datos fiscales con aplicaciones de facturación y sistemas administrativos.

## Tecnologías

* Python
* FastAPI
* Pydantic
* SQLite
* SQL
* REST API
* HTTP / JSON
* Uvicorn
* Git / GitHub

## Funcionalidades

### Consulta por RNC

Permite consultar la información asociada a un RNC específico.

`GET /rnc/{numero_rnc}`

Ejemplo:

`GET /rnc/101010101`

Devuelve información como:

* RNC
* Nombre
* Nombre comercial
* Actividad económica
* Fecha de inicio
* Estado
* Régimen de pago

### Búsqueda por nombre

Permite localizar contribuyentes utilizando el inicio de su nombre.

`GET /rnc/buscar?nombre=DSM`

También incorpora:

* Límite de resultados
* Offset para paginación
* Búsqueda sin distinción entre mayúsculas y minúsculas
* Ordenamiento alfabético

Ejemplo:

`GET /rnc/buscar?nombre=DSM&limit=20&offset=0`

### Validación de RNC

Comprueba que el RNC tenga un formato válido y verifica si existe dentro de la base de datos.

`GET /rnc/validar?numero_rnc=101010101`

La validación contempla:

* Solo caracteres numéricos
* RNC de 9 u 11 dígitos
* Existencia del RNC en la base de datos
* Respuestas HTTP diferenciadas para errores y resultados

### Health Check

Permite comprobar el estado de la API y su conexión con SQLite.

`GET /health`

Respuesta de ejemplo:

```json
{
  "estado": "ok",
  "api": "funcionando",
  "base_de_datos": "conectada"
}
```

## Documentación interactiva

FastAPI genera automáticamente documentación interactiva mediante Swagger UI.

Una vez iniciada la aplicación:

`http://127.0.0.1:8001/docs`

Desde allí se pueden probar directamente los endpoints de la API.

## Arquitectura del proyecto

```text
DGAPI/
│
├── data/
│   └── DGII_RNC.TXT
│
├── routes/
│   └── rnc.py
│
├── database.py
├── importar_rnc.py
├── buscar_rnc.py
├── main.py
├── rnc.db
├── .gitignore
└── README.md
```

Los archivos de datos de gran tamaño y la base de datos local están excluidos del repositorio mediante `.gitignore`.

## Organización del código

El proyecto utiliza una estructura modular para separar responsabilidades.

`main.py`

Punto de entrada de la aplicación FastAPI y configuración principal de la API.

`routes/rnc.py`

Contiene los endpoints relacionados con RNC, validaciones, consultas y modelos de respuesta.

`database.py`

Centraliza la conexión con SQLite y la creación de la estructura de la base de datos.

`importar_rnc.py`

Procesa el archivo de datos y realiza la importación de registros hacia SQLite.

`buscar_rnc.py`

Script independiente para realizar consultas de RNC desde la terminal.

## Base de datos

DGAPI utiliza SQLite como sistema de almacenamiento local.

La información importada se organiza en una tabla `rnc` con campos como:

```text
rnc
nombre
nombre_comercial
actividad_economica
fecha_inicio
estado
regimen_pago
```

La base local contiene aproximadamente **790,000 registros** procesados a partir del archivo de datos utilizado por el proyecto.

Los archivos de datos originales y la base SQLite no se incluyen en GitHub debido a su tamaño y se mantienen localmente.

## Instalación

Clonar el repositorio:

```text
git clone https://github.com/luisitodeaza1-rgb/DGAPI.git
```

Entrar al proyecto:

```text
cd DGAPI
```

Crear un entorno virtual:

```text
python -m venv venv
```

Activar el entorno virtual en Windows PowerShell:

```text
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```text
pip install fastapi uvicorn pydantic
```

## Ejecución

Iniciar la API:

```text
python -m uvicorn main:app --port 8001
```

La API estará disponible en:

```text
http://127.0.0.1:8001
```

Documentación:

```text
http://127.0.0.1:8001/docs
```

## Ejemplo de respuesta

Consulta:

`GET /rnc/101010101`

Respuesta:

```json
{
  "encontrado": true,
  "rnc": "101010101",
  "nombre": "EMPRESA EJEMPLO",
  "nombre_comercial": "EMPRESA EJEMPLO",
  "actividad_economica": "SERVICIOS",
  "fecha_inicio": "01/01/2020",
  "estado": "ACTIVO",
  "regimen_pago": "NORMAL"
}
```

## Manejo de errores

DGAPI utiliza códigos de estado HTTP para comunicar diferentes resultados.

| Código | Situación                        |
| ------ | -------------------------------- |
| 200    | Consulta realizada correctamente |
| 400    | Parámetros o formato inválido    |
| 404    | RNC no encontrado                |
| 500    | Error interno del servidor       |

## Objetivos de aprendizaje

Este proyecto fue desarrollado para aplicar conocimientos de:

* Programación con Python
* Desarrollo de APIs REST
* FastAPI
* Pydantic
* SQL y SQLite
* Procesamiento de archivos
* Validación de datos
* Manejo de errores HTTP
* Arquitectura modular
* Documentación de APIs
* Git y GitHub

## Posibles integraciones

DGAPI fue diseñada como un componente independiente y reutilizable.

Entre sus posibles usos se encuentran:

* Sistemas de facturación
* Sistemas administrativos
* Aplicaciones contables
* Herramientas de validación de clientes
* Sistemas de gestión empresarial
* Aplicaciones que requieran consultas de RNC

## Próximas mejoras

Algunas mejoras consideradas para futuras versiones:

* Variables de entorno para configuración
* Sistema de logging
* Tests automatizados
* Docker
* Índices adicionales para optimización de consultas
* Autenticación mediante API Keys
* Rate limiting
* Endpoint para estadísticas
* Integración con una aplicación de facturación

## Autor

**Luis Manuel De Aza Salcedo**

Systems Engineering Student | Junior Python Developer

Intereses:

* Python
* Backend Development
* REST APIs
* Data Analysis
* Databases
* Cybersecurity
* Automation

## Licencia

Proyecto desarrollado con fines educativos, de aprendizaje y portafolio profesional.
