import os
import msvcrt
import time
from datetime import datetime

pesos = {"vermelho": 3, "amarelo": 2, "verde": 1}
tempos_maximos = {"vermelho": 0, "amarelo": 30, "verde": 120}

itens = []
em_atendimento = []

def chave_ordenacao(paciente):
    peso = pesos[paciente["prioridade"]]
    idoso = 1 if paciente["idade"] >= 60 else 0
    timestamp = paciente["timestamp"]
    return (peso, idoso, -timestamp)

def checar_alertas():
    agora = time.time()
    for paciente in itens:
        if paciente.get("alerta_disparado"):
            continue
        tempo_espera = (agora - paciente["timestamp"]) / 60
        limite = tempos_maximos[paciente["prioridade"]]
        if tempo_espera >= limite:
            paciente["alerta_disparado"] = True
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║         ⚠ ALERTA DE TEMPO ⚠          ║")
            print("╠══════════════════════════════════════╣")
            print(f"║  Nome:      {paciente['nome']:<25}║")
            print(f"║  Prioridade:{paciente['prioridade']:<25}║")
            print(f"║  Tempo esp: {tempo_espera:.1f} min{'':<20}║")
            print("║                                      ║")
            print("║  Aperte qualquer tecla para fechar!  ║")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()

def main(itens):
    checar_alertas()
    os.system('cls')
    print("╔══════════════════════════════════════╗")
    print("║             HealthManager            ║")
    print("╠══════════════════════════════════════╣")
    print("║                                      ║")
    print("║       Qual você deseja acessar?      ║")
    print("║                                      ║")
    print("║  1. Lista de Atendimento             ║")
    print("║  2. Nova Triagem                     ║")
    print("║  3. Chamar Próximo Paciente          ║")
    print("║  4. Finalizar dia                    ║")
    print("║                                      ║")
    print("╚══════════════════════════════════════╝")
    print("")
    try:
        option_choose = int(input("Digite uma alternativa: "))
    except ValueError:
        option_choose = -1
    return option_choose, itens

def nova_triagem():
    os.system('cls')
    print("╔══════════════════════════════════════╗")
    print("║             Nova Triagem             ║")
    print("╠══════════════════════════════════════╣")
    print("║                                      ║")
    nome = input("║  Nome:      ")
    idade = input("║  Idade:     ")
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

    return nome, int(idade), prioridade

def chamar_proximo():
    if len(itens) == 0:
        os.system('cls')
        print("╔══════════════════════════════════════╗")
        print("║                                      ║")
        print("║  Nenhuma pessoa na fila atualmente!  ║")
        print("║  Aperte qualquer tecla para voltar!  ║")
        print("║                                      ║")
        print("╚══════════════════════════════════════╝")
        msvcrt.getch()
        return

    ordenado = sorted(itens, key=chave_ordenacao, reverse=True)
    proximo = ordenado[0]
    proximo["timestamp_atendimento"] = time.time()
    proximo["horario_atendimento"] = datetime.now().strftime("%H:%M:%S")
    proximo["status"] = "Em Atendimento"
    itens.remove(proximo)
    em_atendimento.append(proximo)

    os.system('cls')
    print("╔══════════════════════════════════════╗")
    print("║         Próximo Paciente             ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Nome:      {proximo['nome']:<25}║")
    print(f"║  Idade:     {proximo['idade']:<25}║")
    print(f"║  Prioridade:{proximo['prioridade']:<25}║")
    print(f"║  Chegada:   {proximo['horario_chegada']:<25}║")
    print(f"║  Atendimento:{proximo['horario_atendimento']:<24}║")
    print("║                                      ║")
    print("║  Aperte qualquer tecla para voltar!  ║")
    print("╚══════════════════════════════════════╝")
    msvcrt.getch()

def finalizar_dia():
    os.system('cls')
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"historico_{agora}.txt"

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
                if "timestamp_atendimento" in p:
                    espera_segundos = int(p["timestamp_atendimento"] - p["timestamp"])
                    espera_min = espera_segundos // 60
                    espera_seg = espera_segundos % 60
                    espera_str = f"{espera_min}min {espera_seg}s"
                    atendimento = p["horario_atendimento"]
                else:
                    atendimento = "Não atendido"
                    espera_str = "N/A"

                f.write(f"Nome:               {p['nome']}\n")
                f.write(f"Cor de triagem:     {p['prioridade']}\n")
                f.write(f"Horário de chegada: {p['horario_chegada']}\n")
                f.write(f"Horário atendimento:{atendimento}\n")
                f.write(f"Tempo de espera:    {espera_str}\n")
                f.write("----------------------------------------\n")

    print("╔══════════════════════════════════════╗")
    print(f"║  Arquivo salvo:                      ║")
    print(f"║  {nome_arquivo:<36}║")
    print("║  Aperte qualquer tecla para sair!    ║")
    print("╚══════════════════════════════════════╝")
    msvcrt.getch()

while True:
    option_choose, itens = main(itens)

    if option_choose == 1:
        if len(itens) == 0:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║                                      ║")
            print("║  Nenhuma pessoa na fila atualmente!  ║")
            print("║  Aperte qualquer tecla para voltar!  ║")
            print("║                                      ║")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()
        else:
            os.system('cls')
            ordenado = sorted(itens, key=chave_ordenacao, reverse=True)
            print("╔══════════════════════════════════════╗")
            print("║          Lista de Atendimento        ║")
            print("╠══════════════════════════════════════╣")
            for paciente in ordenado:
                print(f"║  Nome:      {paciente['nome']:<25}║")
                print(f"║  Idade:     {paciente['idade']:<25}║")
                print(f"║  Prioridade:{paciente['prioridade']:<25}║")
                print(f"║  Chegada:   {paciente['horario_chegada']:<25}║")
                print("╠══════════════════════════════════════╣")
            print("╚══════════════════════════════════════╝")
            msvcrt.getch()

    elif option_choose == 2:
        nome, idade, prioridade = nova_triagem()
        if prioridade is not None:
            itens.append({
                "nome": nome,
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
        finalizar_dia()
        break