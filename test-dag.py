from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import psutil

def check_memory_usage(**kwargs):
    process_list = [p for p in psutil.process_iter(['pid', 'name']) if 'airflow' in p.info['name']]
    total_memory_usage = 0
    for process in process_list:
        try:
            process_memory_info = psutil.Process(process.info['pid']).memory_info()
            total_memory_usage += process_memory_info.rss / (1024 * 1024)  # Convert bytes to MB
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if total_memory_usage > 512:
        kwargs['ti'].xcom_push(key='alert', value=True)
    else:
        kwargs['ti'].xcom_push(key='alert', value=False)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'check_memory_usage',
    default_args=default_args,
    description='A DAG to monitor memory usage and send email alerts',
    schedule_interval=timedelta(minutes=10),
)

check_memory = PythonOperator(
    task_id='check_memory',
    provide_context=True,
    python_callable=check_memory_usage,
    dag=dag,
)

send_email = EmailOperator(
    task_id='send_email',
    to='demo@no-place-on-earth.kom',
    subject='Memory Usage Alert',
    html_content='Memory usage is over 512MB',
    dag=dag,
)

check_memory >> send_email
