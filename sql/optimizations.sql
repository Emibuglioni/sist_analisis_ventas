-- Optimizaciones de rendimiento para la base de datos ventas_db
USE ventas_db;

-- 1. Índices para mejorar búsquedas frecuentes
-- Índice para búsquedas por fecha en ventas
CREATE INDEX idx_sales_date ON sales(SalesDate);

-- Índice compuesto para análisis de ventas por producto y fecha
CREATE INDEX idx_sales_product_date ON sales(ProductID, SalesDate);

-- Índice para búsquedas de productos por categoría y precio
CREATE INDEX idx_product_category_price ON products(CategoryID, Price);

-- Índice para búsquedas de clientes por ciudad
CREATE INDEX idx_customer_city ON customers(CityID);

-- 2. Vistas materializadas para reportes comunes
-- Vista materializada de ventas por categoría y mes
CREATE TABLE mv_sales_by_category_month AS
SELECT 
    c.CategoryName,
    DATE_FORMAT(s.SalesDate, '%Y-%m') as YearMonth,
    COUNT(*) as TotalSales,
    SUM(s.TotalPrice) as TotalRevenue,
    AVG(s.TotalPrice) as AvgTicket
FROM sales s
JOIN products p ON s.ProductID = p.ProductID
JOIN categories c ON p.CategoryID = c.CategoryID
GROUP BY c.CategoryName, DATE_FORMAT(s.SalesDate, '%Y-%m');

-- Vista materializada de rendimiento de vendedores
CREATE TABLE mv_sales_person_performance AS
SELECT 
    CONCAT(e.FirstName, ' ', e.LastName) as SalesPerson,
    COUNT(*) as TotalTransactions,
    SUM(s.TotalPrice) as TotalRevenue,
    AVG(s.Discount) as AvgDiscount,
    COUNT(DISTINCT s.CustomerID) as UniqueCustomers
FROM sales s
JOIN employees e ON s.SalesPersonID = e.EmployeeID
GROUP BY e.EmployeeID, e.FirstName, e.LastName;

-- 3. Procedimiento para actualizar vistas materializadas
DELIMITER //
CREATE PROCEDURE refresh_materialized_views()
BEGIN
    -- Actualizar vista de ventas por categoría
    TRUNCATE TABLE mv_sales_by_category_month;
    INSERT INTO mv_sales_by_category_month
    SELECT 
        c.CategoryName,
        DATE_FORMAT(s.SalesDate, '%Y-%m') as YearMonth,
        COUNT(*) as TotalSales,
        SUM(s.TotalPrice) as TotalRevenue,
        AVG(s.TotalPrice) as AvgTicket
    FROM sales s
    JOIN products p ON s.ProductID = p.ProductID
    JOIN categories c ON p.CategoryID = c.CategoryID
    GROUP BY c.CategoryName, DATE_FORMAT(s.SalesDate, '%Y-%m');

    -- Actualizar vista de rendimiento de vendedores
    TRUNCATE TABLE mv_sales_person_performance;
    INSERT INTO mv_sales_person_performance
    SELECT 
        CONCAT(e.FirstName, ' ', e.LastName) as SalesPerson,
        COUNT(*) as TotalTransactions,
        SUM(s.TotalPrice) as TotalRevenue,
        AVG(s.Discount) as AvgDiscount,
        COUNT(DISTINCT s.CustomerID) as UniqueCustomers
    FROM sales s
    JOIN employees e ON s.SalesPersonID = e.EmployeeID
    GROUP BY e.EmployeeID, e.FirstName, e.LastName;
END //
DELIMITER ;

-- 4. Evento para actualización automática de vistas materializadas
CREATE EVENT refresh_mv_daily
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY
DO CALL refresh_materialized_views();

-- 5. Análisis de rendimiento (comentarios explicativos)
/*
JUSTIFICACIÓN DE OPTIMIZACIONES:

1. ÍNDICES:
   - idx_sales_date: Optimiza consultas de ventas por período
   - idx_sales_product_date: Mejora análisis de tendencias de productos
   - idx_product_category_price: Acelera búsquedas de productos por categoría y rango de precios
   - idx_customer_city: Optimiza segmentación geográfica de clientes

2. VISTAS MATERIALIZADAS:
   - mv_sales_by_category_month: 
     * Reduce tiempo de generación de reportes mensuales
     * Evita joins costosos y cálculos repetitivos
   - mv_sales_person_performance:
     * Acelera análisis de rendimiento de vendedores
     * Precalcula métricas importantes de ventas

3. ACTUALIZACIÓN AUTOMÁTICA:
   - Procedimiento refresh_materialized_views:
     * Mantiene datos actualizados
     * Se ejecuta diariamente en horario no pico
   - Evento refresh_mv_daily:
     * Automatiza la actualización
     * Reduce carga manual de mantenimiento

IMPACTO EN RENDIMIENTO:
- Consultas de reportes: reducción esperada del 70-80% en tiempo de ejecución
- Análisis de tendencias: mejora de 40-50% en tiempo de respuesta
- Carga del sistema: distribuida eficientemente con actualizaciones programadas

MONITOREO SUGERIDO:
- Usar EXPLAIN ANALYZE para verificar uso de índices
- Monitorear tamaño de vistas materializadas
- Revisar tiempos de actualización de vistas
- Ajustar frecuencia de actualización según necesidad
*/

EXPLAIN ANALYZE SELECT * FROM mv_sales_by_category_month;
EXPLAIN ANALYZE SELECT * FROM mv_sales_person_performance;

SHOW INDEX FROM sales;
SHOW INDEX FROM products; 