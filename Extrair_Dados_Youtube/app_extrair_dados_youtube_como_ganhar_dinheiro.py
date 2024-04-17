import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Defina suas credenciais de API do YouTube
API_KEY = 'ID_da_API_DO_YOUTUBE'

# Crie uma função para extrair os dados do YouTube e salvar em um arquivo CSV
def extrair_dados_youtube_csv(palavra_chave, max_resultados=50, nome_arquivo='dados_youtube.csv'):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    try:
        # Extrair os dados em várias páginas de resultados
        videos = []
        next_page_token = None
        total_resultados = 0
        
        while True:
            request = youtube.search().list(
                part='snippet',
                q=palavra_chave,
                type='video',
                maxResults=min(50, max_resultados - total_resultados),  # Limitar a 50 ou ao restante dos resultados desejados
                pageToken=next_page_token
            )
            response = request.execute()
            
            # Extrair os dados relevantes dos vídeos encontrados
            for item in response['items']:
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
            
            # Verificar se há mais páginas de resultados
            next_page_token = response.get('nextPageToken')
            if not next_page_token or total_resultados == max_resultados:
                break
        
        # Salvar os dados em um arquivo CSV
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
            campos = ['titulo', 'descricao', 'id_video', 'canal']
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
            
            escritor_csv.writeheader()
            for video in videos:
                escritor_csv.writerow(video)
        
        print(f'Dados salvos com sucesso no arquivo "{nome_arquivo}"')
    
    except HttpError as e:
        print('Erro ao fazer a chamada à API do YouTube:', e)

# Teste a função de extração de dados e salvamento em CSV
palavra_chave = 'como ganhar dinheiro'
extrair_dados_youtube_csv(palavra_chave, max_resultados=1000)  # Exemplo: obter até 1000 resultados
