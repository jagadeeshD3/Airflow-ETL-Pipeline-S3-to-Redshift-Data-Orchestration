"""
Generates fake order data using Faker, uploads to S3, and loads to Redshift
"""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.empty import EmptyOperator
import pandas as pd
from faker import Faker
import random
from io import StringIO

# Constants
S3_BUCKET = 'orders_source_bucket'  # Replace with your S3 bucket name
REDSHIFT_SCHEMA = 'staging'  # Redshift schema (e.g., 'public' or 'staging')
REDSHIFT_STAGING_TABLE = 'stg_orders'  # Redshift staging table name

# Initialize Faker
fake = Faker()


def generate_cdc_order_data(num_rows: int = 500) -> pd.DataFrame:
    """
    Generate fake order data using Faker library
    
    Args:
        num_rows: Number of rows to generate
        
    Returns:
        DataFrame containing fake order data
    """
    data = []
    for i in range(num_rows):
        order = {
            'order_id': i + 1,
            'customer_id': random.randint(1, 1000),
            'order_date': fake.date_this_year(),
            'status': random.choice(['CREATED', 'SHIPPED', 'DELIVERED', 'CANCELLED']),
            'product_id': random.randint(1, 100),
            'quantity': random.randint(1, 5),
            'price': round(random.uniform(10.0, 500.0), 2),
            'total_amount': 0.0,
            'cdc_timestamp': datetime.now()
        }
        order['total_amount'] = round(order['quantity'] * order['price'], 2)
        data.append(order)

    return pd.DataFrame(data)


def upload_df_to_s3(bucket_name: str, file_name: str, df: pd.DataFrame) -> None:
    """
    Upload DataFrame to S3 as CSV
    
    Args:
        bucket_name: S3 bucket name
        file_name: S3 file path/key
        df: Pandas DataFrame to upload
    """
    s3_hook = S3Hook(aws_conn_id='aws_default')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    s3_hook.load_string(
        string_data=csv_buffer.getvalue(),
        key=file_name,
        bucket_name=bucket_name,
        replace=True
    )
    print(f"✓ Data uploaded to s3://{bucket_name}/{file_name}")


# Define the DAG using the new decorator syntax
@dag(
    dag_id='extract_and_load_data_to_redshift',
    schedule='@daily',  # Changed from schedule_interval to schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    tags=['etl', 'redshift', 's3', 'data-pipeline'],
    doc_md=__doc__,
)
def extract_and_load_data_to_redshift():
    """
    ETL Pipeline: Extract fake order data → Load to S3 → Copy to Redshift
    """
    
    # Task 1: Generate and upload data to S3 using TaskFlow API
    @task
    def generate_and_upload_to_s3() -> str:
        """
        Generate fake order data and upload to S3
        
        Returns:
            S3 file path (key) for downstream tasks
        """
        # Generate 20 rows of fake order data
        df_order_data = generate_cdc_order_data(num_rows=20)
        
        # Create timestamped file name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"incoming_data/orders/cdc_order_data_{timestamp}.csv"
        
        # Upload to S3
        upload_df_to_s3(S3_BUCKET, file_name, df_order_data)
        
        return file_name
    
    # Start marker (using EmptyOperator, which replaces DummyOperator)
    start = EmptyOperator(task_id='start')
    
    # Generate and upload data
    s3_file_path = generate_and_upload_to_s3()
    
    # Task 2: Copy data from S3 to Redshift
    copy_to_redshift = S3ToRedshiftOperator(
        task_id='copy_to_redshift',
        schema=REDSHIFT_SCHEMA,
        table=REDSHIFT_STAGING_TABLE,
        s3_bucket=S3_BUCKET,
        s3_key=s3_file_path,  # Direct reference to TaskFlow output
        redshift_conn_id='redshift_conn',
        aws_conn_id='aws_default',
        copy_options=[
            "CSV",
            "IGNOREHEADER 1",
        ],
    )
    
    # End marker
    end = EmptyOperator(task_id='end')
    
    # Define task dependencies
    start >> s3_file_path >> copy_to_redshift >> end


# Instantiate the DAG
dag_instance = extract_and_load_data_to_redshift()