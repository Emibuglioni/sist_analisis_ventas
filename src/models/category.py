"""
Módulo que contiene la clase Category para el manejo de categorías de productos.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    """Clase que representa una categoría de productos."""
    
    category_id: int
    category_name: str
    
    def __str__(self) -> str:
        """Retorna una representación en string de la categoría."""
        return f"Categoría: {self.category_name} (ID: {self.category_id})"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        return {
            "category_id": self.category_id,
            "category_name": self.category_name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        """
        Crea una instancia de Category a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos de la categoría
            
        Returns:
            Nueva instancia de Category
        """
        return cls(
            category_id=data["category_id"],
            category_name=data["category_name"]
        ) 