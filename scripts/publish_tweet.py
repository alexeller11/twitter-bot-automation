#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import requests
import pytz
from datetime import datetime
from requests_oauthlib import OAuth1Session

# Configurar timezone para Brasil
br_tz = pytz.timezone('America/Sao_Paulo')

# Inicializar tokens Twitter OAuth 1.0a (User Context)
consumer_key = os.getenv('TWITTER_API_KEY', '')
consumer_secret = os.getenv('TWITTER_API_KEY_SECRET', '')
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
    """Publica tweet usando Twitter API v2 com OAuth 1.0a User Context."""
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("❌ ERRO: Credentials do Twitter não estão definidos corretamente")
        return False
    
    try:
        # Criar sessão OAuth 1.0a User Context
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            signature_type='auth_header'
        )
        
        # URL endpoint da Twitter API v2
        url = "https://api.twitter.com/2/tweets"
        
        # Payload do tweet
        payload = {"text": content[:280]}
        
        # Fazer requisição
        response = oauth.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            tweet_id = data.get('data', {}).get('id', 'N/A')
            print(f"✅ Tweet publicado com sucesso! ID: {tweet_id}")
            return True
        elif response.status_code == 401:
            print(f"❌ ERRO 401: OAuth credentials inválidos ou expirados")
            print(f"Resposta: {response.text}")
            return False
        elif response.status_code == 403:
            print(f"❌ ERRO 403: Permissão negada - Verifique se o token tem permissão para postar")
            print(f"Resposta: {response.text}")
            return False
        else:
            print(f"❌ ERRO {response.status_code} ao publicar tweet: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro fatal ao publicar: {e}")
        raise

if __name__ == "__main__":
    print("\n🔍 Iniciando publicacao de tweet...\n")
    tweet_content = generate_tweet_content()
    print(f"Conteudo gerado: {tweet_content}")
    publish_tweet(tweet_content)
