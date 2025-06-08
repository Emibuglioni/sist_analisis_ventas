"""
Módulo que contiene la clase Country para el manejo de países.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Country:
    """Clase que representa un país."""
    
    country_id: int
    country_name: str
    country_code: str
    
    def __str__(self) -> str:
        """Retorna una representación en string del país."""
        return f"{self.country_name} ({self.country_code})"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        return {
            "country_id": self.country_id,
            "country_name": self.country_name,
            "country_code": self.country_code
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Country':
        """
        Crea una instancia de Country a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del país
            
        Returns:
            Nueva instancia de Country
        """
        return cls(
            country_id=data["country_id"],
            country_name=data["country_name"],
            country_code=data["country_code"]
        )
        
    def get_formatted_code(self) -> str:
        """Retorna el código del país en formato estándar ISO."""
        return self.country_code.upper() 