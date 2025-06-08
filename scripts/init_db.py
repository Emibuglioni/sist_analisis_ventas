"""
Script para inicializar la base de datos.
"""
import os
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv

def init_database():
    """Inicializa la base de datos con el esquema y datos de ejemplo."""
    # Cargar variables de entorno
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    
    # Obtener credenciales
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', '3306'))
    }
    
    try:
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Leer y ejecutar el script SQL
        sql_path = Path(__file__).parent.parent / 'sql' / 'init_database.sql'
        with open(sql_path, 'r', encoding='utf-8') as file:
            # Dividir el script en comandos individuales
            sql_commands = file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command + ';')
            
        connection.commit()
        print("Base de datos inicializada exitosamente")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    init_database() 