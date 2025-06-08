"""
Módulo que contiene la clase Customer para el manejo de clientes.
"""
from dataclasses import dataclass
from typing import Optional
from .person import Person
from .city import City

@dataclass
class Customer(Person):
    """Clase que representa un cliente."""
    
    customer_id: int
    address: str
    
    def __str__(self) -> str:
        """Retorna una representación en string del cliente."""
        return f"Cliente: {super().__str__()}"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        base_dict = super().to_dict()
        base_dict.update({
            "customer_id": self.customer_id,
            "address": self.address
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: dict, city: Optional[City] = None) -> 'Customer':
        """
        Crea una instancia de Customer a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del cliente
            city: Instancia opcional de City. Si no se proporciona,
                 se creará a partir de los datos del diccionario
            
        Returns:
            Nueva instancia de Customer
        """
        if city is None and "city" in data:
            city = City.from_dict(data["city"])
        elif city is None:
            raise ValueError("Se requiere una instancia de City o datos de city en el diccionario")
            
        return cls(
            customer_id=data["customer_id"],
            first_name=data["first_name"],
            middle_initial=data.get("middle_initial"),
            last_name=data["last_name"],
            city=city,
            address=data["address"]
        )
    
    def get_full_address(self) -> str:
        """Retorna la dirección completa del cliente incluyendo ciudad y país."""
        return f"{self.address}, {self.city.get_full_address()}"
    
    def is_local_customer(self, store_city: City) -> bool:
        """
        Verifica si el cliente es local a una tienda específica.
        
        Args:
            store_city: Ciudad de la tienda
            
        Returns:
            True si el cliente vive en la misma ciudad que la tienda
        """
        return self.city.city_id == store_city.city_id 