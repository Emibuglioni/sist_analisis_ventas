"""
Configuración y fixtures comunes para las pruebas.
"""
from datetime import datetime, date, timedelta
import pytest
from src.models.category import Category
from src.models.country import Country
from src.models.city import City
from src.models.person import Person
from src.models.customer import Customer
from src.models.employee import Employee
from src.models.product import Product
from src.models.sale import Sale
from src.patterns.database_singleton import DatabaseConnection
from typing import List, Dict, Any
import pandas as pd

@pytest.fixture
def sample_country():
    """Fixture que proporciona un país de ejemplo."""
    return Country(
        country_id=1,
        country_name="España",
        country_code="ESP"
    )

@pytest.fixture
def sample_city(sample_country):
    """Fixture que proporciona una ciudad de ejemplo."""
    return City(
        city_id=1,
        city_name="Madrid",
        zipcode="28001",
        country=sample_country
    )

@pytest.fixture
def another_city(sample_country):
    """Fixture que proporciona otra ciudad de ejemplo."""
    return City(
        city_id=2,
        city_name="Barcelona",
        zipcode="08001",
        country=sample_country
    )

@pytest.fixture
def sample_category():
    """Fixture que proporciona una categoría de ejemplo."""
    return Category(
        category_id=1,
        category_name="Electrónica"
    )

@pytest.fixture
def sample_product(sample_category):
    """Fixture que proporciona un producto de ejemplo."""
    return Product(
        product_id=1,
        product_name="Smartphone",
        price=599.99,
        category=sample_category,
        product_class="Premium",
        modify_date=datetime(2024, 1, 1, 12, 0),
        resistant=True,
        is_allergic=False,
        vitality_days=365
    )

@pytest.fixture
def sample_customer(sample_city):
    """Fixture que proporciona un cliente de ejemplo."""
    return Customer(
        customer_id=1,
        first_name="Juan",
        middle_initial="A",
        last_name="García",
        city=sample_city,
        address="Calle Mayor 123"
    )

@pytest.fixture
def sample_employee(sample_city):
    """Fixture que proporciona un empleado de ejemplo."""
    return Employee(
        employee_id=1,
        first_name="María",
        middle_initial="B",
        last_name="López",
        city=sample_city,
        birth_date=date(1990, 5, 15),
        gender="F",
        hire_date=date(2020, 1, 10)
    )

@pytest.fixture
def sample_sale(sample_employee, sample_customer, sample_product):
    """Fixture que proporciona una venta de ejemplo."""
    return Sale(
        sale_id=1,
        sales_person=sample_employee,
        customer=sample_customer,
        product=sample_product,
        quantity=2,
        discount=10.0,
        total_price=1079.98,  # (599.99 * 2) - 10% descuento
        sales_date=datetime(2024, 3, 15, 14, 30),
        transaction_number="TRX-001"
    )

@pytest.fixture
def mock_sales_data() -> List[Sale]:
    """Fixture que proporciona datos de prueba para ventas."""
    category = Category(1, "Electrónicos")
    product = Product(1, "Laptop", 1000.0, category, 50, 10)
    employee = Employee(1, "Juan", "Pérez", "juan@email.com", "Ventas")
    customer = Customer(1, "Ana", "García", "ana@email.com", "Ciudad A")
    
    sales = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(5):
        sale = Sale(
            sale_id=i+1,
            sale_date=base_date + timedelta(days=i),
            product=product,
            customer=customer,
            sales_person=employee,
            quantity=1,
            total_price=1000.0,
            discount=0.0
        )
        sales.append(sale)
    
    return sales

@pytest.fixture
def mock_db_connection(monkeypatch):
    """Fixture que proporciona una conexión mock a la base de datos."""
    class MockCursor:
        def __init__(self, data: List[Dict[str, Any]]):
            self.data = data
            
        def execute(self, query: str, params: Dict[str, Any] = None):
            pass
            
        def fetchall(self):
            return self.data
            
        def close(self):
            pass
    
    class MockConnection:
        def __init__(self):
            self.mock_data = []
            
        def cursor(self, dictionary=True):
            return MockCursor(self.mock_data)
            
        def close(self):
            pass
            
        def set_mock_data(self, data: List[Dict[str, Any]]):
            self.mock_data = data
    
    mock_conn = MockConnection()
    
    def mock_connect(*args, **kwargs):
        return mock_conn
    
    monkeypatch.setattr("mysql.connector.connect", mock_connect)
    
    db = DatabaseConnection()
    db.connect()  # Ya no necesitamos pasar parámetros
    
    return db, mock_conn

@pytest.fixture
def sample_query_results():
    """Fixture que proporciona datos de ejemplo para consultas."""
    return [
        {
            "product_id": 1,
            "product_name": "Laptop",
            "total_sales": 10,
            "total_revenue": 10000.0
        },
        {
            "product_id": 2,
            "product_name": "Smartphone",
            "total_sales": 15,
            "total_revenue": 7500.0
        }
    ] 