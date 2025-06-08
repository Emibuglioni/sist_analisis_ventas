"""
Pruebas unitarias para la clase Sale.
"""
from datetime import datetime
import pytest
from src.models.sale import Sale

def test_sale_creation(sample_sale, sample_employee, sample_customer, sample_product):
    """Prueba la creación de una venta."""
    assert sample_sale.sale_id == 1
    assert sample_sale.sales_person == sample_employee
    assert sample_sale.customer == sample_customer
    assert sample_sale.product == sample_product
    assert sample_sale.quantity == 2
    assert sample_sale.discount == 10.0
    assert sample_sale.total_price == 1079.98
    assert sample_sale.transaction_number == "TRX-001"

def test_sale_string_representation(sample_sale):
    """Prueba la representación en string de una venta."""
    assert str(sample_sale) == "Venta #1 - TRX-001"

def test_sale_to_dict(sample_sale):
    """Prueba la conversión de venta a diccionario."""
    sale_dict = sample_sale.to_dict()
    assert sale_dict["sale_id"] == 1
    assert sale_dict["sales_person"]["first_name"] == "María"
    assert sale_dict["customer"]["first_name"] == "Juan"
    assert sale_dict["product"]["product_name"] == "Smartphone"
    assert sale_dict["quantity"] == 2
    assert sale_dict["discount"] == 10.0
    assert sale_dict["total_price"] == 1079.98
    assert sale_dict["transaction_number"] == "TRX-001"

def test_sale_from_dict(sample_employee, sample_customer, sample_product):
    """Prueba la creación de una venta desde un diccionario."""
    data = {
        "sale_id": 2,
        "sales_person": sample_employee.to_dict(),
        "customer": sample_customer.to_dict(),
        "product": sample_product.to_dict(),
        "quantity": 1,
        "discount": 5.0,
        "total_price": 569.99,
        "sales_date": "2024-03-16T10:30:00",
        "transaction_number": "TRX-002"
    }
    sale = Sale.from_dict(data)
    assert sale.sale_id == 2
    assert sale.quantity == 1
    assert sale.discount == 5.0
    assert sale.total_price == 569.99
    assert sale.transaction_number == "TRX-002"

def test_calculate_unit_price(sample_sale):
    """Prueba el cálculo del precio unitario."""
    # total_price = 1079.98, quantity = 2
    assert sample_sale.calculate_unit_price() == pytest.approx(539.99)

def test_get_discount_amount(sample_sale):
    """Prueba el cálculo del monto de descuento."""
    # Precio original: 599.99 * 2 = 1199.98
    # Precio con descuento: 1079.98
    # Descuento: 120.00
    assert sample_sale.get_discount_amount() == pytest.approx(120.00)

def test_get_discount_percentage(sample_sale):
    """Prueba el cálculo del porcentaje de descuento."""
    # Precio original: 599.99 * 2 = 1199.98
    # Precio con descuento: 1079.98
    # Porcentaje de descuento: 10%
    assert sample_sale.get_discount_percentage() == pytest.approx(10.0)

def test_get_discount_percentage_zero_price():
    """Prueba el cálculo del porcentaje de descuento con precio cero."""
    sale = Sale(
        sale_id=3,
        sales_person=sample_sale.sales_person,
        customer=sample_sale.customer,
        product=sample_sale.product,
        quantity=0,
        discount=0,
        total_price=0,
        sales_date=datetime.now(),
        transaction_number="TRX-003"
    )
    assert sale.get_discount_percentage() == 0.0

def test_is_local_sale(sample_sale):
    """Prueba la verificación de venta local."""
    # Cliente y vendedor en la misma ciudad
    assert sample_sale.is_local_sale() is True

def test_is_local_sale_different_cities(sample_sale, another_city):
    """Prueba la verificación de venta local con diferentes ciudades."""
    # Modificar la ciudad del cliente
    sample_sale.customer.city = another_city
    assert sample_sale.is_local_sale() is False

def test_get_sale_summary(sample_sale):
    """Prueba la generación del resumen de venta."""
    summary = sample_sale.get_sale_summary()
    assert summary["transaction_number"] == "TRX-001"
    assert summary["product"] == "Smartphone"
    assert summary["quantity"] == 2
    assert summary["unit_price"] == pytest.approx(539.99)
    assert summary["total_price"] == 1079.98
    assert summary["discount_percentage"] == pytest.approx(10.0)
    assert summary["customer"] == "Juan A. García"
    assert summary["sales_person"] == "María B. López"
    assert summary["is_local_sale"] is True 