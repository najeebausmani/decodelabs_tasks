-- =====================================================================
-- DecodeLabs Project 3 - SQL Data Analysis (E-commerce Orders)
-- Engine: SQLite  | Table: orders (1,200 rows, Jan 2023 - Jun 2025)
-- Columns: OrderID, Date (YYYY-MM-DD text), CustomerID, Product, Quantity,
--          UnitPrice, ShippingAddress, PaymentMethod, OrderStatus,
--          TrackingNumber, ItemsInCart, CouponCode, ReferralSource, TotalPrice
-- Execution order reminder: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY
-- =====================================================================

-- ### Q01 | SELECT basics | What does an order record look like?
SELECT OrderID, Date, Product, Quantity, UnitPrice, TotalPrice, OrderStatus
FROM orders
LIMIT 10;

-- ### Q02 | WHERE (comparison + equality) + ORDER BY | Which delivered orders are worth $2,000 or more?
SELECT OrderID, Date, Product, Quantity, TotalPrice
FROM orders
WHERE OrderStatus = 'Delivered' AND TotalPrice >= 2000
ORDER BY TotalPrice DESC;

-- ### Q03 | WHERE (IN, BETWEEN, LIKE) | Social-media orders in H1 2025 for products starting with 'L' or 'M'
SELECT OrderID, Date, Product, ReferralSource, TotalPrice
FROM orders
WHERE ReferralSource IN ('Instagram', 'Facebook')
  AND Date BETWEEN '2025-01-01' AND '2025-06-30'
  AND (Product LIKE 'L%' OR Product LIKE 'M%')
ORDER BY Date;

-- ### Q04 | COUNT / SUM / AVG | What are the headline KPIs?
SELECT COUNT(*)                         AS total_orders,
       COUNT(DISTINCT CustomerID)       AS unique_customers,
       ROUND(SUM(TotalPrice), 2)        AS gross_order_value,
       ROUND(AVG(TotalPrice), 2)        AS avg_order_value,
       MIN(TotalPrice)                  AS smallest_order,
       MAX(TotalPrice)                  AS largest_order
FROM orders;

-- ### Q05 | GROUP BY + aggregates + ORDER BY | Revenue and volume by product
SELECT Product,
       COUNT(*)                  AS orders,
       ROUND(SUM(TotalPrice), 2) AS revenue,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY Product
ORDER BY revenue DESC;

-- ### Q06 | GROUP BY + percentage contribution | How are orders split by status?
SELECT OrderStatus,
       COUNT(*) AS orders,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) AS pct_of_orders,
       ROUND(SUM(TotalPrice), 2) AS order_value
FROM orders
GROUP BY OrderStatus
ORDER BY orders DESC;

-- ### Q07 | WHERE + GROUP BY (year) | Like-for-like H1 comparison: is revenue falling?
SELECT strftime('%Y', Date)      AS year,
       COUNT(*)                  AS orders,
       ROUND(SUM(TotalPrice), 2) AS revenue,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
WHERE strftime('%m', Date) <= '06'
GROUP BY year
ORDER BY year;

-- ### Q08 | GROUP BY (quarter) | Quarterly revenue trend
SELECT strftime('%Y', Date) || '-Q' || ((CAST(strftime('%m', Date) AS INTEGER) + 2) / 3) AS quarter,
       COUNT(*)                  AS orders,
       ROUND(SUM(TotalPrice), 2) AS revenue
FROM orders
GROUP BY quarter
ORDER BY quarter;

-- ### Q09 | CASE inside SUM | What share of each product's orders is Cancelled or Returned?
SELECT Product,
       COUNT(*) AS orders,
       SUM(CASE WHEN OrderStatus IN ('Cancelled', 'Returned') THEN 1 ELSE 0 END) AS lost_orders,
       ROUND(100.0 * SUM(CASE WHEN OrderStatus IN ('Cancelled', 'Returned') THEN 1 ELSE 0 END) / COUNT(*), 1) AS loss_rate_pct
FROM orders
GROUP BY Product
ORDER BY loss_rate_pct DESC;

-- ### Q10 | HAVING | Which payment methods have an average order above $1,050?
SELECT PaymentMethod,
       COUNT(*)                  AS orders,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY PaymentMethod
HAVING AVG(TotalPrice) > 1050
ORDER BY avg_order_value DESC;

-- ### Q11 | GROUP BY (two columns) | Revenue by referral source and order status
SELECT ReferralSource, OrderStatus,
       COUNT(*)                  AS orders,
       ROUND(SUM(TotalPrice), 2) AS revenue
FROM orders
GROUP BY ReferralSource, OrderStatus
ORDER BY ReferralSource, revenue DESC;

-- ### Q12 | HAVING (repeat customers) | Which customers ordered more than once?
SELECT CustomerID,
       COUNT(*)                  AS orders,
       ROUND(SUM(TotalPrice), 2) AS total_spent
FROM orders
GROUP BY CustomerID
HAVING COUNT(*) > 1
ORDER BY total_spent DESC;

-- ### Q13 | GROUP BY quantity | How does basket size drive order value?
SELECT Quantity,
       COUNT(*)                  AS orders,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY Quantity
ORDER BY Quantity;

-- ### Q14 | Subquery (outliers) | Orders above the IQR fence from Project 2 ($3,330.41)
SELECT OrderID, Product, Quantity, UnitPrice, TotalPrice, OrderStatus
FROM orders
WHERE TotalPrice > 3330.41
ORDER BY TotalPrice DESC;

-- ### Q15 | Alias-trap fix | Products whose revenue exceeds $190k (alias cannot be used in WHERE; use HAVING)
SELECT Product, ROUND(SUM(TotalPrice), 2) AS revenue
FROM orders
GROUP BY Product
HAVING SUM(TotalPrice) > 190000
ORDER BY revenue DESC;

-- ### Q16 | GROUP BY coupon | Coupon usage (CAUTION: 309 blanks were filled with FREESHIP in Project 1)
SELECT CouponCode,
       COUNT(*)                  AS orders,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY CouponCode
ORDER BY orders DESC;
