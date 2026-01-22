#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import pytz
from datetime import datetime
from requests_oauthlib import OAuth1Session

# Configurar timezone para Brasil
br_tz = pytz.timezone('America/Sao_Paulo')

# Inicializar tokens Twitter OAuth 1.0a
consumer_key = os.getenv('TWITTER_API_KEY', '')
consumer_secret = os.getenv('TWITTER_API_SECRET', '')
access_token = os.getenv('TWITTER_ACCESS_TOKEN', '')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')
openai_api_key = os.getenv('OPENAI_API_KEY', '')

def generate_tweet_content():
    """Gera conteudo de tweet usando OpenAI com fallback."""
    try:
        current_hour = datetime.now(br_tz).hour
        
        # Diferentes prompts para cada horario
        if 6 <= current_hour < 12:
            prompt_text = "Generate a motivational and productive morning message in Portuguese for digital marketers. Keep it short (280 chars max)."
        elif 12 <= current_hour < 18:
            prompt_text = "Generate an engaging afternoon productivity tip in Portuguese for digital marketers. Keep it short (280 chars max)."
        else:
            prompt_text = "Generate an inspiring evening reflection in Portuguese about business growth. Keep it short (280 chars max)."
        
        try:
            import openai
            client = openai.OpenAI(api_key=openai_api_key)
            message = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=100
            )
            return message.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}. Using fallback message.")
            return "Bom dia! Vamos crescer juntos! 🚀 #marketing #growth"
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return "Vamos criar conteúdo incrível hoje! 💪 #marketing"

def publish_tweet(content):
    """Publica tweet usando Twitter API OAuth 1.0a."""
    try:
        # Criar sessão OAuth 1.0a
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            signature_type='auth_header'
        )
        
        # Endpoint da Twitter API v2
        url = "https://api.twitter.com/2/tweets"
        
        payload = {"text": content[:280]}
        
        response = oauth.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print(f"Tweet publicado com sucesso: {response.json()}")
            return True
        else:
            print(f"Erro ao publicar tweet: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Erro fatal ao publicar: {e}")
        raise

if __name__ == "__main__":
    print("Iniciando publicacao de tweet...")
    tweet_content = generate_tweet_content()
    print(f"Conteudo gerado: {tweet_content}")
    publish_tweet(tweet_content)
