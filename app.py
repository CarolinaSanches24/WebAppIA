from flask import Flask, redirect, url_for, request, render_template, session;
import requests, os, uuid,json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__);

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html');

@app.route('/', methods=['POST'])
def index_post():
    #Lendo os valores do formulario
    texto_original = request.form['text']
    idioma_alvo = request.form['language']
    
    #Carregando os valores do arquivo env
    key=os.environ['KEY']
    endpoint= os.environ['ENDPOINT']
    location = os.environ['LOCATION']
    
    # Indicando a versão da API (3.0) de tradução e o idioma de destino
    path = '/translate?api-version=3.0'
    
    #Adicionando  o parâmetro do idioma de destino
    idioma_alvo_parametro = '&to=' + idioma_alvo
    
    # Criação do URL completo
    url_construido = endpoint + path + idioma_alvo_parametro
    
    #Configuração das informações do header, que incluem a chave de assinatura
    headers = {
        'Ocp-Apim-Subscription-Key': key, #verifica que você tem permissão para acessar os recursos solicitados.
        'Ocp-Apim-Subscription-Region': location, # região onde sua instância está hospedada ou a região que você deseja acessar. 
        'Content-type': 'application/json', # informa ao servidor que o corpo da solicitação está em formato JSON 
        'X-ClientTraceId': str(uuid.uuid4())  #identificador único para a solicitação X- no início sugere que é um cabeçalho personalizado, não padrão na especificação HTTP.
    }
    
    #Criando o corpo da solicitação com o texto a ser traduzido
    body = [{'text':texto_original}]
    
    #cria a conexao usando post
    requisicao_traducao = requests.post(url_construido, headers=headers, json=body)
    # Recupera a resposta em JSON
    resposta_traducao= requisicao_traducao.json();
    #Recupera a tradução
    texto_traduzido = resposta_traducao[0]['translations'][0]['text']
    
    #Chamada ao modelo de renderizacao, pasando o texto traduzido
    # texto original, idioma de destino e modelo
    
    return render_template(
        'results.html',
        texto_traduzido=texto_traduzido,
        texto_original=texto_original,
        idioma_alvo=idioma_alvo
    )