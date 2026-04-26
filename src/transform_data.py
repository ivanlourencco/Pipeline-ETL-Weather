import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).resolve().parent.parent / "data/weather_data/weather.json"
columns_names_to_drop = ["weather", 'weather_icon', 'sys.type']
columns_name_to_rename = {
    'base': 'base',
    'visibility': 'visibility',
    'dt': 'datetime',
    'timezone': 'timezone',
    'id': 'city_id',
    'name': 'city_name',
    'cod': 'code',
    'coord.lon': 'longitude',
    'coord.lat': 'latitude',
    'main.temp': 'temperature',
    'main.feels_like': 'feels_like',
    'main.temp_min': 'min_temperature',
    'main.temp_max': 'max_temperature',
    'main.pressure': 'pressure',
    'main.humidity': 'humidity',
    'main.sea_level': 'sea_level',
    'main.grnd_level': 'grnd_level',
    'wind.speed': 'wind_speed',
    'wind.deg': 'wind_deg',
    'wind.gust': 'wind_gust',
    'clouds.all': 'cloudiness',
    'sys.country': 'country',
    'sys.sunrise': 'sunrise',
    'sys.sunset': 'sunset',
}
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name: str) -> pd.DataFrame:
  logging.info(f"Criando um DataFrame do arquivo JSON:")
  path = path_name
  
  if not path.exists():
    raise FileNotFoundError(f'Arquivo não encontrado: {path}')
  
  with open(path) as f:
    data = json.load(f)

  df = pd.json_normalize(data)
  logging.info(f"\n DataFrame craido com {len(df)} linhas e {len(df.columns)} colunas. ")
  return df
  

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
  df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

  df_weather = df_weather.rename(columns={
    'id':'weather_id', 
    'main':'weather_main', 
    'description':'weather_description', 
    'icon':'weather_icon'
  })

  df = pd.concat([df_weather, df], axis=1)
  logging.info(f"\n DataFrame com colunas normalizadas: {df}")  
  return df

def drop_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:
 
  logging.info(f"Excluindo colunas desnecessárias do DataFrame {columns_names}")
  df = df.drop(columns=columns_names)
  logging.info(f"\n DataFrame após exclusão de colunas: {df}")  
  return df

def rename_columns(df: pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
  logging.info(f"Renomeando colunas do DataFrame para {columns_names}")
  df = df.rename(columns=columns_names)
  logging.info(f"\n DataFrame após renomeação de colunas: {df}")  
  return df

def normalize_datetime_columns(df: pd.DataFrame, columns_name:list[str]) -> pd.DataFrame:
  logging.info(f"Normalizando colunas de data: {columns_name}")
  for name in columns_name:
    df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
  logging.info(f"\n DataFrame após normalização de colunas de data: {df}")
  return df

def data_tranformation():
  print('Iniciando a transformações')
  df = create_dataframe(path_name)
  df = normalize_weather_columns(df)
  df = drop_columns(df, columns_names_to_drop)
  df = rename_columns(df, columns_name_to_rename)
  df = normalize_datetime_columns(df, columns_to_normalize_datetime)
  logging.info(f"\n DataFrame após transformações: {df}")
  return df

  