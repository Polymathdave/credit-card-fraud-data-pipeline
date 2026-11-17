-- Fraud rate and average amount by transaction size band (gold table)
SELECT
    amount_bucket,
    COUNT(*)                                                  AS transactions,
    SUM(Class)                                                AS fraud_transactions,
    ROUND(AVG(Class) * 100, 4)                                AS fraud_rate_pct,
    ROUND(AVG(CASE WHEN Class = 1 THEN Amount END), 2)        AS avg_fraud_amount
FROM transactions
GROUP BY amount_bucket
ORDER BY fraud_rate_pct DESC
