# LincOpt Simulation

## Visão Geral
LincOpt Simulation é um simulador para avaliar estratégias de escalonamento de robôs em RPA, comparando o **BP Scheduler** (agendamento fixo) com a **DynamicQueue** (fila dinâmica otimizada). O projeto é desenvolvido em **Python**.

## Estruturas do Projeto

### ExecutionDataset
- Contém execuções planejadas, workload e restrições de horário/dia.
- Fonte: Arquivo **Excel** com:
  - Nome do robô
  - Data e janela de execução
  - Workload (itens e tempo por item)
- Quando uma execução ocorre, ela é marcada como **concluída**.
- A simulação termina quando todas as execuções forem concluídas.

### DynamicQueue
- Lista de robôs prontos para execução, ordenados por diferentes estratégias.
- Fonte: Arquivo **Excel** definindo a **ordem inicial da fila**.
- A fila é reorganizada dinamicamente conforme o algoritmo de ordenação selecionado.

### QueueSortingAlgorithm
- Implementa diferentes estratégias de ordenação:
  - FIFO (First In, First Out)
  - FIFO com prioridade
  - Escalonamento usando Inteligencia Artificial.

## Estrutura de Pastas
```
LincOpt_Simulation/
│── data/                # Arquivos de entrada (Excel)
│   ├── execution_dataset.xlsx
│   ├── dynamic_queue.xlsx
│   ├── bp_scheduler.xlsx
│
│── src/                 # Código-fonte do projeto
│   ├── main.py          # Script principal
│   ├── event_scheduler.py  # MinHeap para controle de eventos
│   ├── dynamic_queue.py # Gerenciamento da fila dinâmica
│   ├── queue_sorting.py # Algoritmos de ordenação da fila
│   ├── bp_scheduler.py  # Implementação do agendador tradicional
│
│── logs/                # Armazena logs de simulação
│
│── tests/               # Testes automatizados
│
│── README.md            # Documentação do projeto
```

### EventScheduler (MinHeap de Eventos)
- Controla todos os eventos da simulação em ordem cronológica.
- Origem dos eventos:
  - **BP Scheduler:** Eventos programados.
  - **DynamicQueue:** Robôs prontos para execução.
- Processa eventos do heap e avança o clock interno.

### BPScheduler
- Simula o agendamento tradicional do Blue Prism.
- Fonte: Arquivo **Excel** com:
  - Nome do robô
  - Data e horário de início
- Quando o `BPScheduler` é usado, a `DynamicQueue` não é utilizada.

### SimulationLog
- Registra todas as execuções concluídas:
  ```
  | Robô  | Início  | Fim   | Status  | Tempo Total |
  |-------|--------|------|--------|-------------|
  | R1    | 12:00  | 15:00 | OK     | 3h          |
  ```
- Utilizado para análise de performance e métricas.

## Fluxo de Inicialização
2. **Carregar dados dos arquivos Excel:**
   - `ExecutionDataset`
   - `DynamicQueue` ou `BPScheduler`
2. **Preencher o `EventScheduler` (MinHeap) com execuções pendentes.**
3. **Definir a estratégia de ordenação da `DynamicQueue`.**
4. **Iniciar a simulação:**
   - Processar eventos do heap
   - Executar robôs e registrar logs
   - Finalizar quando todas as execuções do `ExecutionDataset` forem concluídas.

## Objetivo
- Comparar **BP Scheduler** vs **DynamicQueue**.
- Avaliar diferentes **algoritmos de ordenação**.
- Gerar **métricas de escalonamento** para análise de performance.

## Casos de Teste
1. Um mês de execuções com janelas espaçadas  de 1h em 1h no bp_scheduler, mas sem restrições de horario.
  1.1 Usando apenas uma maquina.
  1.2 Usando multiplas maquinas.
2.Um mês de execuções com janelas espaçadas com tempos variados bp_scheduler, com restrições de horario. Exemplo 15 min e na sequencia uma janela de 4h.
  2.1 Usando apenas uma maquina.
  2.2 Usando multiplas maquins.
3. Um mês de execuções com Shceduler cheio:
  3.1 Execuções com cargas muito pequenas comoparadas as janelas do scheduler 
  3.2 Execuções com cargas muito grandes comoparadas as janelas do scheduler
4. Carga anual contenplando os casos 1, 2 e 3. 


