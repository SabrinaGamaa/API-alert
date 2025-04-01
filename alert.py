# Pseudocódigo - Sistema de Alerta de Terremotos na Tailândia
# 1. Configuração Inicial
import requests
from datetime import datetime, timezone, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import os
from thaiquake_bot import notificar_todos, app
import asyncio
import threading
import json
from threading import Lock

# Dados do Twilio
load_dotenv()
account_sid = os.getenv("account_sid")
token = os.getenv("token")

# (EMSC-USGS).
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

# Salvar os id dos eventos
ARQUIVO_HISTORICO = os.getenv('terremotos_alertados', 'terremotos_alertados.json')
lock = Lock()

# Carregar historicos de eventos
def carregar_historico():
    with lock:
        if os.path.exists(ARQUIVO_HISTORICO):
            try:
                with open(ARQUIVO_HISTORICO, "r") as f:
                    conteudo = f.read().strip()
                    return json.load(conteudo) if conteudo else []
                
            except (json.JSONDecodeError, IOError) as e:
                print(f'Erro ao carregar histórico: {e}')
                return []
        return []

# salvar os eventos detectados
def salvar_historico(eventos):
    with lock:
        eventos_unicos = list(set(eventos))
        try:
            with open(ARQUIVO_HISTORICO, "w") as f:
                json.dump(eventos_unicos, f, indent=4)
        except IOError as e:
            print(f'Erro ao salvar histórico: {e}')


# Definir parâmetros para filtrar terremotos na Tailândia
max_lat = 20
min_lat = 5
max_lon = 105
min_lon = 95

# Aqui vou enviar mensagem com o twilio
async def enviar_mensagem(mag, place, data):
    client = Client(account_sid, token)

    try:
        mensagem = client.messages.create(
            messaging_service_sid=os.getenv("service_sid"),
            to = os.getenv("para"),
            body = f'Terremoto! Magnitude: {mag} | Data: {data} | Localização: {place}'
        )
        print(f'Mensagem enviada com sucesso: {mensagem.sid}')
    except Exception as e:
        print(f'Erro ao enviar mensagem: {e}')


# MAIN    
async def executar_alerta():
    # carregar historico de eventos
    historico = carregar_historico()

    print('Analisando possíveis tremores...')
    # Definir o tempo de consulta.
    hora_atual = datetime.now(timezone.utc)
    horas_atras = hora_atual - timedelta(days=4)
    horas_atras_str = horas_atras.strftime('%Y-%m-%dT%H:%M:%S')
    hora_atual_str = hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

    parametros = {
    'starttime': horas_atras_str,
    'endtime': hora_atual_str,
    'minmagnitude': 3.0,
    'format': 'geojson',
    'maxlatitude': max_lat,
    'minlatitude': min_lat,
    'maxlongitude': max_lon,
    'minlongitude': min_lon,
    
    }

    # Fazer uma requisição para a API USGS.
    try:
        response = requests.get(url, params=parametros, timeout=30)
        response.raise_for_status()
    except requests.Timeout:
        print('Erro: API demorou demais e foi interrompida')
        return
    except requests.RequestException as e:
        print(f'Erro na response: {e}')
        return

    data = response.json()
    novos_eventos = []

    if 'features' not in data or len(data['features']) == 0:
        print('Nenhum evento encontrado!')
    else:
        for evento in data['features']:
            evento_id = evento['id']

            # Se evento_id já está no historico, quer dizer que as mensagens já foram enviadas!
            if evento_id not in historico:
                time = datetime.fromtimestamp(evento['properties']['time'] / 1000).strftime('%Y-%m-%d T%H:%M:%S %z')
                mag = evento['properties']['mag']
                loc = evento['properties']['place']
                link = evento['properties']['url']

                mensagem_alerta = f'🚨 TERREMOTO DETECTADO! 🚨\n\n📍 Local: {loc}\n📅 Data e Hora: {time}\n💥 Magnitude: {mag}\n🔗 Mais informações: {link}'

                # Verificar se o alerta deve ser enviado
                if mag > 3:
                    novos_eventos.append(evento_id)
                    print(f'\n{mensagem_alerta}')

                    # Enviar para o twilio
                    await enviar_mensagem(mag=mag, place=loc, data=time)
                    # Enviar para o telegram
                    print("ENVIANDO MENSAGEM PARA TELEGRAM")
                    await notificar_todos(mensagem_alerta)
            else:
                print('Mensagens já foram enviadas!')

    if novos_eventos:
        salvar_historico(list(set(historico + novos_eventos)))


# Executa a função principal
async def monitoramento():
    while True:
        try:
            await executar_alerta()
        except Exception as e:
            print(f'Erro no monitoramento: {e}')
        finally:
            await asyncio.sleep(120)  # Espera 2 minutos entre as verificações


# Executa o telegram sem bloquear o loop
async def main():
    monitoramento_task = asyncio.create_task(monitoramento())
    await asyncio.gather(
        monitoramento_task,  
        asyncio.to_thread(app.run_polling),
    )


if __name__ == "__main__":
    print("Iniciando monitoramento e bot")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Criar uma thread separada para rodar o monitoramento
    def iniciar_monitoramento():
        asyncio.run(monitoramento())

    monitoramento_thread = threading.Thread(target=iniciar_monitoramento, daemon=True)
    monitoramento_thread.start()

    # Rodar o bot do Telegram diretamente na thread principal
    app.run_polling()


# Usar um servidor ou serviço online para rodar o script automaticamente.