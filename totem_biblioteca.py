import requests
import time

# IP da antena M-ID10W configurada na porta da biblioteca
IP_ANTENA_SAIDA = "192.168.0.10"


def enviar_para_antena(epc, acao):
    """
    Comunica com a M-ID10W para liberar (add) ou bloquear (remove) o livro.
    """
    url = f"http://{IP_ANTENA_SAIDA}:8080/blackList?{acao}={epc}"

    try:
        resposta = requests.get(url, timeout=3)
        dados = resposta.json()

        if resposta.status_code == 200:
            print(f"[SUCESSO] Comando executado! Resposta da Antena: {dados.get('msg')}")
        else:
            print("[ERRO] A antena não respondeu corretamente.")

    except Exception as e:
        print(f"[FALHA DE REDE] Não foi possível comunicar com a antena ({IP_ANTENA_SAIDA}): {e}")


def tela_simulacao_totem():
    """
    Menu interativo que simula o Totem.
    """
    while True:
        print("\n" + "=" * 50)
        print("   SISTEMA DE EMPRÉSTIMO DE LIVROS - BIBLIOTECA   ")
        print("=" * 50)

        print("1. Fazer Empréstimo (Liberar na saída)")
        print("2. Fazer Devolução (Bloquear na saída)")
        print("3. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            print("\n--- [ TELA DE EMPRÉSTIMO ] ---")
            epc_livro = input("Aproxime o livro do leitor de mesa (M-ID10S): ").strip()

            if epc_livro:
                print(f"Livro lido: {epc_livro}")
                input("Pressione [ENTER] no teclado para CONFIRMAR o empréstimo...")

                print("Salvando no banco de dados...")
                time.sleep(0.5)

                print("Avisando a catraca para LIBERAR a saída...")
                enviar_para_antena(epc_livro, acao="add")

        elif opcao == '2':
            print("\n--- [ TELA DE DEVOLUÇÃO ] ---")
            epc_livro = input("Aproxime o livro do leitor de mesa (M-ID10S): ").strip()

            if epc_livro:
                print(f"Livro lido: {epc_livro}")
                input("Pressione [ENTER] no teclado para CONFIRMAR a devolução...")

                print("Atualizando banco de dados...")
                time.sleep(0.5)

                print("Avisando a catraca para BLOQUEAR a saída...")
                enviar_para_antena(epc_livro, acao="remove")

        elif opcao == '3':
            print("Encerrando o sistema do Totem...")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == '__main__':
    tela_simulacao_totem()