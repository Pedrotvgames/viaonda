import requests
import time
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)


# ==========================================
# 1. SERVIDOR FLASK (Recebe dados da antena)
# ==========================================
@app.route('/porta_saida', methods=['POST'])
def receber_leitura_porta():
    dados = request.get_json()

    if dados:
        for leitura in dados:
            epc = leitura.get("reading_epc_hex")
            print(f"\n[CATRACA] ALERTA: Livro detectado na porta! EPC: {epc}")

    return jsonify({"status": "recebido"}), 200


def iniciar_servidor_flask():
    """Função para rodar o servidor em uma Thread separada"""
    # debug=False e use_reloader=False são importantes para rodar em thread sem bugar o terminal
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


# ==========================================
# 2. SIMULAÇÃO DO TOTEM (Envia para a antena)
# ==========================================
IP_ANTENA_SAIDA = "192.168.0.10"  # <-- Confirmando: o IP voltou para o padrão de fábrica. Certifique-se de que a antena está neste IP mesmo.


def enviar_para_antena(epc, acao):
    url = f"http://{IP_ANTENA_SAIDA}:8080/blackList?{acao}={epc}"

    try:
        resposta = requests.get(url, timeout=3)
        dados = resposta.json()

        if resposta.status_code == 200:
            print(f"[SUCESSO] Resposta da Antena: {dados.get('msg')}")
        else:
            print("[ERRO] A antena não respondeu corretamente.")

    except Exception as e:
        print(f"[FALHA DE REDE] Não foi possível comunicar com a antena ({IP_ANTENA_SAIDA}): {e}")


def tela_simulacao_totem():
    while True:
        print("\n" + "=" * 50)
        print("   SISTEMA DE EMPRÉSTIMO DE LIVROS - BIBLIOTECA   ")
        print("=" * 50)

        print("1. Fazer Empréstimo (Liberar na saída)")
        print("2. Fazer Devolução (Bloquear na saída)")
        print("3. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            print("\n[ TELA DE EMPRÉSTIMO ]")
            epc_livro = input("Aproxime o livro do leitor de mesa (M-ID10S): ").strip()

            if epc_livro:
                print(f"\nLivro lido: {epc_livro}")
                input("Pressione [ENTER] no teclado para CONFIRMAR o empréstimo...")
                print("Enviando comando para a antena da porta...")
                enviar_para_antena(epc_livro, acao="add")

        elif opcao == '2':
            print("\n[ TELA DE DEVOLUÇÃO ]")
            epc_livro = input("Aproxime o livro do leitor de mesa (M-ID10S): ").strip()

            if epc_livro:
                print(f"\nLivro lido: {epc_livro}")
                input("Pressione [ENTER] no teclado para CONFIRMAR a devolução...")
                print("Enviando comando para a antena da porta...")
                enviar_para_antena(epc_livro, acao="remove")

        elif opcao == '3':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")


# ==========================================
# 3. INÍCIO DO PROGRAMA
# ==========================================
if __name__ == '__main__':
    # Cria uma thread (processo paralelo) para o servidor Flask
    thread_servidor = threading.Thread(target=iniciar_servidor_flask)
    # Define como 'daemon' para que a thread feche automaticamente quando você sair do menu
    thread_servidor.daemon = True
    thread_servidor.start()

    # Dá 1 segundo para o Flask ligar antes de imprimir o menu na tela
    time.sleep(1)

    # Inicia o menu interativo no processo principal
    tela_simulacao_totem()