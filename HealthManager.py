import os
import msvcrt
import time
from datetime import datetime

pesos = {"vermelho": 3, "amarelo": 2, "verde": 1}
tempos_maximos = {"vermelho": 0, "amarelo": 30, "verde": 120}

itens = []
em_atendimento = []

def chave_ordenacao(paciente):
    """
    Gera a chave de ordenação de um paciente para a fila de triagem.

    Segue o Protocolo de Manchester:
    - Prioridade mais alta (vermelho > amarelo > verde) vem primeiro.
    - Em caso de empate, pacientes idosos (>= 60 anos) têm preferência.
    - Em caso de empate total, quem chegou antes é atendido antes.

    Args:
        paciente (dict): Dicionário com os dados do paciente,
                         incluindo 'prioridade', 'idade' e 'timestamp'.

    Returns:
        tuple: Tupla (peso, idoso, -timestamp) usada pelo sorted().
    """
    peso = pesos[paciente["prioridade"]]
    idoso = 1 if paciente["idade"] >= 60 else 0
    timestamp = paciente["timestamp"]
    return (peso, idoso, -timestamp)


def checar_alertas():
    """
    Verifica se algum paciente na fila ultrapassou o tempo máximo de espera.

    Percorre a lista de pacientes aguardando e, para cada um, calcula
    o tempo decorrido desde a chegada. Se o tempo ultrapassar o limite
    definido para a prioridade (vermelho: 0 min, amarelo: 30 min,
    verde: 120 min), exibe um alerta visual no terminal e aguarda
    confirmação do usuário antes de prosseguir.

    O campo 'alerta_disparado' evita que o mesmo alerta seja exibido
    mais de uma vez para o mesmo paciente.
    """
    agora = time.time()
    for paciente in itens:
        if paciente.get("alerta_disparado"):
            continue
        tempo_espera = (agora - paciente["timestamp"]) / 60
        limite = tempos_maximos[paciente["prioridade"]]
        if tempo_espera >= limite:
            paciente["alerta_disparado"] = True
            os.system('cls' if os.name == 'nt' else 'clear')
            print("╔══════════════════════════════════════╗")
            print("║         ⚠ ALERTA DE TEMPO ⚠          ║")
            print("╠══════════════════════════════════════╣")
            print(f"║  Nome:      {paciente['nome']:<25}║")
            print(f"║  Prioridade: {paciente['prioridade']:<24}║")
            print(f"║  Tempo esp: {tempo_espera:.1f} min{'':<18}║")
            print("║                                      ║")
            print("║  Aperte qualquer tecla para fechar!  ║")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()


def main(itens):
    """
    Exibe o menu principal e captura a escolha do usuário.

    Antes de renderizar o menu, chama checar_alertas() para verificar
    se há pacientes com tempo de espera excedido. Em seguida, limpa
    o terminal e exibe as opções disponíveis.

    Args:
        itens (list): Lista atual de pacientes na fila de espera.

    Returns:
        tuple: (option_choose, itens), onde option_choose é um inteiro
               correspondente à opção selecionada, ou -1 em caso de
               entrada inválida.
    """
    checar_alertas()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════╗")
    print("║             HealthManager            ║")
    print("╠══════════════════════════════════════╣")
    print("║                                      ║")
    print("║       Qual você deseja acessar?      ║")
    print("║                                      ║")
    print("║  1. Lista de Atendimento             ║")
    print("║  2. Nova Triagem                     ║")
    print("║  3. Chamar Próximo Paciente          ║")
    print("║  4. Atualizar Registro               ║")
    print("║  5. Finalizar dia                    ║")
    print("║                                      ║")
    print("╚══════════════════════════════════════╝")
    print("")
    try:
        option_choose = int(input("Digite uma alternativa: "))
    except ValueError:
        option_choose = -1
    return option_choose, itens


def nova_triagem():
    """
    Coleta os dados de um novo paciente para entrada na fila de triagem.

    Solicita ao operador o nome, sobrenome, idade e nível de prioridade
    do paciente. A idade é validada em loop até que um valor inteiro
    positivo seja informado. A prioridade é mapeada de um número
    (1, 2 ou 3) para a cor correspondente do Protocolo de Manchester.

    O sobrenome é armazenado separadamente para permitir desambiguação
    em casos onde dois pacientes possuam o mesmo nome.

    Returns:
        tuple: (nome, sobrenome, idade, prioridade), onde:
            - nome (str): Primeiro nome do paciente.
            - sobrenome (str): Sobrenome do paciente.
            - idade (int): Idade do paciente.
            - prioridade (str | None): 'vermelho', 'amarelo', 'verde',
              ou None se a opção digitada for inválida.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════╗")
    print("║             Nova Triagem             ║")
    print("╠══════════════════════════════════════╣")
    print("║                                      ║")
    while True:
        nome = str(input("║  Nome:      "))
        if len(nome) == 0:
            print("║ Nome inválido! Tente novamente!")
        else:
            break
    while True:
        sobrenome = str(input("║  Sobrenome: "))
        if len(sobrenome) == 0:
            print("║ Sobrenome inválido! Tente novamente!")
        else:
            break
    while True:
        try:
            idade = int(input("║  Idade:     "))
            if idade < 0:
                print("║  Idade inválida! Digite um valor positivo.")
                continue
            break
        except ValueError:
            print("║  Digite apenas números!")
    print("║                                      ║")
    print("║  Prioridade:                         ║")
    print("║  1. Vermelho                         ║")
    print("║  2. Amarelo                          ║")
    print("║  3. Verde                            ║")
    print("║                                      ║")
    print("╚══════════════════════════════════════╝")
    try:
        opcao = int(input("Digite a prioridade: "))
    except ValueError:
        opcao = -1

    prioridades = {1: "vermelho", 2: "amarelo", 3: "verde"}
    prioridade = prioridades.get(opcao, None)

    return nome, sobrenome, int(idade), prioridade


def chamar_proximo():
    """
    Chama o próximo paciente da fila de acordo com a ordenação de triagem.

    Ordena a lista de espera usando chave_ordenacao() e move o paciente
    de maior prioridade para a lista 'em_atendimento'. Registra o
    horário e timestamp de início do atendimento e exibe as informações
    do paciente no terminal, incluindo nome e sobrenome.

    Caso a fila esteja vazia, exibe uma mensagem informativa e retorna
    sem realizar nenhuma ação.
    """
    if len(itens) == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔══════════════════════════════════════╗")
        print("║                                      ║")
        print("║  Nenhuma pessoa na fila atualmente!  ║")
        print("║  Aperte qualquer tecla para voltar!  ║")
        print("║                                      ║")
        print("╚══════════════════════════════════════╝")
        msvcrt.getch()
        return

    ordenado = sorted(itens, key=chave_ordenacao, reverse=True)
    if len(ordenado) >= 1:
        proximo = ordenado[0]
    proximo["timestamp_atendimento"] = time.time()
    proximo["horario_atendimento"] = datetime.now().strftime("%H:%M:%S")
    proximo["status"] = "Em Atendimento"
    itens.remove(proximo)
    em_atendimento.append(proximo)

    nome_completo = f"{proximo['nome']} {proximo['sobrenome']}"
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════╗")
    print("║         Próximo Paciente             ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Nome:      {nome_completo:<25}║")
    print(f"║  Idade:     {proximo['idade']:<25}║")
    print(f"║  Prioridade:{proximo['prioridade']:<25}║")
    print(f"║  Chegada:   {proximo['horario_chegada']:<25}║")
    print(f"║  Atendimento:{proximo['horario_atendimento']:<24}║")
    print("║                                      ║")
    print("║  Aperte qualquer tecla para voltar!  ║")
    print("╚══════════════════════════════════════╝")
    msvcrt.getch()


def atualizar_registro():
    """
    Permite editar os dados de um paciente que está na fila de espera.

    Busca pelo nome (sem distinção de maiúsculas/minúsculas) e coleta
    todos os pacientes que correspondam. Se houver mais de um com o
    mesmo nome, solicita o sobrenome para desambiguação antes de
    prosseguir. As opções de edição são: nome, sobrenome, idade ou
    prioridade.

    A idade é revalidada em loop. Ao alterar a prioridade, o campo
    'alerta_disparado' é resetado para que o novo limite de tempo
    seja monitorado corretamente. O .get("sobrenome", "") garante
    compatibilidade com registros cadastrados sem sobrenome.

    Caso a fila esteja vazia ou o paciente não seja encontrado,
    exibe uma mensagem informativa e retorna sem realizar alterações.
    """
    if len(itens) == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔══════════════════════════════════════╗")
        print("║                                      ║")
        print("║  Nenhuma pessoa na fila atualmente!  ║")
        print("║  Aperte qualquer tecla para voltar!  ║")
        print("║                                      ║")
        print("╚══════════════════════════════════════╝")
        msvcrt.getch()
        return

    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════╗")
    print("║         Atualizar Registro           ║")
    print("╠══════════════════════════════════════╣")
    nome_busca = input("║  Nome do paciente: ").strip().lower()
    matches = [p for p in itens if p["nome"].lower() == nome_busca]

    if not matches:
        print("║                                      ║")
        print("║  Paciente não encontrado!            ║")
        print("║  Aperte qualquer tecla para voltar!  ║")
        print("╚══════════════════════════════════════╝")
        msvcrt.getch()
        return

    if len(matches) > 1:
        sobrenome_busca = input("║  Há mais de um paciente com esse nome.\n║  Digite o sobrenome: ").strip().lower()
        matches = [p for p in matches if p.get("sobrenome", "").lower() == sobrenome_busca]

        if not matches:
            print("║                                      ║")
            print("║  Sobrenome não encontrado!           ║")
            print("║  Aperte qualquer tecla para voltar!  ║")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()
            return

    paciente = matches[0]

    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════╗")
    print("║         Atualizar Registro           ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Paciente encontrado: {paciente['nome']:<15}║")
    print("║                                      ║")
    print("║  O que deseja editar?                ║")
    print("║  1. Nome                             ║")
    print("║  2. Sobrenome                        ║")
    print("║  3. Idade                            ║")
    print("║  4. Prioridade                       ║")
    print("║                                      ║")
    print("╚══════════════════════════════════════╝")

    try:
        campo = int(input("Digite uma alternativa: "))
    except ValueError:
        campo = -1

    if campo == 1:
        novo_nome = input("║  Novo nome: ").strip()
        if novo_nome:
            paciente["nome"] = novo_nome

    elif campo == 2:
        novo_sobrenome = input("║  Novo sobrenome: ").strip()
        if novo_sobrenome:
            paciente["sobrenome"] = novo_sobrenome

    elif campo == 3:
        while True:
            try:
                nova_idade = int(input("║  Nova idade: "))
                if nova_idade < 0:
                    print("║  Idade inválida! Digite um valor positivo.")
                    continue
                paciente["idade"] = nova_idade
                break
            except ValueError:
                print("║  Digite apenas números!")

    elif campo == 4:
        print("║  1. Vermelho  2. Amarelo  3. Verde   ║")
        try:
            opcao = int(input("║  Nova prioridade: "))
        except ValueError:
            opcao = -1
        prioridades = {1: "vermelho", 2: "amarelo", 3: "verde"}
        nova_prioridade = prioridades.get(opcao, None)
        if nova_prioridade:
            paciente["prioridade"] = nova_prioridade
            paciente["alerta_disparado"] = False

    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔══════════════════════════════════════╗")
    print("║  Registro atualizado com sucesso!    ║")
    print("║  Aperte qualquer tecla para voltar!  ║")
    print("╚══════════════════════════════════════╝")
    msvcrt.getch()
    return


def finalizar_dia():
    """
    Encerra o turno e gera um relatório em arquivo .txt com o histórico
    de todos os pacientes atendidos e não atendidos no dia.

    Cria o diretório 'registros/' caso não exista e salva o arquivo com
    o nome no formato 'historico_AAAA-MM-DD_HH-MM-SS.txt'. Para cada
    paciente, registra nome completo (nome + sobrenome), cor de triagem,
    horário de chegada, horário de atendimento e tempo de espera
    calculado. Pacientes que não foram chamados recebem 'Não atendido'
    e 'N/A' nos campos correspondentes.

    Ao final, exibe o caminho do arquivo salvo e aguarda confirmação
    do usuário antes de encerrar o programa.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("registros", exist_ok=True)
    nome_arquivo = f"registros/historico_{agora}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("========================================\n")
        f.write("        HISTÓRICO DO DIA - HealthManager\n")
        f.write(f"        Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("========================================\n\n")

        todos = em_atendimento + itens
        if len(todos) == 0:
            f.write("Nenhum paciente registrado hoje.\n")
        else:
            for p in todos:
                nome_completo = f"{p['nome']} {p.get('sobrenome', '')}".strip()
                if "timestamp_atendimento" in p:
                    espera_segundos = int(p["timestamp_atendimento"] - p["timestamp"])
                    espera_min = espera_segundos // 60
                    espera_seg = espera_segundos % 60
                    espera_str = f"{espera_min}min {espera_seg}s"
                    atendimento = p["horario_atendimento"]
                else:
                    atendimento = "Não atendido"
                    espera_str = "N/A"

                f.write(f"Nome:               {nome_completo}\n")
                f.write(f"Cor de triagem:     {p['prioridade']}\n")
                f.write(f"Horário de chegada: {p['horario_chegada']}\n")
                f.write(f"Horário atendimento:{atendimento}\n")
                f.write(f"Tempo de espera:    {espera_str}\n")
                f.write("----------------------------------------\n")

    print("╔══════════════════════════════════════╗")
    print("║  Arquivo salvo:                      ║")
    print(f"║  {nome_arquivo:<36}║")
    print("║  Aperte qualquer tecla para sair!    ║")
    print("╚══════════════════════════════════════╝")
    msvcrt.getch()


while True:
    option_choose, itens = main(itens)

    if option_choose == 1:
        if len(itens) == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("╔══════════════════════════════════════╗")
            print("║                                      ║")
            print("║  Nenhuma pessoa na fila atualmente!  ║")
            print("║  Aperte qualquer tecla para voltar!  ║")
            print("║                                      ║")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            ordenado = sorted(itens, key=chave_ordenacao, reverse=True)
            print("╔══════════════════════════════════════╗")
            print("║          Lista de Atendimento        ║")
            print("╠══════════════════════════════════════╣")
            for paciente in ordenado:
                nome_completo = f"{paciente['nome']} {paciente.get('sobrenome', '')}".strip()
                print(f"║  Nome:      {nome_completo:<25}║")
                print(f"║  Idade:     {paciente['idade']:<25}║")
                print(f"║  Prioridade:{paciente['prioridade']:<25}║")
                print(f"║  Chegada:   {paciente['horario_chegada']:<25}║")
                print("╠══════════════════════════════════════╣")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()

    elif option_choose == 2:
        nome, sobrenome, idade, prioridade = nova_triagem()
        if prioridade is not None:
            duplicado = any(
                p["nome"].lower() == nome.lower() and
                p.get("sobrenome", "").lower() == sobrenome.lower()
                for p in itens
            )
            if duplicado:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("╔══════════════════════════════════════╗")
                print("║  Paciente já cadastrado na fila!     ║")
                print("║  Aperte qualquer tecla para voltar!  ║")
                print("╚══════════════════════════════════════╝")
                msvcrt.getch()
            else:
                itens.append({
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "idade": idade,
                    "prioridade": prioridade,
                    "timestamp": time.time(),
                    "horario_chegada": datetime.now().strftime("%H:%M:%S"),
                    "status": "Em Espera",
                    "alerta_disparado": False
                })
                

    elif option_choose == 3:
        chamar_proximo()
    elif option_choose == 4:
        atualizar_registro()
    elif option_choose == 5:
        finalizar_dia()
        break
