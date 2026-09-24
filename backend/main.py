from fastapi import FastAPI, HTTPException
from config.database import get_connection

app = FastAPI(
    title="Clase CSR",
    description="Primera conexión entre FastAPI y PostgreSQL",
    version="1.0",
)


# Endpoint de prueba de conexión a la base de datos
@app.get("/db-test")
def probar_base_datos():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT current_database() AS base_datos,
                       current_user AS usuario,
                       NOW() AS fecha_hora;
                """)
                resultado = cursor.fetchone()
                return {"conexion": "correcta", "informacion": resultado}
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"No fue posible conectarse a PostgreSQL: {error}",
        )


# Endpoint para obtener la lista de estudiantes
@app.get("/estudiantes")
def obtener_estudiantes():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                SELECT
                    id,
                    nombre,
                    correo,
                    creado_en
                FROM estudiantes
                ORDER BY id;
                """)
                resultado = cursor.fetchall()
                return {"estudiantes": resultado}
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estudiantes: {error}",
        )