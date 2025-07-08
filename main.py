# Importa as bibliotecas necessárias
import requests # Para enviar a mensagem final ao seu webhook
from flask import Flask, request, jsonify # Para criar a API

# Cria a aplicação web
app = Flask(__name__)

# --- INÍCIO DA CONFIGURAÇÃO ---
#
# COLE A URL DO WEBHOOK QUE VOCÊ PEGOU DO SEU DISCORD AQUI DENTRO DAS ASPAS
#
DESTINATION_WEBHOOK_URL = "https://discord.com/api/webhooks/1392282620888354918/U7641Igwzhv1qvI06jBqYV7uJ5Rw_-ZfVBgTa1Hf8jcfK_Bfk12gQYkMOajdItBJmxB6"
#
# --- FIM DA CONFIGURAÇÃO ---


# Esta é a rota principal, só para sabermos que o app está no ar
@app.route('/')
def home():
    return "Proxy de Webhooks do Discord está no ar e funcionando!"

# Esta é a rota que vai receber as mensagens do Discord
@app.route('/webhook-receiver', methods=['POST'])
def receive_webhook():
    # Pega os dados que o Discord enviou no formato JSON
    data = request.get_json()

    # Linha mágica para debugar: imprime tudo o que o Discord enviou no console do Replit
    print("--- DADOS RECEBIDOS ---")
    print(data)
    print("-------------------------")

    # =================================================================
    # AQUI FICA A SUA LÓGICA DE FILTRAGEM
    #
    # Exemplo de filtro: Só deixar passar mensagens que contenham a palavra "grátis"

    conteudo_da_mensagem = data.get('content', '').lower() # Pega o texto da msg, em minúsculas

    if "grátis" not in conteudo_da_mensagem:
        print("Mensagem ignorada: não continha a palavra 'grátis'.")
        return jsonify({'status': 'ignored'}), 200 # Responde ao Discord que está tudo bem, mas não faz nada.

    # Exemplo de modificação: Adicionar um título à mensagem que passou pelo filtro
    data['content'] = f"**NOVO ANÚNCIO INTERESSANTE!**\n\n{data.get('content', '')}"

    # =================================================================

    # Tenta enviar os dados (já filtrados e modificados) para o seu webhook de destino
    try:
        response = requests.post(DESTINATION_WEBHOOK_URL, json=data)
        response.raise_for_status()  # Isso vai gerar um erro se o Discord não aceitar nosso envio
        print("Mensagem encaminhada com sucesso para o seu servidor!")

    except requests.exceptions.RequestException as e:
        print(f"ERRO ao encaminhar a mensagem: {e}")
        return jsonify({'status': 'error'}), 500

    return jsonify({'status': 'success'}), 200

# Linha que faz o servidor rodar
app.run(host='0.0.0.0', port=81)
