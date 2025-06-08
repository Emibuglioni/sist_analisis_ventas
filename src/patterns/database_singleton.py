"""
Implementación del patrón Singleton para la conexión a la base de datos.
"""
from typing import Optional, Dict, Any, List, Union
import pandas as pd
from datetime import datetime
from mysql.connector import MySQLConnection
import mysql.connector
from src.patterns.query_builder import SalesQueryBuilder
from src.config import Config

class DatabaseConnection:
    """
    Singleton que maneja la conexión a la base de datos.
    Garantiza una única instancia de conexión en toda la aplicación.
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[MySQLConnection] = None
    
    def __new__(cls) -> 'DatabaseConnection':
        """Crea o retorna la única instancia de DatabaseConnection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Inicializa la conexión si no existe."""
        if self._connection is None:
            self._connection = None  # Se inicializará en connect()
    
    def connect(self) -> None:
        """
        Establece la conexión a la base de datos usando la configuración.
        """
        if self._connection is None:
            params = Config.DB.get_connection_params()
            self._connection = mysql.connector.connect(**params)
    
    def get_connection(self) -> MySQLConnection:
        """
        Retorna la conexión activa a la base de datos.
        
        Returns:
            Conexión a la base de datos
            
        Raises:
            RuntimeError: Si la conexión no ha sido establecida
        """
        if self._connection is None:
            raise RuntimeError("La conexión a la base de datos no ha sido establecida")
        return self._connection
    
    def close(self) -> None:
        """Cierra la conexión a la base de datos si existe."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute_query(self, query: str, params: Union[List[Any], Dict[str, Any], None] = None) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL y retorna los resultados como DataFrame.
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (lista o diccionario)
            
        Returns:
            DataFrame con los resultados
        """
        cursor = self._connection.cursor(dictionary=True)
        
        try:
            # Si los parámetros son un diccionario, convertirlos a lista
            if isinstance(params, dict):
                params = list(params.values())
            
            # Ejecutar la consulta
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return pd.DataFrame(results)
            
        finally:
            cursor.close()

    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Obtiene las ventas en un rango de fechas.
        
        Args:
            start_date: Fecha inicial
            end_date: Fecha final
            
        Returns:
            DataFrame con las ventas del período
        """
        query_builder = SalesQueryBuilder()
        query, params = (
            query_builder
            .with_date_range(start_date, end_date)
            .build()
        )
        return self.execute_query(query, params)

    def get_top_selling_products(self, limit: int = 10) -> pd.DataFrame:
        """
        Obtiene los productos más vendidos.
        
        Args:
            limit: Cantidad de productos a retornar
            
        Returns:
            DataFrame con los productos más vendidos
        """
        query_builder = SalesQueryBuilder()
        query, params = (
            query_builder
            .group_by_product()
            .build()
        )
        df = self.execute_query(query, params)
        return df.nlargest(limit, 'total_revenue')

    def get_employee_performance(self, start_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Obtiene el desempeño de los empleados.
        
        Args:
            start_date: Fecha desde la cual analizar (opcional)
            
        Returns:
            DataFrame con métricas de desempeño por empleado
        """
        query_builder = SalesQueryBuilder()
        builder = query_builder.group_by_employee()
        
        if start_date:
            builder.with_date_range(start_date, datetime.now())
            
        query, params = builder.build()
        df = self.execute_query(query, params)
        
        # Calcular métricas adicionales
        if not df.empty:
            df['promedio_venta'] = df['total_revenue'] / df['total_sales']
            
        return df.sort_values('total_revenue', ascending=False)

    def get_sales_by_category(self, start_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Obtiene las ventas agrupadas por categoría de producto.
        
        Args:
            start_date: Fecha desde la cual analizar (opcional)
            
        Returns:
            DataFrame con ventas por categoría
        """
        query = """
        SELECT 
            c.category_id,
            c.category_name,
            COUNT(*) as total_sales,
            SUM(s.quantity) as total_quantity,
            SUM(s.total_price) as total_revenue,
            AVG(s.total_price) as avg_sale_value
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        WHERE 1=1
        """
        params = {}
        
        if start_date:
            query += " AND s.sale_date >= :start_date"
            params['start_date'] = start_date
            
        query += """
        GROUP BY c.category_id, c.category_name
        ORDER BY total_revenue DESC
        """
        
        return self.execute_query(query, params)

    def get_customer_insights(self, min_purchases: int = 1) -> pd.DataFrame:
        """
        Obtiene insights sobre los clientes.
        
        Args:
            min_purchases: Número mínimo de compras para incluir al cliente
            
        Returns:
            DataFrame con métricas por cliente
        """
        query = """
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            COUNT(*) as total_purchases,
            SUM(s.total_price) as total_spent,
            AVG(s.total_price) as avg_purchase_value,
            MIN(s.sale_date) as first_purchase,
            MAX(s.sale_date) as last_purchase
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        HAVING total_purchases >= :min_purchases
        ORDER BY total_spent DESC
        """
        
        df = self.execute_query(query, {'min_purchases': min_purchases})
        
        if not df.empty:
            # Calcular días desde la última compra
            df['days_since_last_purchase'] = (datetime.now() - pd.to_datetime(df['last_purchase'])).dt.days
            # Calcular frecuencia de compra (días entre primera y última compra / número de compras)
            df['purchase_frequency_days'] = (
                (pd.to_datetime(df['last_purchase']) - pd.to_datetime(df['first_purchase'])).dt.days / 
                df['total_purchases']
            )
            
        return df

    def get_inventory_status(self) -> pd.DataFrame:
        """
        Obtiene el estado actual del inventario.
        
        Returns:
            DataFrame con el estado del inventario
        """
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            c.category_name,
            p.unit_price,
            p.stock_quantity,
            p.reorder_level,
            CASE 
                WHEN p.stock_quantity <= p.reorder_level THEN 'Reordenar'
                WHEN p.stock_quantity <= p.reorder_level * 2 THEN 'Stock Bajo'
                ELSE 'OK'
            END as stock_status,
            COALESCE(
                (SELECT SUM(quantity) 
                FROM sales 
                WHERE product_id = p.product_id 
                AND sale_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)),
                0
            ) as sales_last_30_days
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY stock_status DESC, sales_last_30_days DESC
        """
        
        df = self.execute_query(query)
        
        if not df.empty:
            # Calcular días estimados de inventario basado en ventas recientes
            df['estimated_days_of_stock'] = df.apply(
                lambda row: float('inf') if row['sales_last_30_days'] == 0 
                else (row['stock_quantity'] / (row['sales_last_30_days'] / 30)),
                axis=1
            )
            
        return df 