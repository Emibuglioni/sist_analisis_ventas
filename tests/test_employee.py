"""
Pruebas unitarias para la clase Employee.
"""
from datetime import date
import pytest
from src.models.employee import Employee

def test_employee_creation(sample_employee, sample_city):
    """Prueba la creación de un empleado."""
    assert sample_employee.employee_id == 1
    assert sample_employee.first_name == "María"
    assert sample_employee.middle_initial == "B"
    assert sample_employee.last_name == "López"
    assert sample_employee.city == sample_city
    assert sample_employee.birth_date == date(1990, 5, 15)
    assert sample_employee.gender == "F"
    assert sample_employee.hire_date == date(2020, 1, 10)

def test_employee_string_representation(sample_employee):
    """Prueba la representación en string de un empleado."""
    assert str(sample_employee) == "Empleado: María B. López"

def test_employee_to_dict(sample_employee):
    """Prueba la conversión de empleado a diccionario."""
    employee_dict = sample_employee.to_dict()
    assert employee_dict["employee_id"] == 1
    assert employee_dict["first_name"] == "María"
    assert employee_dict["middle_initial"] == "B"
    assert employee_dict["last_name"] == "López"
    assert employee_dict["birth_date"] == "1990-05-15"
    assert employee_dict["gender"] == "F"
    assert employee_dict["hire_date"] == "2020-01-10"
    assert employee_dict["city"]["city_name"] == "Madrid"

def test_employee_from_dict(sample_city):
    """Prueba la creación de un empleado desde un diccionario."""
    data = {
        "employee_id": 2,
        "first_name": "Carlos",
        "last_name": "Ruiz",
        "birth_date": "1985-08-20",
        "gender": "M",
        "hire_date": "2019-03-15",
        "city": {
            "city_id": 1,
            "city_name": "Madrid",
            "zipcode": "28001",
            "country": {
                "country_id": 1,
                "country_name": "España",
                "country_code": "ESP"
            }
        }
    }
    employee = Employee.from_dict(data)
    assert employee.employee_id == 2
    assert employee.first_name == "Carlos"
    assert employee.last_name == "Ruiz"
    assert employee.birth_date == date(1985, 8, 20)
    assert employee.gender == "M"
    assert employee.hire_date == date(2019, 3, 15)

def test_calculate_age(sample_employee):
    """Prueba el cálculo de edad del empleado."""
    # Antes del cumpleaños
    reference_date = date(2024, 5, 14)
    assert sample_employee.calculate_age(reference_date) == 33
    
    # En el cumpleaños
    reference_date = date(2024, 5, 15)
    assert sample_employee.calculate_age(reference_date) == 34
    
    # Después del cumpleaños
    reference_date = date(2024, 5, 16)
    assert sample_employee.calculate_age(reference_date) == 34

def test_calculate_seniority(sample_employee):
    """Prueba el cálculo de antigüedad del empleado."""
    # Antes del aniversario
    reference_date = date(2024, 1, 9)
    assert sample_employee.calculate_seniority(reference_date) == 3
    
    # En el aniversario
    reference_date = date(2024, 1, 10)
    assert sample_employee.calculate_seniority(reference_date) == 4
    
    # Después del aniversario
    reference_date = date(2024, 1, 11)
    assert sample_employee.calculate_seniority(reference_date) == 4

def test_is_birthday(sample_employee):
    """Prueba la verificación de cumpleaños."""
    # No es cumpleaños
    reference_date = date(2024, 5, 14)
    assert sample_employee.is_birthday(reference_date) is False
    
    # Es cumpleaños
    reference_date = date(2024, 5, 15)
    assert sample_employee.is_birthday(reference_date) is True
    
    # Mismo día, diferente mes
    reference_date = date(2024, 6, 15)
    assert sample_employee.is_birthday(reference_date) is False 