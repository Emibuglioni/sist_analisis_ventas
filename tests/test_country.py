"""
Pruebas unitarias para la clase Country.
"""
import pytest
from src.models.country import Country

def test_country_creation(sample_country):
    """Prueba la creación de un país."""
    assert sample_country.country_id == 1
    assert sample_country.country_name == "España"
    assert sample_country.country_code == "ESP"

def test_country_string_representation(sample_country):
    """Prueba la representación en string de un país."""
    assert str(sample_country) == "España (ESP)"

def test_country_to_dict(sample_country):
    """Prueba la conversión de país a diccionario."""
    country_dict = sample_country.to_dict()
    assert country_dict["country_id"] == 1
    assert country_dict["country_name"] == "España"
    assert country_dict["country_code"] == "ESP"

def test_country_from_dict():
    """Prueba la creación de un país desde un diccionario."""
    data = {
        "country_id": 2,
        "country_name": "Francia",
        "country_code": "FRA"
    }
    country = Country.from_dict(data)
    assert country.country_id == 2
    assert country.country_name == "Francia"
    assert country.country_code == "FRA"

def test_get_formatted_code(sample_country):
    """Prueba el método get_formatted_code."""
    assert sample_country.get_formatted_code() == "ESP"

def test_get_formatted_code_lowercase():
    """Prueba get_formatted_code con código en minúsculas."""
    country = Country(country_id=3, country_name="Italia", country_code="ita")
    assert country.get_formatted_code() == "ITA" 