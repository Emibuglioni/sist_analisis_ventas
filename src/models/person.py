"""
Módulo que contiene la clase base Person para el manejo de personas.
"""
from dataclasses import dataclass
from typing import Optional
from .city import City

@dataclass
class Person:
    """Clase base que representa una persona."""
    
    first_name: str
    middle_initial: Optional[str]
    last_name: str
    city: City
    
    def __str__(self) -> str:
        """Retorna una representación en string de la persona."""
        middle = f" {self.middle_initial}." if self.middle_initial else ""
        return f"{self.first_name}{middle} {self.last_name}"
    
    def get_full_name(self) -> str:
        """Retorna el nombre completo de la persona."""
        return str(self)
    
    def get_location(self) -> str:
        """Retorna la ubicación de la persona (ciudad y país)."""
        return str(self.city)
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        return {
            "first_name": self.first_name,
            "middle_initial": self.middle_initial,
            "last_name": self.last_name,
            "city": self.city.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict, city: Optional[City] = None) -> 'Person':
        """
        Crea una instancia de Person a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos de la persona
            city: Instancia opcional de City. Si no se proporciona,
                 se creará a partir de los datos del diccionario
            
        Returns:
            Nueva instancia de Person
        """
        if city is None and "city" in data:
            city = City.from_dict(data["city"])
        elif city is None:
            raise ValueError("Se requiere una instancia de City o datos de city en el diccionario")
            
        return cls(
            first_name=data["first_name"],
            middle_initial=data.get("middle_initial"),  # Optional
            last_name=data["last_name"],
            city=city
        ) 