import psycopg2
from datetime import datetime

# Configura tu conexión a PostgreSQL aquí
conn = psycopg2.connect(
    dbname="proyectoRafa",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

def crear_tabla():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellidos VARCHAR(50) NOT NULL,
                correo VARCHAR(100) UNIQUE NOT NULL,
                contrasena VARCHAR(50) NOT NULL,
                Fecha_Nacimiento DATE NOT NULL,
                estado BOOLEAN DEFAULT TRUE,
                Fecha_Registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Ultimo_Login TIMESTAMP
            );
        """)
        conn.commit()

def insertar_usuario(nombre, apellidos, correo, contrasena, fecha_nacimiento):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (nombre, apellidos, correo, contrasena, Fecha_Nacimiento)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, correo, contrasena, fecha_nacimiento))
        conn.commit()

def verificar_usuario(correo, contrasena):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM users WHERE correo = %s AND contrasena = %s
        """, (correo, contrasena))
        result = cur.fetchone()
        if result:
            cur.execute("UPDATE users SET Ultimo_Login = %s WHERE id = %s", (datetime.now(), result[0]))
            conn.commit()
            return True
        return False

crear_tabla()
