import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

# Defina as credenciais de API do YouTube
API_KEY = 'ID_da_API_DO_YOUTUBE'

# Função para buscar todos os canais disponíveis
def buscar_canais_disponiveis(api_key, palavra_chave):
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        canais = []
        next_page_token = None

        while True:
            request = youtube.search().list(
                part='snippet',
                q=palavra_chave,
                type='channel',
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                canal = {
                    'nome': item['snippet']['channelTitle'],
                    'id_canal': item['id']['channelId']
                }
                canais.append(canal)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return canais

    except HttpError as e:
        print('Erro ao fazer a chamada à API do YouTube:', e)
        return None

# Função para extrair vídeos de um canal filtrados por data de postagem
def extrair_videos_por_data(api_key, canal_id, data_inicial, data_final, max_resultados=50):
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        videos = []
        next_page_token = None

        while True:
            request = youtube.search().list(
                part='snippet',
                channelId=canal_id,
                type='video',
                maxResults=min(50, max_resultados - len(videos)),
                publishedAfter=data_inicial.isoformat() + 'Z',  # Data inicial em formato ISO 8601
                publishedBefore=data_final.isoformat() + 'Z',  # Data final em formato ISO 8601
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                video = {
                    'titulo': item['snippet']['title'],
                    'descricao': item['snippet']['description'],
                    'id_video': item['id']['videoId'],
                    'canal': item['snippet']['channelTitle']
                }
                videos.append(video)

            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(videos) >= max_resultados:
                break

        return videos

    except HttpError as e:
        print('Erro ao fazer a chamada à API do YouTube:', e)
        return None

# Testar a função
def extrair_e_salvar_videos_por_data(api_key, palavra_chave, data_inicial, data_final, max_resultados=50, nome_arquivo='videos.csv'):
    canais = buscar_canais_disponiveis(api_key, palavra_chave)
    
    if canais:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            campos = ['titulo', 'descricao', 'id_video', 'canal']
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
            escritor_csv.writeheader()
            
            for canal in canais:
                videos = extrair_videos_por_data(api_key, canal['id_canal'], data_inicial, data_final, max_resultados)
                if videos:
                    for video in videos:
                        escritor_csv.writerow(video)
        
        print(f'Dados salvos com sucesso no arquivo "{nome_arquivo}"')
    else:
        print('Não foi possível extrair os dados do YouTube.')

# Testar a função
data_inicial = datetime(2024, 4, 10)  # Data inicial desejada (ano, mês, dia)
data_final = datetime(2024, 4, 11)    # Data final desejada (ano, mês, dia)
palavra_chave = 'historia dos empresarios brasileiros'
extrair_e_salvar_videos_por_data(API_KEY, palavra_chave, data_inicial, data_final, max_resultados=1000)
