"""
Módulo que contiene la clase Product para el manejo de productos.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .category import Category

@dataclass
class Product:
    """Clase que representa un producto."""
    
    product_id: int
    product_name: str
    price: float
    category: Category
    product_class: str
    modify_date: datetime
    resistant: bool
    is_allergic: bool
    vitality_days: int
    
    def __str__(self) -> str:
        """Retorna una representación en string del producto."""
        return f"{self.product_name} - {self.category.category_name} (${self.price:.2f})"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "category": self.category.to_dict(),
            "product_class": self.product_class,
            "modify_date": self.modify_date.isoformat(),
            "resistant": self.resistant,
            "is_allergic": self.is_allergic,
            "vitality_days": self.vitality_days
        }
    
    @classmethod
    def from_dict(cls, data: dict, category: Optional[Category] = None) -> 'Product':
        """
        Crea una instancia de Product a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del producto
            category: Instancia opcional de Category. Si no se proporciona,
                     se creará a partir de los datos del diccionario
            
        Returns:
            Nueva instancia de Product
        """
        if category is None and "category" in data:
            category = Category.from_dict(data["category"])
        elif category is None:
            raise ValueError("Se requiere una instancia de Category o datos de category en el diccionario")
            
        return cls(
            product_id=data["product_id"],
            product_name=data["product_name"],
            price=float(data["price"]),
            category=category,
            product_class=data["product_class"],
            modify_date=datetime.fromisoformat(data["modify_date"]) if isinstance(data["modify_date"], str) else data["modify_date"],
            resistant=bool(data["resistant"]),
            is_allergic=bool(data["is_allergic"]),
            vitality_days=int(data["vitality_days"])
        )
    
    def calculate_discount_price(self, discount_percentage: float) -> float:
        """
        Calcula el precio con descuento.
        
        Args:
            discount_percentage: Porcentaje de descuento (0-100)
            
        Returns:
            Precio con descuento aplicado
        """
        if not 0 <= discount_percentage <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100")
        return self.price * (1 - discount_percentage / 100)
    
    def is_expired(self, reference_date: Optional[datetime] = None) -> bool:
        """
        Verifica si el producto está expirado basado en sus días de vitalidad.
        
        Args:
            reference_date: Fecha de referencia para el cálculo. Si no se proporciona,
                          se usa la fecha actual
            
        Returns:
            True si el producto está expirado
        """
        if reference_date is None:
            reference_date = datetime.now()
            
        expiration_date = self.modify_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        expiration_date = expiration_date.fromordinal(expiration_date.toordinal() + self.vitality_days)
        return reference_date > expiration_date
    
    def get_storage_instructions(self) -> str:
        """
        Genera instrucciones de almacenamiento basadas en las características del producto.
        
        Returns:
            String con las instrucciones de almacenamiento
        """
        instructions = []
        
        if self.is_allergic:
            instructions.append("¡PRECAUCIÓN! Producto alergénico")
            
        if self.resistant:
            instructions.append("Producto resistente - Almacenamiento estándar")
        else:
            instructions.append("Producto delicado - Requiere almacenamiento especial")
            
        instructions.append(f"Vida útil: {self.vitality_days} días desde fabricación")
        
        return " | ".join(instructions) 