-- Fraud rate by hour of day (gold table)
SELECT
    hour_of_day,
    COUNT(*)                              AS transactions,
    SUM(Class)                            AS fraud_transactions,
    ROUND(AVG(Class) * 100, 4)            AS fraud_rate_pct,
    ROUND(SUM(Amount), 2)                 AS total_amount
FROM transactions
GROUP BY hour_of_day
ORDER BY hour_of_day
