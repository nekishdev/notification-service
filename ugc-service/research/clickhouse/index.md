Count rows = [32352880]

Function test_select {'sql': 'select count(*) from example.regular_table2'} Took 0.0020 seconds
Function test_select {'sql': 'select count(*) from example.regular_table2  where viewed_frame between 2000000 and 3000000'} Took 0.1220 seconds
Function test_select {'sql': 'SELECT max(viewed_frame), user_id FROM example.regular_table2 group by user_id'} Took 0.2893 seconds
Function test_select {'sql': 'SELECT count(DISTINCT user_id) FROM example.regular_table2'} Took 0.1333 seconds

### BATCH INSERT
* Function test_batch_insert {'size': 1000, 'count': 1} 
    
    Took 0.0258 seconds

* Function test_batch_insert {'size': 10000, 'count': 1} 

    Took 0.0353 seconds

* Function test_batch_insert {'size': 100000, 'count': 1} 
    
    Took 0.3312 seconds

* Function test_batch_insert {'size': 1000000, 'count': 1} 

    Took 32.0299 seconds

### SELECT
* Function test_select {'sql': 'select count(*) from views'} 

    Took 0.0020 seconds

* Function test_select {'sql': 'select count(*) from views where viewed_frame between 2000000 and 3000000'} 

    Took 0.1220 seconds

* Function test_select {'sql': 'SELECT max(viewed_frame), user_id FROM views group by user_id'} 

    Took 0.2893 seconds

* Function test_select {'sql': 'SELECT count(DISTINCT user_id) FROM views'} 

    Took 0.1333 seconds