from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys, os

sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_weather_data
from transform_data import data_tranformation
from load_data import load_data
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)


API_KEY = os.getenv("API_KEY")
url = f'https://api.openweathermap.org/data/2.5/weather?q=Campinas,br&units=metric&lang=pt_br&appid={API_KEY}'

@dag(
  dag_id='weather_pipeline',
  default_args={
    'owner':'airflow',
    'depends_on_past': False,
    'retries':2,
    'retry_delay': timedelta(minutes=5),
  },
  description = 'Pipeline que extrai, transforma e carrega dados de API para o banco',
  schedule = '0 * * * *',
  start_date = datetime(2026,4,26),
  catchup = False,
  tags = ['weather', 'Olá Ivan!']
)
def weather_pipeline():
  
  @task
  def extract_task():
    extract_weather_data(url)

  @task
  def transform_task():
    df = data_tranformation()
    df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

  @task
  def load_task():
    import pandas as pd
    df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
    load_data('campinas_weather', df)

  extract_task() >> transform_task() >> load_task()


weather_pipeline()