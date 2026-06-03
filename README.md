
# Especificação de Requisitos de Software — HealthManager
> Sistema de Triagem Hospitalar baseado no Protocolo de Manchester

## 1. Introdução

### 1.1 Propósito

Este documento especifica os requisitos funcionais, não funcionais e as regras de negócio para o sistema **HealthManager**, um software de triagem hospitalar baseado no Protocolo de Manchester para otimização do fluxo de atendimento.

### 1.2 Escopo do Sistema

O sistema controlará a recepção e a triagem, permitindo:

- Classificação de risco por cores (Vermelho, Amarelo, Verde)
- Ordenação automatizada da fila por gravidade e idade
- Controle de tempo de atendimento através de alertas visuais
- Atualização e edição de registros de pacientes já triados
- Exportação diária dos dados em arquivo `.txt` na pasta `registros/`

---

## 2. Descrição Geral

### 2.1 Funções do Produto

O HealthManager atuará na recepção do hospital, sendo operado por enfermeiras na triagem e visualizado por médicos e gestores. O sistema substitui o controle manual ou por ordem de chegada simples por um algoritmo de priorização dinâmica.

### 2.2 Características dos Usuários

| Perfil | Descrição |
|---|---|
| **Enfermeira da Triagem** | Usuário operacional; necessita de interface rápida e de poucos cliques. |
| **Médico / Profissional de Saúde** | Usuário final da fila; focado na chamada do próximo paciente. |
| **Gestor / Administrador** | Usuário que monitora gargalos e exporta relatórios. |

---

## 3. Requisitos de Sistema

As necessidades dos stakeholders são mapeadas no formato de histórias de usuário, acompanhadas de seus critérios de aceitação e identificadores únicos.

### 3.1 Requisitos Funcionais (RF)

---

#### [RF-01] Cadastro de Paciente e Triagem

> **User Story:** Como *Enfermeira da Triagem*, eu quero cadastrar o paciente com nome, idade, cor do Protocolo de Manchester e horário automático de chegada, para identificar o nível de risco de cada paciente logo na recepção.

**Critérios de Aceitação:**

- O sistema deve registrar o carimbo de data/hora (`timestamp`) no momento exato do salvamento.
- As cores permitidas devem ser estritamente: **Vermelho**, **Amarelo** ou **Verde** (mapeadas nos valores 3, 2 e 1, respectivamente).
- A idade deve ser validada como número inteiro positivo; valores negativos ou não numéricos devem ser rejeitados com mensagem de erro.
- O campo `status` do paciente deve ser iniciado como `"Em Espera"` e o campo `alerta_disparado` como `False`.
- Prioridade inválida (fora das opções 1, 2 ou 3) deve ser rejeitada, não adicionando o paciente à fila.

**Prioridade:** `Alta`

---

#### [RF-02] Exibição da Fila Atualizada

> **User Story:** Como *Equipe Hospitalar*, eu quero visualizar a fila de espera atualizada em tempo real a cada nova triagem, para saber exatamente quem é o próximo a ser chamado conforme as regras de prioridade.

**Critérios de Aceitação:**

- A lista de atendimento deve ser exibida já ordenada conforme as regras de negócio [RN-01] e [RN-02].
- A exibição deve mostrar nome, idade, prioridade e horário de chegada de cada paciente.
- Se a fila estiver vazia, o sistema deve exibir a mensagem `"Nenhuma pessoa na fila atualmente!"` e aguardar confirmação do usuário.

**Prioridade:** `Alta`

---

#### [RF-03] Chamar Próximo Paciente

> **User Story:** Como *Profissional de Saúde*, eu quero acionar um comando para chamar o próximo paciente da fila, para iniciar o atendimento dele, registrá-lo no sistema e removê-lo da espera.

**Critérios de Aceitação:**

- O sistema deve registrar o horário de início do atendimento (`horario_atendimento`) e o timestamp correspondente (`timestamp_atendimento`).
- O paciente chamado deve sair do status `"Em Espera"` e ser movido para a lista `em_atendimento`.
- O próximo paciente deve ser determinado pela chave de ordenação conforme [RN-01] e [RN-02]: peso da prioridade → idoso → ordem de chegada.
- Se a fila estiver vazia, o sistema deve exibir mensagem informativa e aguardar confirmação.

**Prioridade:** `Alta`

---

#### [RF-04] Alerta de Tempo Limite (Pop-Up)

> **User Story:** Como *Gestor do Hospital*, eu quero receber um alerta em formato de pop-up quando um paciente ultrapassar o tempo máximo permitido de espera, para tomar providências rápidas e evitar riscos à saúde.

**Critérios de Aceitação:**

- O alerta deve ser verificado automaticamente a cada carregamento do menu principal (via `checar_alertas()`).
- O alerta deve interromper a tela atual exibindo nome, prioridade e tempo de espera já decorrido (em minutos, com uma casa decimal).
- O alerta só é disparado **uma vez por paciente**; após ser exibido, o campo `alerta_disparado` é marcado como `True`, impedindo repetições.
- O alerta deve aguardar confirmação do usuário (qualquer tecla) antes de retornar ao menu.

**Prioridade:** `Média`

---

#### [RF-05] Atualização de Registro

> **User Story:** Como *Enfermeira da Triagem*, eu quero editar os dados de um paciente já cadastrado na fila (nome, idade ou prioridade), para corrigir informações inseridas de forma incorreta durante a triagem.

**Critérios de Aceitação:**

- A busca do paciente deve ser feita pelo nome, sem distinção de maiúsculas/minúsculas.
- Os campos editáveis são: **Nome**, **Idade** e **Prioridade**.
- Ao atualizar a prioridade de um paciente, o campo `alerta_disparado` deve ser resetado para `False`, reiniciando a contagem de alerta com base na nova cor.
- Se o paciente não for encontrado, o sistema deve exibir mensagem de erro e retornar ao menu.
- A validação dos dados segue as mesmas regras do [RF-01] (idade positiva, prioridade válida).

**Prioridade:** `Média`

---

#### [RF-06] Exportação de Histórico Diário

> **User Story:** Como *Administrador do Sistema*, eu quero exportar os dados de atendimento do dia em um arquivo TXT ao fechar o turno, para manter um backup físico e auditar os tempos de espera do hospital.

**Critérios de Aceitação:**

- O arquivo deve ser salvo automaticamente na pasta `registros/` com nome no formato `historico_AAAA-MM-DD_HH-MM-SS.txt`.
- O arquivo deve conter, para cada paciente: Nome, Cor de triagem, Horário de chegada, Horário de atendimento e Tempo total de espera (em minutos e segundos).
- Pacientes não atendidos devem ter os campos de atendimento registrados como `"Não atendido"` e `"N/A"`.
- O arquivo deve incluir um cabeçalho com a data e hora de geração.
- Após a exportação, o sistema deve encerrar o programa.

**Prioridade:** `Baixa`

---

### 3.2 Requisitos Não Funcionais (RNF)

---

#### [RNF-01] Desempenho e Fluidez

> **User Story:** Como *Enfermeira da Triagem*, eu quero que o sistema processe as triagens e atualize a fila em menos de 1 segundo, para que o sistema não trave e a recepção não fique congestionada.

**Métrica / Critério:**

- Tempo de resposta das requisições de ordenação da fila **≤ 1,0 segundo** sob carga normal de uso.

**Prioridade:** `Alta`

---

#### [RNF-02] Usabilidade e Menu Intuitivo

> **User Story:** Como *Usuário do Sistema*, eu quero um menu simples, intuitivo e com cores de prioridade bem destacadas, para operar o software sem necessidade de treinamentos complexos.

**Métrica / Critério:**

- Fluxo de triagem completo em no máximo **3 entradas** a partir da tela inicial.
- O menu principal deve apresentar todas as opções numeradas e acessíveis por entrada direta.
- Interface em modo texto (terminal) com bordas em ASCII art para melhor legibilidade.
- Cores acessíveis com alto contraste para visualização em monitores simples.

**Prioridade:** `Média`

---

## 4. Regras de Negócio (RN)

Conforme a norma IEEE 29148, as regras de negócio guiam a lógica do código que processa os requisitos funcionais descritos na seção 3.

---

### [RN-01] Ordenação por Gravidade (Protocolo de Manchester)

A ordenação primária da fila deve ser baseada estritamente no grau de risco determinado pelas cores:

| Cor | Nível | Peso |
|---|---|---|
| 🔴 Vermelho | Emergência | 3 (maior) |
| 🟡 Amarelo | Urgente | 2 |
| 🟢 Verde | Pouco Urgente | 1 (menor) |

> Nenhum paciente de cor inferior pode ser chamado se houver um paciente de cor superior aguardando.

---

### [RN-02] Prioridade para Idosos (≥ 60 Anos)

Dentro de uma mesma cor, pacientes com idade igual ou superior a 60 anos possuem prioridade sobre os não-idosos. A chave de ordenação é uma tupla de três critérios avaliados com `reverse=True`:

```python
def chave_ordenacao(paciente):
    peso      = pesos[paciente["prioridade"]]          # 1º: peso da cor
    idoso     = 1 if paciente["idade"] >= 60 else 0    # 2º: é idoso?
    timestamp = paciente["timestamp"]                   # 3º: hora de chegada
    return (peso, idoso, -timestamp)                    # -timestamp = quem chegou antes vem primeiro
```

**Critério de desempate:** se dois pacientes tiverem o mesmo peso e mesma categoria de idade, o que chegou **primeiro** (menor `timestamp` → maior `-timestamp`) é chamado antes.

---

### [RN-03] Tempos Máximos para Disparo de Alerta

O gatilho para o pop-up de alerta definido no [RF-04] segue as métricas abaixo. O tempo é calculado em minutos a partir do `timestamp` de chegada do paciente:

| Cor | Tempo Máximo em Fila | Comportamento |
|---|---|---|
| 🔴 Vermelho | 0 minutos | Alerta imediato ao cadastrar |
| 🟡 Amarelo | 30 minutos | Pop-up após 30 min na fila |
| 🟢 Verde | 120 minutos | Pop-up após 120 min na fila |

O alerta é verificado via `checar_alertas()` a cada retorno ao menu principal. Cada alerta é disparado no máximo **uma vez por paciente**; ao alterar a prioridade via [RF-05], o `alerta_disparado` é resetado para contemplar os novos limites de tempo da cor atualizada.
