"""
Executes a stored procedure for incremental data loading
"""
from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.empty import EmptyOperator

# Constants for database and schema
DATABASE_ID = 'AIRFLOW'
SCHEMA_ID = 'SILVER'


@dag(
    dag_id='snowflake_incremental_load',
    schedule='@daily',  # Changed from schedule_interval to schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        'owner': 'airflow',
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
    },
    tags=['snowflake', 'incremental-load', 'data-warehouse'],
    doc_md=__doc__,
)
def snowflake_incremental_load():
    """
    Daily incremental load to Snowflake using stored procedure
    """
    
    # Start marker
    start = EmptyOperator(task_id='start')
    
    # Execute Snowflake stored procedure
    incremental_load = SnowflakeOperator(
        task_id='incremental_load',
        sql=f'CALL {DATABASE_ID}.{SCHEMA_ID}.INCREMENTAL_LOAD();',
        snowflake_conn_id='snowflake_conn',
    )
    
    # End marker
    end = EmptyOperator(task_id='end')
    
    # Define task dependencies
    start >> incremental_load >> end


# Instantiate the DAG
dag_instance = snowflake_incremental_load()