-- Cross-checking late_delivery_risk column against distinct Delivery Status
SELECT
	"Late_delivery_risk",
	"Delivery Status",
	COUNT(*) AS order_count
FROM orders
GROUP BY "Late_delivery_risk", "Delivery Status"
ORDER BY "Late_delivery_risk", "Delivery Status";