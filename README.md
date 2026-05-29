# Especificação de Requisitos de Software — HealthManager

## 1. Introdução
### 1.1 Propósito
Este documento especifica os requisitos funcionais, não funcionais e as regras de negócio para o sistema HealthManager, um software de triagem hospitalar baseado no Protocolo de Manchester para otimização do fluxo de atendimento.

### 1.2 Escopo do Sistema
O sistema controlará a recepção e a triagem, permitindo a classificação de risco por cores, a ordenação automatizada da fila por gravidade e idade, o controle de tempo de atendimento através de alertas visuais e a exportação diária dos dados.

## 2. Descrição Geral 
### 2.1 Funções do Produto
O HealthManager atuará na recepção do hospital, sendo operado por enfermeiras na triagem e visualizado por médicos e gestores. O sistema substitui o controle manual ou por ordem de chegada simples por um algoritmo de priorização dinâmica.

### 2.2 Características dos Usuários
- Enfermeira da Triagem: Usuário operacional, necessita de interface rápida e de poucos cliques.
  
- Médico/Profissional de Saúde: Usuário final da fila, focado na chamada do próximo paciente.
  
- Gestor/Administrador: Usuário que monitora gargalos (limitações) e exporta relatórios.

## 3. Requisitos de Sistema
Nesta seção, as necessidades dos stakeholders são mapeadas no formato de histórias de usuário, acompanhadas de seus critérios de aceitação e identificadores únicos.

### 3.1 Requisitos Funcionais (RF)
#### [RF-01] Cadastro de Paciente e Triagem
- User Story: Como Enfermeira da Triagem, eu quero cadastrar o paciente com nome, idade, cor do Protocolo de Manchester e horário automático de chegada, para identificar o nível de risco de cada paciente logo na recepção.
  
- Critérios de Aceitação: O sistema deve registrar o carimbo de data/hora (timestamp) no momento exato do salvamento.
  
- As cores permitidas devem ser estritamente: Vermelho, Amarelo ou Verde.
  
- Prioridade: Alta

#### [RF-02] Exibição da Fila Atualizada
- User Story: Como Equipe Hospitalar, eu quero visualizar a fila de espera atualizada em tempo real a cada nova triagem, para saber exatamente quem é o próximo a ser chamado conforme as regras de prioridade.

- Critérios de Aceitação: Qualquer inserção ou alteração na fila deve disparar um gatilho de atualização visual imediata para todos os usuários logados.

- Prioridade: Alta

#### [RF-03] Chamar Próximo Paciente
- User Story: Como Profissional de Saúde, eu quero acionar um comando para chamar o próximo paciente da fila, para iniciar o atendimento dele, registrá-lo no sistema e removê-lo da espera.

- Critérios de Aceitação: O sistema deve registrar o horário de início do atendimento médico. O paciente chamado deve sair do status "Em Espera" e passar para o status "Em Atendimento".

- Prioridade: Alta

#### [RF-04] Alerta de Tempo Limite (Pop Up)
- User Story: Como Gestor do Hospital, eu quero receber um alerta em formato de pop-up quando um paciente ultrapassar o tempo máximo permitido de fila ou de atendimento, para tomar providências rápidas e evitar riscos à saúde.

- Critérios de Aceitação: O alerta deve interromper a tela atual em formato modal (pop-up) exibindo nome, cor e tempo estourado do paciente.

- Prioridade: Média

#### [RF-05] Exportação de Histórico Diário
- User Story: Como Administrador do Sistema, eu quero exportar os dados de atendimento do dia em um arquivo TXT ao fechar o turno, para manter um backup físico e auditar os tempos de espera do hospital.

- Critérios de Aceitação: O arquivo deve ser gerado contendo: Nome, cor de triagem, horário de chegada, horário de atendimento e tempo total de espera.

- Prioridade: Baixa

### 3.2 Requisitos Não Funcionais (RNF)
#### [RNF-01] Desempenho e Fluidez (Otimização)
- User Story: Como Enfermeira da Triagem, eu quero que o sistema processe as triagens e atualize a fila em menos de 1 segundo, para que o sistema não trave e a recepção não fique congestionada.
  
- Métrica/Critério: Tempo de resposta das requisições de ordenação da fila $\le 1.0 \text{ segundo}$ sob carga normal de uso.
  
- Prioridade: Alta

#### [RNF-02] Usabilidade e Menu Intuitivo
- User Story: Como Usuário do Sistema, eu quero um menu simples, intuitivo e com cores de prioridade bem destacadas, para operar o software sem necessidade de treinamentos complexos e com pouquíssimos cliques.

- Métrica/Critério: Fluxo de triagem completo em no máximo 3 cliques a partir da tela inicial. Cores acessíveis (alto contraste para visualização em monitores simples).

- Prioridade: Média

## 4. Regras de Negócio (RN)
Conforme a norma IEEE 29148, as regras de negócio guiam a lógica do código que processa os requisitos funcionais descritos na seção 3.

#### [RN-01] Ordenação por Gravidade (Protocolo de Manchester): 
A ordenação primária da fila deve ser baseada estritamente no grau de risco determinado pelas cores:

- Vermelho (Emergência) -> Amarelo (Urgente) -> Verde (Pouco Urgente)

Nenhum paciente de cor inferior pode ser chamado se houver um paciente de cor superior aguardando.

#### [RN-02] Prioridade para Idosos (> 60 Anos ):
Dentro de uma mesma cor, pacientes com idade igual ou superior a 60 anos possuem prioridade sobre os não-idosos, movendo-se para a frente deste subgrupo.
- Critério de Desempate: Se houver dois idosos (ou dois não-idosos) na mesma categoria de cor, o critério de desempate será estritamente a ordem cronológica de chegada (horário da triagem).

#### [RN-03] Tempos Máximos para Disparo de Alerta:
O gatilho para o pop-up de alerta estipulado no [RF-04] deve seguir rigorosamente as métricas de tempo abaixo:
##### - Em Fila de Espera:
- Vermelho: 0 Minutos (Alerta imediato se não for atendido)
- Amarelo: 30 minutos
- Verde: 120 minutos

##### Em atendimento: 
Qualquer paciente (independente da cor) que ultrapassar 60 minutos dentro do consultório.
