#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
from requests_oauthlib import OAuth1Session

def test_twitter_credentials():
    """Testa se as credenciais do Twitter API v2 estão válidas"""
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN', '')
    
    if not bearer_token:
        print("❌ ERRO: TWITTER_BEARER_TOKEN não está definido")
        return False
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2TestScript"
    }
    
    try:
        # Testa a conexão com a API do Twitter
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent?query=test&max_results=10",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Twitter Bearer Token válido!")
            return True
        elif response.status_code == 401:
            print("❌ ERRO 401: Twitter Bearer Token inválido ou expirado")
            return False
        else:
            print(f"❌ ERRO {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERRO ao testar Twitter: {e}")
        return False

def test_openai_credentials():
    """Testa se as credenciais do OpenAI estão válidas"""
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not api_key:
        print("❌ ERRO: OPENAI_API_KEY não está definido")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ OpenAI API Key válida!")
            return True
        elif response.status_code == 401:
            print("❌ ERRO 401: OpenAI API Key inválida ou expirada")
            return False
        elif response.status_code == 429:
            print("❌ ERRO 429: Quota de OpenAI excedida")
            return False
        else:
            print(f"❌ ERRO {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERRO ao testar OpenAI: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 Testando credenciais...\n")
    twitter_ok = test_twitter_credentials()
    openai_ok = test_openai_credentials()
    
    print("\n" + "="*50)
    if twitter_ok and openai_ok:
        print("✅ Todas as credenciais estão válidas!")
    else:
        print("❌ Algumas credenciais estão inválidas. Verifique acima.")
    print("="*50 + "\n")
