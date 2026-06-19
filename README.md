# Especificação de Requisitos — HealthManager
> Sistema de triagem hospitalar baseado no Protocolo de Manchester

---

## 0. Histórico de Versões

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 29/05/2025 | Versão inicial | Eduardo e Letícia |
| 1.1 | 03/06/2025 | Adicionado RF-05, detalhamento das regras de negócio e tempos de alerta | Eduardo e Letícia |
| 1.2 | 12/06/2025 | Adicionado campo sobrenome (RF-01, RF-05), desambiguação por sobrenome, validação de duplicata e nova regra RN-04 | Eduardo e Letícia |
| 1.2.1 | 19/06/2025 | Adicionando compatibilidade ao Linux | Eduardo |


---

## 1. Introdução

### 1.1 O que é esse documento

Esse documento descreve tudo que o sistema **HealthManager** precisa ter e fazer. Ele foi feito para organizar as ideias antes de começar a programar, deixando claro o que é prioridade e o que cada parte do sistema deve fazer.

### 1.2 O que o sistema faz

O HealthManager é um sistema de triagem hospitalar. Em vez de atender as pessoas por ordem de chegada, ele organiza a fila por gravidade, usando as cores do Protocolo de Manchester. O sistema consegue:

- Classificar pacientes por cor de risco (Vermelho, Amarelo ou Verde)
- Organizar a fila automaticamente por gravidade e idade
- Emitir alertas quando um paciente espera tempo demais
- Editar os dados de um paciente que já foi cadastrado
- Exportar um relatório do dia em arquivo de texto

---

## 2. Sobre o sistema

### 2.1 Funções principais

O sistema vai ser usado na recepção do hospital. As enfermeiras fazem a triagem, os médicos chamam os pacientes e os gestores acompanham os atendimentos. A ideia é substituir o controle manual (ou por ordem de chegada) por um sistema que prioriza quem está mais em risco.

### 2.2 Quem vai usar

| Perfil | Como usa o sistema |
|---|---|
| **Enfermeira da Triagem** | Cadastra os pacientes e preenche os dados da triagem |
| **Médico / Profissional de Saúde** | Chama o próximo paciente da fila |
| **Gestor / Administrador** | Acompanha a fila e exporta o relatório do dia |

---

## 3. Requisitos

Os requisitos foram escritos no formato de **histórias de usuário**, que é uma forma de descrever o que cada tipo de usuário precisa do sistema e por quê.

### 3.1 O que o sistema precisa fazer (Requisitos Funcionais)

---

#### [RF-01] Cadastrar paciente

> **História:** Como *enfermeira da triagem*, quero cadastrar o paciente com nome, sobrenome, idade, cor de risco e horário de chegada, para registrar as informações dele logo na entrada.

**O sistema deve:**

- Salvar automaticamente o horário exato em que o cadastro foi feito
- Aceitar só as cores **Vermelho**, **Amarelo** ou **Verde**
- Coletar nome e sobrenome separadamente para permitir desambiguação quando dois pacientes tiverem o mesmo nome
- Validar a idade (só números positivos; se digitar errado, pede de novo — ver RN-04)
- Começar o status do paciente como "Em Espera"
- Não cadastrar o paciente se a cor de risco for inválida
- Verificar se já existe um paciente com o mesmo nome e sobrenome na fila; se houver duplicata, exibir aviso e cancelar o cadastro

**Prioridade:** `Alta`

---

#### [RF-02] Mostrar a fila de espera

> **História:** Como *equipe hospitalar*, quero ver a fila atualizada com os pacientes em ordem de prioridade, para saber quem deve ser chamado primeiro.

**O sistema deve:**

- Mostrar a fila já ordenada seguindo as regras de prioridade
- Exibir nome completo (nome + sobrenome), idade, cor e horário de chegada de cada paciente
- Se não tiver ninguém na fila, mostrar uma mensagem avisando

**Prioridade:** `Alta`

---

#### [RF-03] Chamar o próximo paciente

> **História:** Como *profissional de saúde*, quero chamar o próximo da fila, para começar o atendimento e registrar o horário no sistema.

**O sistema deve:**

- Registrar o horário em que o atendimento começou
- Tirar o paciente da fila e mover ele para "Em Atendimento"
- Escolher o próximo paciente seguindo as regras de prioridade (cor, idoso, chegada)
- Exibir nome completo (nome + sobrenome), idade, cor, horário de chegada e horário de início do atendimento
- Se a fila estiver vazia, mostrar uma mensagem avisando

**Prioridade:** `Alta`

---

#### [RF-04] Alertar quando o tempo de espera estourar

> **História:** Como *gestor do hospital*, quero receber um alerta quando um paciente esperar mais do que o permitido, para conseguir agir rápido e evitar riscos.

**O sistema deve:**

- Verificar os tempos toda vez que voltar para o menu principal
- Mostrar um aviso em tela cheia com o nome, cor e tempo de espera do paciente
- Disparar o alerta só uma vez por paciente (não fica repetindo)
- Esperar o usuário apertar uma tecla para fechar o aviso

**Prioridade:** `Média`

---

#### [RF-05] Editar cadastro de paciente

> **História:** Como *enfermeira da triagem*, quero poder editar os dados de um paciente que já está na fila, para corrigir alguma informação errada.

**O sistema deve:**

- Buscar o paciente pelo nome (sem diferenciar maiúscula de minúscula)
- Se houver mais de um paciente com o mesmo nome, solicitar o sobrenome para desambiguação antes de prosseguir
- Permitir editar: nome, sobrenome, idade ou cor de risco
- Se a cor for alterada, resetar o alerta para contar o tempo do zero com a nova cor
- Se o paciente não for encontrado, mostrar mensagem de erro
- Validar os dados da mesma forma que no cadastro

**Prioridade:** `Média`

---

#### [RF-06] Exportar relatório do dia

> **História:** Como *administrador*, quero exportar os dados de atendimento do dia em um arquivo de texto ao fechar o turno, para ter um backup e poder conferir os tempos depois.

**O sistema deve:**

- Salvar o arquivo na pasta `registros/` com o nome no formato `historico_AAAA-MM-DD_HH-MM-SS.txt`
- Incluir para cada paciente: nome completo (nome + sobrenome), cor de triagem, horário de chegada, horário de atendimento e tempo de espera
- Para pacientes que não foram atendidos, registrar como "Não atendido" e "N/A"
- Colocar no topo do arquivo a data e hora em que foi gerado
- Encerrar o programa depois de salvar

**Prioridade:** `Baixa`

---

### 3.2 Como o sistema precisa se comportar (Requisitos Não Funcionais)

---

#### [RNF-01] Velocidade

> **História:** Como *enfermeira da triagem*, quero que o sistema seja rápido, para não travar na hora do cadastro e não atrasar a fila.

**Critério:** A fila deve ser atualizada em no máximo **1 segundo**.

**Prioridade:** `Alta`

---

#### [RNF-02] Facilidade de uso

> **História:** Como *usuário do sistema*, quero um menu simples e direto, para conseguir usar sem precisar de treinamento.

**Critérios:**

- Fazer uma triagem completa em no máximo **3 passos** a partir do menu
- Todas as opções numeradas e acessíveis direto pelo teclado
- Interface no terminal com bordas em ASCII para ficar mais fácil de ler
- Letras e contrastes que deem para enxergar bem em monitores simples

**Prioridade:** `Média`

---

## 4. Regras de Negócio

As regras de negócio definem a lógica por trás do sistema, ou seja, como ele deve tomar decisões.

---

### [RN-01] Ordem de atendimento por cor de risco

A fila é sempre organizada pela gravidade do paciente, nessa ordem:

| Cor | Situação | Prioridade |
|---|---|---|
| Vermelho | Emergência | Maior |
| Amarelo | Urgente | Média |
| Verde | Pouco urgente | Menor |

> Nenhum paciente de cor mais baixa pode ser chamado enquanto houver alguém de cor mais alta esperando.

---

### [RN-02] Idosos têm prioridade dentro da mesma cor

Dentro de uma mesma cor, pacientes com **60 anos ou mais** são chamados antes dos mais novos. Se houver empate (dois idosos ou dois não-idosos na mesma cor), quem chegou **primeiro** é chamado antes.

---

### [RN-03] Tempo máximo de espera por cor

Quando um paciente espera mais do que o limite da sua cor, o sistema mostra um alerta automático:

| Cor | Tempo máximo | O que acontece |
|---|---|---|
| Vermelho | 0 minutos | Alerta assim que é cadastrado |
| Amarelo | 30 minutos | Alerta após 30 min na fila |
| Verde | 120 minutos | Alerta após 120 min na fila |

O alerta aparece só uma vez por paciente. Se a cor dele for alterada no cadastro, o alerta é resetado e começa a contar de novo com base na nova cor.

---

### [RN-04] Validação de idade

O sistema nunca aceita uma idade inválida. As seguintes situações são tratadas:

- **Valor não-numérico** (letras, símbolos).
- **Valor negativo** (ex.: -5).
