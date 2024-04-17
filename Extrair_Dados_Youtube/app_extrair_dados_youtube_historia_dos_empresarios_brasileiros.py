import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Defina as crendenciais de API do YOUTUBE
API_KEY = 'ID_da_API_DO_YOUTUBE'

# Cria uma função para extrair os dados do YouTube e salvar em um arquivo CSV
def extrair_dados_youtube_csv(palavra_chave, max_resultados=50, nome_arquivo ='historia_dos_empresarios_brasileiros.csv'):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        # Extrair os dados em várias páginas de resultados
        videos = []
        next_page_token = None
        total_resultados = 0

        while True:
            request = youtube.search().list(
                part ='snippet',
                q = palavra_chave,
                type =  'video',
                maxResults = min(50, max_resultados - total_resultados), # Limitar a 50 ou o restante dos resultados
                pageToken = next_page_token
            )
            reponse = request.execute()

            # Extrair os dados relevantes dos videos encontrados
            for item in reponse['items']:
                video = {
                    'titulo': item['snippet']['title'],
                    'descricao': item['snippet']['description'],
                    'id_video': item['id']['videoId'],
                    'canal': item['snippet']['channelTitle']
                }
                videos.append(video)
                total_resultados += 1
                if total_resultados == max_resultados:
                    break

            # Verifica se há mais páginas de resultados
            next_page_token = reponse.get('nextPageToken')
            if not next_page_token or total_resultados == max_resultados:
                break

        # Salva os dados em um arquivo CSV
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            campos = ['titulo','descricao','id_video','canal']
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)

            escritor_csv.writeheader()
            for video in videos:
                escritor_csv.writerow(video)

        print(f'Dados salvos com sucesso no arquivo "{nome_arquivo}"')

    except HttpError as e:
        print('Error ao fazer a chamada à API do YouTube', e)

# Testa a função de extração de dados e salvamento em CSV
palavra_chave = 'historia dos empresarios brasileiros'
extrair_dados_youtube_csv(palavra_chave, max_resultados=1000) # Exemplo: obter até 1000 resultados