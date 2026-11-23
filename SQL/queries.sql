-- 1. Top 10 Mutual Funds by AUM
SELECT f.scheme_name, f.fund_house, f.category, p.aum_crore
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 10;


-- 2. Fund House-wise AUM Analysis
SELECT fund_house,
       ROUND(SUM(aum_crore), 2) AS total_aum_crore,
       SUM(num_schemes) AS total_schemes
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC;


-- 3. Best Performing Mutual Funds
SELECT f.scheme_name, f.fund_house, f.category,
       p.return_1yr_pct, p.return_3yr_pct, p.return_5yr_pct
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.return_5yr_pct DESC
LIMIT 10;


-- 4. Category-wise Average Returns
SELECT f.category,
       ROUND(AVG(p.return_1yr_pct), 2) AS avg_1yr_return,
       ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return,
       ROUND(AVG(p.return_5yr_pct), 2) AS avg_5yr_return
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.category
ORDER BY avg_5yr_return DESC;


-- 5. Monthly Average NAV Analysis
SELECT d.year, d.month,
       ROUND(AVG(n.nav), 2) AS average_nav
FROM fact_nav n
JOIN dim_date d ON n.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 6. Investor Transaction Analysis
SELECT transaction_type,
       COUNT(*) AS total_transactions,
       ROUND(SUM(amount_inr), 2) AS total_amount_inr,
       ROUND(AVG(amount_inr), 2) AS average_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;


-- 7. City-wise Investor Analysis
SELECT city, state,
       COUNT(DISTINCT investor_id) AS total_investors,
       ROUND(SUM(amount_inr), 2) AS total_transaction_amount
FROM fact_transactions
GROUP BY city, state
ORDER BY total_investors DESC
LIMIT 10;


-- 8. Risk-wise Fund Analysis
SELECT f.risk_category,
       COUNT(DISTINCT f.amfi_code) AS total_funds,
       ROUND(AVG(p.return_1yr_pct), 2) AS avg_1yr_return,
       ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return,
       ROUND(AVG(p.return_5yr_pct), 2) AS avg_5yr_return
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.risk_category
ORDER BY avg_5yr_return DESC;


-- 9. Expense Ratio Comparison
SELECT f.scheme_name, f.fund_house, f.category,
       p.expense_ratio_pct, p.return_5yr_pct
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.expense_ratio_pct ASC
LIMIT 10;


-- 10. Fund House-wise Scheme Count and AUM
SELECT fund_house,
       SUM(num_schemes) AS total_schemes,
       ROUND(SUM(aum_crore), 2) AS total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC;