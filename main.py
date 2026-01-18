import requests
import time

# Configurações do Banco Inter
CERT_KEY = 'caminho/para/seu/certificado.key'
CERT_CRT = 'caminho/para/seu/certificado.crt'
CLIENT_ID = 'SEU_CLIENT_ID'
CLIENT_SECRET = 'SEU_CLIENT_SECRET'

def obter_token():
    url = "https://cdpj.inter.co/oauth/v2/token"
    payload = "grant_type=client_credentials&scope=pix.read pix.write"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    response = requests.post(url, data=payload, headers=headers, 
                             cert=(CERT_CRT, CERT_KEY))
    return response.json()['access_token']

def verificar_pagamento(txid):
    token = obter_token()
    url = f"https://cdpj.inter.co/pix/v2/cob/{txid}"
    headers = {'Authorization': f'Bearer {token}'}
    
    while True:
        response = requests.get(url, headers=headers, cert=(CERT_CRT, CERT_KEY))
        status = response.json().get('status')
        
        if status == 'CONCLUIDA':
            print("✅ Pagamento recebido! Liberando ebook...")
            # Aqui você enviaria um comando para o seu Firebase
            return True
        elif status == 'EXPIRADA':
            print("❌ O tempo do PIX acabou.")
            return False
            
        print("⏳ Aguardando pagamento...")
        time.sleep(5) # Verifica a cada 5 segundos

# Exemplo de uso
# verificar_pagamento('ID_DA_COBRANCA_GERADA')
