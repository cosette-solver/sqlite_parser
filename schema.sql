CREATE TABLE indiv_sample_nyc (
	cmte_id INTEGER PRIMARY KEY,
   	transaction_amt INTEGER NOT NULL,
	name TEXT
)

CREATE TABLE comm (
	cmte_id INTEGER PRIMARY KEY,
   	cmte_nm INTEGER NOT NULL,
	cand_id INTEGER
)

SELECT
    cmte_id,
    transaction_amt,
    name
FROM indiv_sample_nyc
WHERE  (name LIKE '%TRUMP%') AND  (name LIKE '%DONALD%') 
ORDER BY name desc
LIMIT 5

SELECT
    cmte_id,
    transaction_amt,
    name
FROM indiv_sample_nyc
WHERE  (name LIKE '%TRUMP%') AND  (name LIKE '%DONALD%') 





















































