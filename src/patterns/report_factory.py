"""
Implementación del patrón Factory Method para la creación de reportes.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

class Report(ABC):
    """Clase base abstracta para todos los tipos de reportes."""
    
    @abstractmethod
    def generate(self) -> Dict[str, Any]:
        """
        Genera el reporte.
        
        Returns:
            Diccionario con los datos del reporte
        """
        pass

class SalesReport(Report):
    """Reporte de ventas."""
    
    def __init__(self, sales_data: List[Dict], start_date: datetime, end_date: datetime):
        self.sales_data = sales_data
        self.start_date = start_date
        self.end_date = end_date
    
    def generate(self) -> Dict[str, Any]:
        """Genera un reporte de ventas con métricas clave."""
        total_sales = len(self.sales_data)
        total_revenue = sum(sale.get('total_revenue', 0) for sale in self.sales_data)
        
        return {
            "tipo": "Reporte de Ventas",
            "periodo": {
                "inicio": self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "fin": self.end_date.strftime("%Y-%m-%d %H:%M:%S")
            },
            "metricas": {
                "total_ventas": total_sales,
                "ingresos_totales": total_revenue,
                "productos_unicos": len(set(sale.get('ProductID', 0) for sale in self.sales_data))
            }
        }

class ProductReport(Report):
    """Reporte de productos."""
    
    def __init__(self, sales_data: List[Dict]):
        self.sales_data = sales_data
    
    def generate(self) -> Dict[str, Any]:
        """Genera un reporte de productos más vendidos y rentables."""
        # Los datos ya vienen agrupados por producto de la consulta SQL
        top_products = [
            {
                "producto_id": sale.get('ProductID', 0),
                "nombre": sale.get('ProductName', ''),
                "cantidad_vendida": sale.get('total_quantity', 0),
                "ingresos_totales": sale.get('total_revenue', 0)
            }
            for sale in self.sales_data
        ]
        
        # Ordenar productos por ingresos
        top_products.sort(key=lambda x: x["ingresos_totales"], reverse=True)
        
        return {
            "tipo": "Reporte de Productos",
            "productos_top": top_products[:10],  # Top 10 productos
            "total_productos": len(self.sales_data)
        }

class EmployeeReport(Report):
    """Reporte de empleados."""
    
    def __init__(self, sales_data: List[Dict]):
        self.sales_data = sales_data
    
    def generate(self) -> Dict[str, Any]:
        """Genera un reporte de desempeño de empleados."""
        # Los datos ya vienen agrupados por empleado de la consulta SQL
        employee_metrics = [
            {
                "empleado_id": sale.get('EmployeeID', 0),
                "nombre": f"{sale.get('FirstName', '')} {sale.get('LastName', '')}",
                "ventas_totales": sale.get('total_sales', 0),
                "ingresos_generados": sale.get('total_revenue', 0)
            }
            for sale in self.sales_data
        ]
        
        return {
            "tipo": "Reporte de Empleados",
            "empleados": employee_metrics,
            "total_empleados": len(self.sales_data)
        }

class ReportFactory:
    """
    Factory Method para crear diferentes tipos de reportes.
    Centraliza la lógica de creación de reportes y facilita la adición de nuevos tipos.
    """
    
    @staticmethod
    def create_report(report_type: str, sales_data: List[Dict], **kwargs) -> Report:
        """
        Crea un reporte del tipo especificado.
        
        Args:
            report_type: Tipo de reporte a crear
            sales_data: Lista de diccionarios con datos de ventas
            **kwargs: Argumentos adicionales específicos del tipo de reporte
            
        Returns:
            Instancia del reporte solicitado
            
        Raises:
            ValueError: Si el tipo de reporte no es válido
        """
        if report_type == "sales":
            start_date = kwargs.get("start_date", datetime.min)
            end_date = kwargs.get("end_date", datetime.max)
            return SalesReport(sales_data, start_date, end_date)
        elif report_type == "product":
            return ProductReport(sales_data)
        elif report_type == "employee":
            return EmployeeReport(sales_data)
        else:
            raise ValueError(f"Tipo de reporte no válido: {report_type}") 