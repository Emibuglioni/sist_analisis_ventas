"""
Pruebas unitarias para los patrones de diseño implementados.
"""
import pytest
from datetime import datetime, timedelta
import pandas as pd
from src.patterns.database_singleton import DatabaseConnection
from src.patterns.query_builder import SQLQueryBuilder, SalesQueryBuilder
from src.patterns.report_factory import ReportFactory

class TestSingletonPattern:
    """Pruebas para el patrón Singleton de conexión a base de datos."""
    
    def test_singleton_instance(self):
        """Verifica que se obtiene la misma instancia."""
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2
    
    def test_connection_management(self, mock_db_connection):
        """Prueba la gestión de la conexión."""
        db, _ = mock_db_connection
        
        # Verificar conexión
        connection = db.get_connection()
        assert connection is not None
        
        # Cerrar conexión
        db.close()
        
        with pytest.raises(RuntimeError):
            db.get_connection()

    def test_query_execution(self, mock_db_connection, sample_query_results):
        """Prueba la ejecución de consultas y conversión a DataFrame."""
        db, mock_conn = mock_db_connection
        mock_conn.set_mock_data(sample_query_results)
        
        df = db.execute_query("SELECT * FROM products")
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_query_results)
        assert "product_name" in df.columns
        assert "total_revenue" in df.columns

class TestBuilderPattern:
    """Pruebas para el patrón Builder de consultas SQL."""
    
    def test_basic_query_builder(self):
        """Prueba la construcción básica de consultas."""
        builder = SQLQueryBuilder()
        query, params = (
            builder
            .select("product_id", "product_name")
            .from_table("products")
            .where("category_id = :category", {"category": 1})
            .build()
        )
        
        assert "SELECT product_id, product_name" in query
        assert "FROM products" in query
        assert "WHERE category_id = :category" in query
        assert params["category"] == 1
    
    def test_complex_query_builder(self):
        """Prueba la construcción de consultas complejas."""
        builder = SQLQueryBuilder()
        query, params = (
            builder
            .select("p.product_id", "p.product_name", "COUNT(*) as total_sales")
            .from_table("products p")
            .join("sales s", "s.product_id = p.product_id")
            .where("s.sale_date >= :start_date", {"start_date": "2024-01-01"})
            .group_by("p.product_id", "p.product_name")
            .having("total_sales > 10")
            .order_by("total_sales", "DESC")
            .limit(5)
            .build()
        )
        
        assert "SELECT p.product_id, p.product_name, COUNT(*) as total_sales" in query
        assert "FROM products p" in query
        assert "INNER JOIN sales s ON s.product_id = p.product_id" in query
        assert "WHERE s.sale_date >= :start_date" in query
        assert "GROUP BY p.product_id, p.product_name" in query
        assert "HAVING total_sales > 10" in query
        assert "ORDER BY total_sales DESC" in query
        assert "LIMIT 5" in query
        assert params["start_date"] == "2024-01-01"
    
    def test_sales_query_builder(self):
        """Prueba el builder especializado para consultas de ventas."""
        builder = SalesQueryBuilder()
        start_date = datetime.now() - timedelta(days=30)
        query, params = (
            builder
            .with_date_range(start_date, datetime.now())
            .with_product_category(1)
            .group_by_product()
            .build()
        )
        
        assert "FROM sales" in query
        assert "JOIN products p" in query
        assert "sale_date BETWEEN :start_date AND :end_date" in query
        assert "category_id = :category_id" in query
        assert params["category_id"] == 1
        assert "start_date" in params
        assert "end_date" in params

class TestFactoryPattern:
    """Pruebas para el patrón Factory de reportes."""
    
    def test_sales_report_creation(self, mock_sales_data):
        """Prueba la creación y generación de reportes de ventas."""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = ReportFactory.create_report(
            "sales",
            mock_sales_data,
            start_date=start_date,
            end_date=end_date
        )
        
        result = report.generate()
        
        assert result["tipo"] == "Reporte de Ventas"
        assert "periodo" in result
        assert "metricas" in result
        assert result["metricas"]["total_ventas"] == len(mock_sales_data)
    
    def test_product_report_creation(self, mock_sales_data):
        """Prueba la creación y generación de reportes de productos."""
        report = ReportFactory.create_report("product", mock_sales_data)
        result = report.generate()
        
        assert result["tipo"] == "Reporte de Productos"
        assert "productos_top" in result
        assert "total_productos" in result
    
    def test_employee_report_creation(self, mock_sales_data):
        """Prueba la creación y generación de reportes de empleados."""
        report = ReportFactory.create_report("employee", mock_sales_data)
        result = report.generate()
        
        assert result["tipo"] == "Reporte de Empleados"
        assert "empleados" in result
        assert "total_empleados" in result
    
    def test_invalid_report_type(self, mock_sales_data):
        """Prueba el manejo de tipos de reporte inválidos."""
        with pytest.raises(ValueError):
            ReportFactory.create_report("invalid_type", mock_sales_data)

def test_patterns_integration(mock_db_connection, sample_query_results):
    """Prueba la integración entre los diferentes patrones."""
    db, mock_conn = mock_db_connection
    mock_conn.set_mock_data(sample_query_results)
    
    # Usar Builder para construir consulta
    query_builder = SalesQueryBuilder()
    query, params = (
        query_builder
        .group_by_product()
        .build()
    )
    
    # Ejecutar consulta usando Singleton
    df = db.execute_query(query, params)
    
    # Crear reporte usando Factory
    report = ReportFactory.create_report("product", df.to_dict('records'))
    result = report.generate()
    
    assert isinstance(df, pd.DataFrame)
    assert result["tipo"] == "Reporte de Productos"
    assert len(result["productos_top"]) > 0 