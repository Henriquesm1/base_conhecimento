from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import Conhecimento
from . import db
from sqlalchemy import or_
import spacy

# Inicializando NLP com spaCy
nlp = spacy.load("pt_core_news_sm")

main = Blueprint('main', __name__)

# Função para extrair palavras-chave da pergunta
def extrair_palavras_chave(pergunta):
    doc = nlp(pergunta)
    palavras_chave = []
    for token in doc:
        if not token.is_stop and token.is_alpha:
            palavras_chave.append(token.lemma_)
    return palavras_chave

# Função para buscar resposta no banco de dados
def buscar_resposta(pergunta):
    # Extrair palavras-chave da pergunta
    palavras_chave = extrair_palavras_chave(pergunta)
    
    # Tentar encontrar uma correspondência exata com a pergunta
    resposta = Conhecimento.query.filter(Conhecimento.pergunta.like(f'%{pergunta}%')).first()
    
    # Se não encontrar uma correspondência exata, buscar pelas palavras-chave
    if not resposta:
        condicoes = or_(*(Conhecimento.pergunta.like(f'%{palavra}%') for palavra in palavras_chave))
        resposta = Conhecimento.query.filter(condicoes).first()
    
    if resposta:
        return resposta.resposta
    else:
        return "Desculpe, não encontrei a resposta para sua pergunta."

# Rota para redirecionar a página inicial para o chatbot
@main.route('/')
def index():
    return redirect(url_for('main.chat'))

# Rota para exibir o chatbot
@main.route('/chat')
def chat():
    return render_template('chatbot.html')

# Rota para processar as perguntas e retornar as respostas via AJAX
@main.route('/chatbot', methods=['POST'])
def chatbot():
    dados = request.get_json()
    pergunta = dados.get('pergunta')

    # Buscar a resposta usando a pergunta
    resposta = buscar_resposta(pergunta)

    return jsonify({"resposta": resposta})

# Rota para exibir o formulário de adição de conhecimento
@main.route('/adicionar_conhecimento', methods=['GET', 'POST'])
def adicionar_conhecimento():
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        resposta = request.form['resposta']
        categoria = request.form['categoria']
        palavras_chave = request.form['palavras_chave']

        # Criação do novo item de conhecimento
        novo_conhecimento = Conhecimento(
            pergunta=pergunta,
            resposta=resposta,
            categoria=categoria,
            palavras_chave=palavras_chave
        )
        
        # Inserção no banco de dados
        db.session.add(novo_conhecimento)
        db.session.commit()

        return redirect(url_for('main.adicionar_conhecimento'))

    return render_template('adicionar_conhecimento.html')

# Rota para sugestões automáticas
@main.route('/sugestoes', methods=['GET'])
def sugestoes():
    termo = request.args.get('termo')
    if termo:
        # Buscar perguntas no banco de dados que contenham o termo digitado
        sugestoes = Conhecimento.query.filter(Conhecimento.pergunta.like(f'%{termo}%')).limit(5).all()
        sugestoes_formatadas = [sugestao.pergunta for sugestao in sugestoes]
        return jsonify(sugestoes_formatadas)
    return jsonify([])
