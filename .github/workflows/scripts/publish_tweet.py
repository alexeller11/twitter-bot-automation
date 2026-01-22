#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import openai
import os
from datetime import datetime
from pytz import timezone
import random

# Configurar credenciais
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

if not bearer_token or not openai.api_key:
    print("Erro: TWITTER_BEARER_TOKEN ou OPENAI_API_KEY não configurados!")
    exit(1)

# Inicializar cliente Twitter v2
client = tweepy.Client(bearer_token=bearer_token)

# Timezone Brasil
br_tz = timezone('America/Sao_Paulo')

def obter_hora_atual():
    """Obtém a hora atual em São Paulo"""
    return datetime.now(br_tz).hour

def gerar_tweet(tipo):
    """Gera um tweet baseado na hora do dia"""
    prompts = {
        'manha': 'Crie um tweet motivacional sobre criptomo edas e oportunidades em PORTUGUÊS BRASILEIRO. Máximo 280 caracteres. Adicione 2-3 emojis relevantes. Tom inspirador.',
        'tarde': 'Gere um tweet informativo sobre tendências de mercado crypto em PORTUGUÊS BRASILEIRO. Seja profissional e inteligente. Máximo 280 caracteres. Inclua hashtags como #CryptoBR ou #Bitcoin.',
        'noite': 'Crie um tweet reflexivo sobre a jornada nos mercados financeiros em PORTUGUÊS BRASILEIRO. Tom inspirador e profissional. Máximo 280 caracteres. Use emojis sérios.'
    }
    
    prompt = prompts.get(tipo, prompts['tarde'])
    
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar tweet: {e}")
        return None

def publicar_tweet(texto):
    """Publica um tweet"""
    if not texto:
        print("Texto vazio, não publicando.")
        return False
    
    try:
        response = client.create_tweet(text=texto)
        tweet_id = response.data['id']
        hora_local = datetime.now(br_tz).strftime('%H:%M:%S')
        print(f"[{hora_local}] ✅ Tweet publicado com sucesso!")
        print(f"ID: {tweet_id}")
        print(f"Conteúdo: {texto}")
        return True
    except Exception as e:
        print(f"❌ Erro ao publicar tweet: {e}")
        return False

def main():
    """Função principal"""
    hora_atual = obter_hora_atual()
    hora_formatada = datetime.now(br_tz).strftime('%H:%M:%S')
    
    print(f"\n{'='*60}")
    print(f"[{hora_formatada}] Iniciando publish_tweet.py")
    print(f"Hora em São Paulo: {hora_atual}h")
    
    # Determinar tipo de tweet baseado na hora
    if 6 <= hora_atual < 12:
        tipo = 'manha'
        print("📤 Gerando tweet da MANHÃ...")
    elif 12 <= hora_atual < 18:
        tipo = 'tarde'
        print("📤 Gerando tweet da TARDE...")
    else:
        tipo = 'noite'
        print("📤 Gerando tweet da NOITE...")
    
    # Gerar e publicar
    print("\n🤖 Gerando conteúdo com IA...")
    tweet = gerar_tweet(tipo)
    
    if tweet:
        print(f"\n💬 Tweet gerado: {tweet}\n")
        publicar_tweet(tweet)
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
