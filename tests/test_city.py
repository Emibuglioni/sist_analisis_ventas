"""
Pruebas unitarias para la clase City.
"""
import pytest
from src.models.city import City

def test_city_creation(sample_city, sample_country):
    """Prueba la creación de una ciudad."""
    assert sample_city.city_id == 1
    assert sample_city.city_name == "Madrid"
    assert sample_city.zipcode == "28001"
    assert sample_city.country == sample_country

def test_city_string_representation(sample_city):
    """Prueba la representación en string de una ciudad."""
    assert str(sample_city) == "Madrid, España"

def test_city_to_dict(sample_city):
    """Prueba la conversión de ciudad a diccionario."""
    city_dict = sample_city.to_dict()
    assert city_dict["city_id"] == 1
    assert city_dict["city_name"] == "Madrid"
    assert city_dict["zipcode"] == "28001"
    assert city_dict["country"]["country_name"] == "España"

def test_city_from_dict(sample_country):
    """Prueba la creación de una ciudad desde un diccionario."""
    data = {
        "city_id": 2,
        "city_name": "Barcelona",
        "zipcode": "08001",
        "country": {
            "country_id": 1,
            "country_name": "España",
            "country_code": "ESP"
        }
    }
    city = City.from_dict(data)
    assert city.city_id == 2
    assert city.city_name == "Barcelona"
    assert city.zipcode == "08001"
    assert city.country.country_name == "España"

def test_city_from_dict_with_country_instance(sample_country):
    """Prueba la creación de una ciudad desde un diccionario con instancia de país."""
    data = {
        "city_id": 2,
        "city_name": "Barcelona",
        "zipcode": "08001"
    }
    city = City.from_dict(data, country=sample_country)
    assert city.city_id == 2
    assert city.city_name == "Barcelona"
    assert city.country == sample_country

def test_city_from_dict_without_country():
    """Prueba que se lanza error al crear ciudad sin país."""
    data = {
        "city_id": 2,
        "city_name": "Barcelona",
        "zipcode": "08001"
    }
    with pytest.raises(ValueError):
        City.from_dict(data)

def test_get_full_address(sample_city):
    """Prueba el método get_full_address."""
    assert sample_city.get_full_address() == "Madrid (28001), España"

def test_is_same_country(sample_city, another_city):
    """Prueba el método is_same_country."""
    assert sample_city.is_same_country(another_city) is True

def test_is_same_country_different_countries(sample_city):
    """Prueba is_same_country con ciudades de diferentes países."""
    other_country = City(
        city_id=3,
        city_name="París",
        zipcode="75001",
        country=sample_city.country.__class__(
            country_id=2,
            country_name="Francia",
            country_code="FRA"
        )
    )
    assert sample_city.is_same_country(other_country) is False 