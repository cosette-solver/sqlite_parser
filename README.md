Usage: 

```
python3 to_nameless.py <input sql file> <output json file>
```

## Input SQL file format
First establish the schema then the queries
```
CREATE TABLE indiv_sample_nyc (
	cmte_id INTEGER PRIMARY KEY,
   	transaction_amt INTEGER NOT NULL,
	name TEXT
);

CREATE TABLE comm (
	cmte_id INTEGER PRIMARY KEY,
   	cmte_nm INTEGER NOT NULL,
	cand_id INTEGER
);

SELECT
    cmte_id,
    transaction_amt,
    name
FROM indiv_sample_nyc
WHERE  (name LIKE '%TRUMP%') AND  (name LIKE '%DONALD%') 
ORDER BY name desc
LIMIT 5;

SELECT
    cmte_id,
    transaction_amt,
    name
FROM indiv_sample_nyc
WHERE  (name LIKE '%TRUMP%') AND  (name LIKE '%DONALD%');
```

## Output JSON file format
`queries` maps to a list of queries, and `schema` is refers to the schema.
```
{'queries': [{'Query': {'from': {'Var': 0},
                        'limit': '5',
                        'order': {'cols': [{'Col': [2]}],
                                  'direction': ['desc']},
                        'preds': {'And': [{'Like': [{'Col': [2]}, "'%trump%'"]},
                                          {'Like': [{'Col': [2]},
                                                    "'%donald%'"]}]},
                        'select': [{'Col': [0]}, {'Col': [1]}, {'Col': [2]}]}},
             {'Query': {'from': {'Var': 0},
                        'preds': {'And': [{'Like': [{'Col': [2]}, "'%trump%'"]},
                                          {'Like': [{'Col': [2]},
                                                    "'%donald%'"]}]},
                        'select': [{'Col': [0]}, {'Col': [1]}, {'Col': [2]}]}}],
 'schema': {'comm': {'cand_id': ['integer', None],
                     'cmte_id': ['integer', ['primary', 'key']],
                     'cmte_nm': ['integer', ['not', 'null']]},
            'indiv_sample_nyc': {'cmte_id': ['integer', ['primary', 'key']],
                                 'name': ['text', None],
                                 'transaction_amt': ['integer',
                                                     ['not', 'null']]}}}
```

