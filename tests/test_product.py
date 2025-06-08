"""
Pruebas unitarias para la clase Product.
"""
from datetime import datetime, timedelta
import pytest
from src.models.product import Product

def test_product_creation(sample_product, sample_category):
    """Prueba la creación de un producto."""
    assert sample_product.product_id == 1
    assert sample_product.product_name == "Smartphone"
    assert sample_product.price == 599.99
    assert sample_product.category == sample_category
    assert sample_product.product_class == "Premium"
    assert sample_product.resistant is True
    assert sample_product.is_allergic is False
    assert sample_product.vitality_days == 365

def test_product_string_representation(sample_product):
    """Prueba la representación en string de un producto."""
    assert str(sample_product) == "Smartphone - Electrónica ($599.99)"

def test_product_to_dict(sample_product):
    """Prueba la conversión de producto a diccionario."""
    product_dict = sample_product.to_dict()
    assert product_dict["product_id"] == 1
    assert product_dict["product_name"] == "Smartphone"
    assert product_dict["price"] == 599.99
    assert product_dict["category"]["category_name"] == "Electrónica"
    assert product_dict["product_class"] == "Premium"
    assert product_dict["resistant"] is True
    assert product_dict["is_allergic"] is False
    assert product_dict["vitality_days"] == 365

def test_product_from_dict(sample_category):
    """Prueba la creación de un producto desde un diccionario."""
    data = {
        "product_id": 2,
        "product_name": "Tablet",
        "price": 299.99,
        "category": {
            "category_id": 1,
            "category_name": "Electrónica"
        },
        "product_class": "Standard",
        "modify_date": "2024-01-01T12:00:00",
        "resistant": False,
        "is_allergic": False,
        "vitality_days": 180
    }
    product = Product.from_dict(data)
    assert product.product_id == 2
    assert product.product_name == "Tablet"
    assert product.price == 299.99
    assert product.category.category_name == "Electrónica"

def test_calculate_discount_price(sample_product):
    """Prueba el cálculo de precio con descuento."""
    # 20% de descuento sobre 599.99
    assert sample_product.calculate_discount_price(20) == pytest.approx(479.992)

def test_calculate_discount_price_invalid_percentage(sample_product):
    """Prueba que se lanza error con porcentaje de descuento inválido."""
    with pytest.raises(ValueError):
        sample_product.calculate_discount_price(150)
    with pytest.raises(ValueError):
        sample_product.calculate_discount_price(-10)

def test_is_expired(sample_product):
    """Prueba la verificación de expiración del producto."""
    # Producto no expirado (dentro del período de vitalidad)
    current_date = sample_product.modify_date + timedelta(days=364)
    assert sample_product.is_expired(current_date) is False
    
    # Producto expirado (fuera del período de vitalidad)
    future_date = sample_product.modify_date + timedelta(days=366)
    assert sample_product.is_expired(future_date) is True

def test_get_storage_instructions(sample_product):
    """Prueba la generación de instrucciones de almacenamiento."""
    instructions = sample_product.get_storage_instructions()
    assert "Producto resistente - Almacenamiento estándar" in instructions
    assert "Vida útil: 365 días desde fabricación" in instructions
    assert "¡PRECAUCIÓN! Producto alergénico" not in instructions

def test_get_storage_instructions_allergic(sample_category):
    """Prueba las instrucciones de almacenamiento para producto alérgico."""
    product = Product(
        product_id=3,
        product_name="Nueces",
        price=9.99,
        category=sample_category,
        product_class="Food",
        modify_date=datetime.now(),
        resistant=False,
        is_allergic=True,
        vitality_days=90
    )
    instructions = product.get_storage_instructions()
    assert "¡PRECAUCIÓN! Producto alergénico" in instructions
    assert "Producto delicado - Requiere almacenamiento especial" in instructions
    assert "Vida útil: 90 días desde fabricación" in instructions 