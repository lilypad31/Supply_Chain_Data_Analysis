-- Late delivery % by Shipping Mode, comparing scheduled vs. actual delivery windows
SELECT 
	"Shipping Mode",
	AVG("Days for shipment (scheduled)") AS avg_scheduled_days,
	AVG("Days for shipping (real)") AS avg_real_days,
	ROUND(AVG("Days for shipping (real)") - AVG("Days for shipment (scheduled)"), 2) AS avg_days_over
FROM orders
GROUP BY "Shipping Mode"
ORDER BY avg_days_over DESC;