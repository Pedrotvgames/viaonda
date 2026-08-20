from flask import Flask, request, jsonify

app = Flask(__name__)

print("="*50)
print(" INICIANDO SERVIDOR DE MONITORAMENTO DA CATRACA ")
print(" Aguardando leituras da antena M-ID10W...")
print("="*50)

@app.route('/porta_saida', methods=['POST'])
def receber_leitura_porta():
    # Recebe o JSON enviado pela antena M-ID10W
    dados = request.get_json()

    if dados:
        for leitura in dados:
            epc = leitura.get("reading_epc_hex")
            # Imprime o alerta de que o livro passou pela porta
            print(f"\n[CATRACA] ALERTA: Livro detectado na porta! EPC: {epc}")

    # Retorna sucesso para a antena
    return jsonify({"status": "recebido"}), 200

if __name__ == '__main__':
    # Roda o servidor na porta 5000
    app.run(host='0.0.0.0', port=5000)