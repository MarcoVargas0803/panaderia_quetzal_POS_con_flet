#Archivo para recuperar los fetch de la BD. 

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Esto busca el archivo .env en la raíz del proyecto
load_dotenv()

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None