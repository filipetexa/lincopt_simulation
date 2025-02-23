from datetime import datetime, timedelta
from event_scheduler import EventScheduler, Event
from bp_scheduler import BPScheduler
from dynamic_queue import DynamicQueue
from execution_dataset import ExecutionDataset
from simulation_log import SimulationLog
from machines import Machines

# Configuração para escolher entre BP Scheduler e Dynamic Queue
USE_BP_SCHEDULER = True  # Se False, usará DynamicQueue (ainda não implementada)

# Definir caminhos dos arquivos de entrada
BP_SCHEDULER_FILE = "data/bp_scheduler.csv"
DYNAMIC_QUEUE_FILE = "data/dynamic_queue.csv"
EXECUTION_DATASET_FILE = "data/execution_dataset.csv"
SIMULATION_LOG_FILE = "logs/simulation_log.csv"

# Inicializar as estruturas do sistema
start_time = datetime(2025, 2, 20, 8, 0)  # Data inicial da simulação
event_scheduler = EventScheduler(start_time)
execution_dataset = ExecutionDataset(EXECUTION_DATASET_FILE)
simulation_log = SimulationLog(SIMULATION_LOG_FILE)
machine_names = ["M1", "M2", "M3"]  # Máquinas disponíveis
machines = Machines(machine_names)

# Escolher a fonte de execuções (BP Scheduler ou Dynamic Queue)
if USE_BP_SCHEDULER:
    scheduler = BPScheduler(BP_SCHEDULER_FILE)
    executions = scheduler.get_all_executions()
else:
    scheduler = DynamicQueue(DYNAMIC_QUEUE_FILE, sorting_algorithm="FIFO")
    executions = []  # Implementação futura

# Carregar os eventos no EventScheduler
for execution in executions:
    scheduled_bot_event = Event(execution.start_time, "start_execution", execution.robot_name, execution.machine_name)
    event_scheduler.add_event(scheduled_bot_event)

# Executar a simulação
while event_scheduler.has_pending_events():
    event = event_scheduler.get_next_event()

    # Verificar se a máquina está ocupada
    if event.event_type == "start_execution":
        if event.machine_name in machines.get_idle_machines():
            machines.make_machine_busy(event.machine_name)
        else:
            # Registrar "Atropelamento" no log e continuar
            simulation_log.log_execution(event.robot_name, event.machine_name, event.event_time, event.event_time, execution_id=None)
            print(f"Atropelamento: {event.robot_name} tentou executar em {event.machine_name}, mas estava ocupada.")
            continue

    # Buscar uma execução no ExecutionDataset com base no robô e horário
    execution = execution_dataset.get_execution_by_robot_and_time(event.robot_name, event.event_time)

    # Definir o tempo de execução baseado no ExecutionDataset, se existir
    if execution:
        execution_time = execution["items"] * execution["time_per_item"]
        execution_id = execution["execution_id"]
    else:
        execution_time = 10  # Tempo mínimo de execução para eventos fora do dataset
        execution_id = None

    # Criar um evento de término da execução
    end_time = event.event_time + timedelta(minutes=execution_time)
    event_scheduler.add_event(Event(end_time, "end_execution", event.robot_name, event.machine_name))

    # Registrar no SimulationLog
    simulation_log.log_execution(event.robot_name, event.machine_name, event.event_time, end_time, execution_id)

    # Marcar a execução como concluída se for do ExecutionDataset
    if execution_id:
        execution_dataset.mark_execution_complete(execution_id)

    # Se for um evento de término, liberar a máquina
    if event.event_type == "end_execution":
        machines.make_machine_idle(event.machine_name)

# Verificar se todas as execuções foram concluídas
if execution_dataset.all_executions_complete():
    print("Simulação concluída com sucesso!")
else:
    print("Algumas execuções não foram realizadas dentro do tempo disponível.")
