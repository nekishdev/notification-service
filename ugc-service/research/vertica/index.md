Count rows = [35803610]

### Одиночный INSERT
* Function test_single_insert {'count': 100} 

    Took 0.6713 seconds

* Function test_single_insert {'count': 1000} 

    Took 8.1539 seconds

### BATCH INSERT
* Function test_batch_insert {'size': 1000, 'count': 1} 
    
    Took 0.0215 seconds

* Function test_batch_insert {'size': 10000, 'count': 1} 

    Took 0.0647 seconds

* Function test_batch_insert {'size': 100000, 'count': 1} 
    
    Took 0.5622 seconds

* Function test_batch_insert {'size': 1000000, 'count': 1} 

    Took 5.5268 seconds

### SELECT
* Function test_select {'sql': 'select count(*) from views'} 

    Took 0.0704 seconds

* Function test_select {'sql': 'select count(*) from views where viewed_frame between 2000000 and 3000000'} 

    Took 0.3222 seconds

* Function test_select {'sql': 'SELECT max(viewed_frame), user_id FROM views group by user_id'} 

    Took 0.9613 seconds

* Function test_select {'sql': 'SELECT count(DISTINCT user_id) FROM views'} 

    Took 0.6396 seconds