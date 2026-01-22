#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tweepy
import openai
from datetime import datetime
import pytz

# Configurar timezone para Brasil
br_tz = pytz.timezone('America/Sao_Paulo')

# Inicializar clientes
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_tweet_content():
    """Gera conteudo de tweet usando OpenAI."""
    try:
        current_hour = datetime.now(br_tz).hour
        
        # Diferentes prompts para cada horario
        if 6 <= current_hour < 12:  # Manha
            prompt = "Generate a motivational and productive morning message in Portuguese for a digital marketing professional. Keep it short and engaging for Twitter (280 chars max)."
        elif 12 <= current_hour < 18:  # Tarde
            prompt = "Generate an engaging afternoon productivity tip in Portuguese for digital marketers and entrepreneurs. Keep it short (280 chars max)."
        else:  # Noite
            prompt = "Generate an inspiring evening reflection in Portuguese about business growth and success. Keep it short (280 chars max)."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar conteudo com OpenAI: {e}")
        # Tweet padrao em caso de erro
        return "Bom dia! Vamos crescer juntos hoje! 🚀 #Marketing #Automacao"

def publish_tweet(content):
    """Publica o tweet na sua conta do Twitter."""
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        response = client.create_tweet(text=content)
        print(f"Tweet publicado com sucesso! ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"Erro ao publicar tweet: {e}")
        raise

if __name__ == "__main__":
    try:
        tweet_content = generate_tweet_content()
        print(f"Conteudo gerado: {tweet_content}")
        publish_tweet(tweet_content)
        print("Execucao concluida com sucesso!")
    except Exception as e:
        print(f"Erro fatal: {e}")
        exit(2)
