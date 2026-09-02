--Late delivery % by Shipping Mode
SELECT 
	"Shipping Mode",
	COUNT(*) AS total_orders,
	COUNT(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 END) AS late_orders,
	ROUND(COUNT(CASE WHEN "Delivery Status" = 'Late delivery' THEN 1 END) * 100.0 / COUNT(*), 2) AS late_pct	
FROM orders
GROUP BY "Shipping Mode"
ORDER BY late_pct DESC;