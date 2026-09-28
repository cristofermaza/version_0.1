from database.connection import obtener_conexion


conexion = obtener_conexion()
cursor = conexion.cursor()

cursor.execute(
    "DELETE FROM empleados WHERE id_usuario = %s",
    ("TEST001",)
)

conexion.commit()

print("Empleados eliminados:", cursor.rowcount)

cursor.close()
conexion.close()