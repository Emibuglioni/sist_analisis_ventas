"""
Módulo que contiene la clase Employee para el manejo de empleados.
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from .person import Person
from .city import City

@dataclass
class Employee(Person):
    """Clase que representa un empleado."""
    
    employee_id: int
    birth_date: date
    gender: str
    hire_date: date
    
    def __str__(self) -> str:
        """Retorna una representación en string del empleado."""
        return f"Empleado: {super().__str__()}"
    
    def to_dict(self) -> dict:
        """Convierte la instancia a un diccionario."""
        base_dict = super().to_dict()
        base_dict.update({
            "employee_id": self.employee_id,
            "birth_date": self.birth_date.isoformat(),
            "gender": self.gender,
            "hire_date": self.hire_date.isoformat()
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: dict, city: Optional[City] = None) -> 'Employee':
        """
        Crea una instancia de Employee a partir de un diccionario.
        
        Args:
            data: Diccionario con los datos del empleado
            city: Instancia opcional de City. Si no se proporciona,
                 se creará a partir de los datos del diccionario
            
        Returns:
            Nueva instancia de Employee
        """
        if city is None and "city" in data:
            city = City.from_dict(data["city"])
        elif city is None:
            raise ValueError("Se requiere una instancia de City o datos de city en el diccionario")
            
        return cls(
            employee_id=data["employee_id"],
            first_name=data["first_name"],
            middle_initial=data.get("middle_initial"),
            last_name=data["last_name"],
            city=city,
            birth_date=date.fromisoformat(data["birth_date"]) if isinstance(data["birth_date"], str) else data["birth_date"],
            gender=data["gender"],
            hire_date=date.fromisoformat(data["hire_date"]) if isinstance(data["hire_date"], str) else data["hire_date"]
        )
    
    def calculate_age(self, reference_date: Optional[date] = None) -> int:
        """
        Calcula la edad del empleado.
        
        Args:
            reference_date: Fecha de referencia para el cálculo. Si no se proporciona,
                          se usa la fecha actual
            
        Returns:
            Edad en años
        """
        if reference_date is None:
            reference_date = date.today()
            
        age = reference_date.year - self.birth_date.year
        
        # Ajustar si aún no ha llegado el cumpleaños este año
        if reference_date.month < self.birth_date.month or \
           (reference_date.month == self.birth_date.month and reference_date.day < self.birth_date.day):
            age -= 1
            
        return age
    
    def calculate_seniority(self, reference_date: Optional[date] = None) -> int:
        """
        Calcula los años de antigüedad del empleado.
        
        Args:
            reference_date: Fecha de referencia para el cálculo. Si no se proporciona,
                          se usa la fecha actual
            
        Returns:
            Años de antigüedad
        """
        if reference_date is None:
            reference_date = date.today()
            
        years = reference_date.year - self.hire_date.year
        
        # Ajustar si aún no ha llegado el aniversario este año
        if reference_date.month < self.hire_date.month or \
           (reference_date.month == self.hire_date.month and reference_date.day < self.hire_date.day):
            years -= 1
            
        return years
    
    def is_birthday(self, reference_date: Optional[date] = None) -> bool:
        """
        Verifica si es el cumpleaños del empleado.
        
        Args:
            reference_date: Fecha de referencia para la verificación. Si no se proporciona,
                          se usa la fecha actual
            
        Returns:
            True si es el cumpleaños del empleado
        """
        if reference_date is None:
            reference_date = date.today()
            
        return (reference_date.month == self.birth_date.month and 
                reference_date.day == self.birth_date.day) 