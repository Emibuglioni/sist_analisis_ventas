"""
Módulo para manejar la configuración y variables de entorno.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class DatabaseConfig:
    """Configuración de la base de datos."""
    
    HOST = os.getenv('DB_HOST', 'localhost')
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = os.getenv('DB_NAME', 'ventas_db')
    PORT = int(os.getenv('DB_PORT', '3306'))
    
    @classmethod
    def get_connection_params(cls) -> dict:
        """
        Obtiene los parámetros de conexión a la base de datos.
        
        Returns:
            Dict con los parámetros de conexión
        """
        return {
            'host': cls.HOST,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'port': cls.PORT
        }

class Config:
    """Configuración general de la aplicación."""
    
    # Ambiente de ejecución
    ENV = os.getenv('ENV', 'development')
    DEBUG = ENV == 'development'
    
    # Configuración de la base de datos
    DB = DatabaseConfig
    
    # Otras configuraciones
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-for-dev') 