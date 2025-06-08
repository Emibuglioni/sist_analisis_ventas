"""
Módulo que contiene la clase Sale para el manejo de ventas.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .employee import Employee
from .customer import Customer
from .product import Product

@dataclass
class Sale:
    """Clase que representa una venta."""
    
    sale_id: int
    sales_person: Employee
    customer: Customer
    product: Product
    quantity: int
    discount: float
    total_price: float
    sales_date: datetime
    transaction_number: str
    
    def __str__(self) -> str:
        """Retorna una representación en string de la venta."""
        return f"Venta #{self.sale_id} - {self.transaction_number}"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        return {
            "sale_id": self.sale_id,
            "sales_person": self.sales_person.to_dict(),
            "customer": self.customer.to_dict(),
            "product": self.product.to_dict(),
            "quantity": self.quantity,
            "discount": self.discount,
            "total_price": self.total_price,
            "sales_date": self.sales_date.isoformat(),
            "transaction_number": self.transaction_number
        }
    
    @classmethod
    def from_dict(cls, data: dict, 
                 sales_person: Optional[Employee] = None,
                 customer: Optional[Customer] = None,
                 product: Optional[Product] = None) -> 'Sale':
        """
        Crea una instancia de Sale a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos de la venta
            sales_person: Instancia opcional de Employee
            customer: Instancia opcional de Customer
            product: Instancia opcional de Product
            
        Returns:
            Nueva instancia de Sale
        """
        if sales_person is None and "sales_person" in data:
            sales_person = Employee.from_dict(data["sales_person"])
        elif sales_person is None:
            raise ValueError("Se requiere una instancia de Employee o datos de sales_person en el diccionario")
            
        if customer is None and "customer" in data:
            customer = Customer.from_dict(data["customer"])
        elif customer is None:
            raise ValueError("Se requiere una instancia de Customer o datos de customer en el diccionario")
            
        if product is None and "product" in data:
            product = Product.from_dict(data["product"])
        elif product is None:
            raise ValueError("Se requiere una instancia de Product o datos de product en el diccionario")
            
        return cls(
            sale_id=data["sale_id"],
            sales_person=sales_person,
            customer=customer,
            product=product,
            quantity=int(data["quantity"]),
            discount=float(data["discount"]),
            total_price=float(data["total_price"]),
            sales_date=datetime.fromisoformat(data["sales_date"]) if isinstance(data["sales_date"], str) else data["sales_date"],
            transaction_number=data["transaction_number"]
        )
    
    def calculate_unit_price(self) -> float:
        """
        Calcula el precio unitario considerando el descuento.
        
        Returns:
            Precio unitario con descuento
        """
        return self.total_price / self.quantity
    
    def get_discount_amount(self) -> float:
        """
        Calcula el monto total del descuento aplicado.
        
        Returns:
            Monto total del descuento
        """
        original_price = self.product.price * self.quantity
        return original_price - self.total_price
    
    def get_discount_percentage(self) -> float:
        """
        Calcula el porcentaje de descuento aplicado.
        
        Returns:
            Porcentaje de descuento
        """
        original_price = self.product.price * self.quantity
        if original_price == 0:
            return 0.0
        return (self.get_discount_amount() / original_price) * 100
    
    def is_local_sale(self) -> bool:
        """
        Verifica si la venta fue realizada a un cliente local.
        
        Returns:
            True si el cliente es de la misma ciudad que el vendedor
        """
        return self.customer.is_local_customer(self.sales_person.city)
    
    def get_sale_summary(self) -> dict:
        """
        Genera un resumen de la venta con información relevante.
        
        Returns:
            Diccionario con el resumen de la venta
        """
        return {
            "transaction_number": self.transaction_number,
            "date": self.sales_date.strftime("%Y-%m-%d %H:%M:%S"),
            "product": self.product.product_name,
            "quantity": self.quantity,
            "unit_price": self.calculate_unit_price(),
            "total_price": self.total_price,
            "discount_percentage": self.get_discount_percentage(),
            "customer": self.customer.get_full_name(),
            "sales_person": self.sales_person.get_full_name(),
            "is_local_sale": self.is_local_sale()
        } 