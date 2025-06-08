"""
Implementación del patrón Builder para construir consultas SQL complejas.
"""
from typing import List, Optional, Any, Dict, Tuple
from datetime import datetime

class SQLQueryBuilder:
    """
    Builder para construir consultas SQL de manera flexible y segura.
    Permite construir consultas complejas paso a paso, evitando errores de sintaxis.
    """
    
    def __init__(self):
        self._select_columns: List[str] = []
        self._from_table: str = ""
        self._joins: List[str] = []
        self._where_conditions: List[str] = []
        self._group_by: List[str] = []
        self._having: List[str] = []
        self._order_by: List[str] = []
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._parameters: List[Any] = []
    
    def select(self, *columns: str) -> 'SQLQueryBuilder':
        """Agrega columnas al SELECT."""
        self._select_columns.extend(columns)
        return self
    
    def from_table(self, table: str) -> 'SQLQueryBuilder':
        """Establece la tabla principal."""
        self._from_table = table
        return self
    
    def join(self, table: str, condition: str, join_type: str = "INNER") -> 'SQLQueryBuilder':
        """Agrega una cláusula JOIN."""
        # Reemplazar los marcadores de posición con %s
        condition = self._convert_named_params(condition)
        join_clause = f"{join_type} JOIN {table} ON {condition}"
        self._joins.append(join_clause)
        return self
    
    def where(self, condition: str, parameters: Dict[str, Any] = None) -> 'SQLQueryBuilder':
        """
        Agrega una condición WHERE.
        
        Args:
            condition: Condición SQL usando %s como placeholder
            parameters: Diccionario de parámetros para la condición
        """
        # Reemplazar los marcadores de posición con %s
        condition = self._convert_named_params(condition)
        self._where_conditions.append(condition)
        if parameters:
            self._parameters.extend(parameters.values())
        return self
    
    def group_by(self, *columns: str) -> 'SQLQueryBuilder':
        """Agrega columnas al GROUP BY."""
        self._group_by.extend(columns)
        return self
    
    def having(self, condition: str) -> 'SQLQueryBuilder':
        """Agrega una condición HAVING."""
        # Reemplazar los marcadores de posición con %s
        condition = self._convert_named_params(condition)
        self._having.append(condition)
        return self
    
    def order_by(self, column: str, direction: str = "ASC") -> 'SQLQueryBuilder':
        """Agrega una columna al ORDER BY."""
        self._order_by.append(f"{column} {direction}")
        return self
    
    def limit(self, limit: int) -> 'SQLQueryBuilder':
        """Establece el LIMIT."""
        self._limit = limit
        return self
    
    def offset(self, offset: int) -> 'SQLQueryBuilder':
        """Establece el OFFSET."""
        self._offset = offset
        return self
    
    def _convert_named_params(self, condition: str) -> str:
        """
        Convierte los marcadores de posición con nombre a %s.
        
        Args:
            condition: Condición SQL con marcadores de posición con nombre
            
        Returns:
            Condición con marcadores %s
        """
        import re
        # Buscar todos los marcadores de posición con nombre (:nombre)
        named_params = re.findall(r':(\w+)', condition)
        # Reemplazar cada uno con %s
        result = condition
        for param in named_params:
            result = result.replace(f":{param}", "%s")
        return result
    
    def build(self) -> Tuple[str, List[Any]]:
        """
        Construye la consulta SQL y retorna también los parámetros.
        
        Returns:
            Tupla con la consulta SQL y lista de parámetros
        """
        query_parts = []
        
        # SELECT
        select_clause = "SELECT " + (", ".join(self._select_columns) if self._select_columns else "*")
        query_parts.append(select_clause)
        
        # FROM
        query_parts.append(f"FROM {self._from_table}")
        
        # JOINs
        if self._joins:
            query_parts.extend(self._joins)
        
        # WHERE
        if self._where_conditions:
            query_parts.append("WHERE " + " AND ".join(self._where_conditions))
        
        # GROUP BY
        if self._group_by:
            query_parts.append("GROUP BY " + ", ".join(self._group_by))
        
        # HAVING
        if self._having:
            query_parts.append("HAVING " + " AND ".join(self._having))
        
        # ORDER BY
        if self._order_by:
            query_parts.append("ORDER BY " + ", ".join(self._order_by))
        
        # LIMIT y OFFSET
        if self._limit is not None:
            query_parts.append(f"LIMIT {self._limit}")
            if self._offset is not None:
                query_parts.append(f"OFFSET {self._offset}")
        
        return " ".join(query_parts), self._parameters

class SalesQueryBuilder:
    """
    Builder especializado para consultas relacionadas con ventas.
    Proporciona métodos de alto nivel para construir consultas comunes de ventas.
    """
    
    def __init__(self):
        self._builder = SQLQueryBuilder()
        self._builder.from_table("sales")
    
    def with_date_range(self, start_date: datetime, end_date: datetime) -> 'SalesQueryBuilder':
        """Filtra ventas por rango de fechas."""
        self._builder.where(
            "SalesDate BETWEEN %s AND %s",
            {"start_date": start_date, "end_date": end_date}
        )
        return self
    
    def with_product_category(self, category_id: int) -> 'SalesQueryBuilder':
        """Filtra ventas por categoría de producto."""
        self._builder.join("products p", "sales.ProductID = p.ProductID")
        self._builder.where("p.CategoryID = %s", {"category_id": category_id})
        return self
    
    def with_employee(self, employee_id: int) -> 'SalesQueryBuilder':
        """Filtra ventas por empleado."""
        self._builder.where("SalesPersonID = %s", {"employee_id": employee_id})
        return self
    
    def with_customer(self, customer_id: int) -> 'SalesQueryBuilder':
        """Filtra ventas por cliente."""
        self._builder.where("CustomerID = %s", {"customer_id": customer_id})
        return self
    
    def group_by_product(self) -> 'SalesQueryBuilder':
        """Agrupa resultados por producto."""
        self._builder.select(
            "p.ProductID",
            "p.ProductName",
            "COUNT(*) as total_sales",
            "SUM(Quantity) as total_quantity",
            "SUM(TotalPrice) as total_revenue"
        )
        self._builder.join("products p", "sales.ProductID = p.ProductID")
        self._builder.group_by("p.ProductID", "p.ProductName")
        return self
    
    def group_by_employee(self) -> 'SalesQueryBuilder':
        """Agrupa resultados por empleado."""
        self._builder.select(
            "e.EmployeeID",
            "e.FirstName",
            "e.LastName", 
            "COUNT(*) as total_sales",
            "SUM(TotalPrice) as total_revenue"
        )
        self._builder.join("employees e", "sales.SalesPersonID = e.EmployeeID")
        self._builder.group_by("e.EmployeeID", "e.FirstName", "e.LastName")
        return self
    
    def build(self) -> Tuple[str, List[Any]]:
        """
        Construye la consulta SQL final.
        
        Returns:
            Tupla con la consulta SQL y lista de parámetros
        """
        return self._builder.build() 