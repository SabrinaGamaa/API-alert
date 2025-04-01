import requests
import json
from datetime import datetime, timezone

# (EMSC).
url2 = 'https://earthquake.usgs.gov/fdsnws/event/1/[ MÉTODO [? PARÂMETROS ]]'

# Definir parâmetros para filtrar terremotos na Tailândia
# Definir limite mínimo de magnitude para alertas.
min_magnitude = 4.0  # Mínima magnitude
max_lat = 20.0       # Latitude máxima (Tailândia)
min_lat = 5.0        # Latitude mínima (Tailândia)
max_lon = 105.0      # Longitude máxima (Tailândia)
min_lon = 95.0       # Longitude mínima (Tailândia)

# Definir região de interesse (Tailândia).
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmag={min_magnitude}&maxlat={max_lat}&minlat={min_lat}&maxlon={max_lon}&minlon={min_lon}"


# 2. Coletar Dados da API
# Fazer uma requisição para a API de terremotos.
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if 'features' in data:
        for event in data['features']:
            magnitude = event['properties']['mag']
            location = event['properties']['place']
            time_ms = event['properties']['time']
            time_s = time_ms / 1000
            time = datetime.fromtimestamp(time_s, tz=timezone.utc)
            print(f'Data e Hora: {time.strftime('%Y-%m-%d %H:%M:%S %z')}, Magnitude: {magnitude}, Localização: {location}')
            
    else:
        print(f'Nenhum evento encontrado.')
else:
    print(f'Erro na requisição: {response.status_code}')