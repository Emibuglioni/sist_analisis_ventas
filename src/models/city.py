"""
Módulo que contiene la clase City para el manejo de ciudades.
"""
from dataclasses import dataclass
from typing import Optional
from .country import Country

@dataclass
class City:
    """Clase que representa una ciudad."""
    
    city_id: int
    city_name: str
    zipcode: str
    country: Country
    
    def __str__(self) -> str:
        """Retorna una representación en string de la ciudad."""
        return f"{self.city_name}, {self.country.country_name}"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        return {
            "city_id": self.city_id,
            "city_name": self.city_name,
            "zipcode": self.zipcode,
            "country": self.country.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict, country: Optional[Country] = None) -> 'City':
        """
        Crea una instancia de City a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos de la ciudad
            country: Instancia opcional de Country. Si no se proporciona,
                    se creará a partir de los datos del diccionario
            
        Returns:
            Nueva instancia de City
        """
        if country is None and "country" in data:
            country = Country.from_dict(data["country"])
        elif country is None:
            raise ValueError("Se requiere una instancia de Country o datos de country en el diccionario")
            
        return cls(
            city_id=data["city_id"],
            city_name=data["city_name"],
            zipcode=data["zipcode"],
            country=country
        )
    
    def get_full_address(self) -> str:
        """Retorna la dirección completa incluyendo código postal y país."""
        return f"{self.city_name} ({self.zipcode}), {self.country.country_name}"
    
    def is_same_country(self, other_city: 'City') -> bool:
        """
        Verifica si dos ciudades están en el mismo país.
        
        Args:
            other_city: Ciudad a comparar
            
        Returns:
            True si ambas ciudades están en el mismo país
        """
        return self.country.country_id == other_city.country.country_id 