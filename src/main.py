from datetime import datetime, timedelta
from event_scheduler import EventScheduler, Event
from bp_scheduler import BPScheduler
from dynamic_queue import DynamicQueue
from execution_dataset import ExecutionDataset
from simulation_log import SimulationLog
from machines import Machines
from robot import Robot

# Configuração para escolher entre BP Scheduler e Dynamic Queue
USE_BP_SCHEDULER = False  # Se False, usará DynamicQueue

# Definir caminhos dos arquivos de entrada
BP_SCHEDULER_FILE = "data/bp_scheduler.csv"
DYNAMIC_QUEUE_FILE = "data/dynamic_queue.csv"
EXECUTION_DATASET_FILE = "data/execution_dataset.csv"
SIMULATION_LOG_FILE = "logs/simulation_log.csv"

# Inicializar as estruturas do sistema
start_time = datetime(2025, 2, 20, 8, 0)  # Data inicial da simulação
clock = start_time
finish_time = datetime(2025, 3, 20, 0, 0)
event_scheduler = EventScheduler(start_time)
execution_dataset = ExecutionDataset(EXECUTION_DATASET_FILE)
simulation_log = SimulationLog(SIMULATION_LOG_FILE)
# machine_names = ["M1", "M2", "M3"]  # Máquinas disponíveis
machine_names = ["M1"]  # Máquinas disponíveis
machines = Machines(machine_names)

# =================================== LÓGICA PARA ESCOLHER ENTRE BP SCHEDULER E FILA DINÂMICA ===================================
if USE_BP_SCHEDULER:
    scheduler = BPScheduler(BP_SCHEDULER_FILE)
    executions = scheduler.get_all_executions()
    for execution in executions:
        robot = execution.robot 
        scheduled_bot_event = Event(execution.start_time, "start_execution", robot, execution.machine_name)
        event_scheduler.add_event(scheduled_bot_event)
else:
    scheduler = DynamicQueue(DYNAMIC_QUEUE_FILE, sorting_algorithm="FIFO")

    for machine in machines.get_idle_machines():
        # Adicionar o primeiro evento da DynamicQueue ao EventScheduler
        robot = scheduler.get_next_robot()
        if robot:
            initial_event = Event(start_time, "start_execution", robot, machine)
            event_scheduler.add_event(initial_event)
# =================================================================================================================================



# Executar a simulação
while event_scheduler.has_pending_events() and clock <= finish_time:
    event = event_scheduler.get_next_event()
    
    # Sai do loop caso não tenha mais eventos a serem processados
    if event == None:
        break

    # ============================= PROCESSAMENTO DE EVENTO DE INÍCIO (start_execution) =============================
    if event.event_type == "start_execution":
        if event.machine_name in machines.get_idle_machines():
            machines.make_machine_busy(event.machine_name)

            # Buscar uma execução no ExecutionDataset com base no robô e horário
            current_execution = execution_dataset.get_execution_by_robot_and_time(event.robot.name, event.event_time)

            # Definir o tempo de execução baseado no ExecutionDataset, se existir
            if current_execution:
                execution_time = current_execution["items"] * current_execution["time_per_item"]
                execution_id = current_execution["execution_id"]
            else:
                execution_time = 2  # Tempo mínimo de execução para eventos fora do dataset
                execution_id = None

            # Set no valor do clock
            clock = event.event_time

            # Criar um evento de término da execução e adicioná-lo no EventScheduler
            end_time = event.event_time + timedelta(minutes=execution_time)
            event_scheduler.add_event(Event(end_time, "end_execution", event.robot, event.machine_name))

            # Registrar no SimulationLog
            simulation_log.log(event.event_type, event.robot.name, event.machine_name, event.event_time, end_time, execution_id)

            # Marcar a execução como concluída se for do ExecutionDataset
            if execution_id:
                execution_dataset.mark_execution_complete(execution_id)
                
                # Faz log da porcentagem de completudo do execution_dataset.
                completion_percentage = round(execution_dataset.get_completion_percentage(), 2)
                
                simulation_log.log("completion_percentage", None, None, event.event_time, event.event_time, execution_id, completion_percentage)

        else:
            # Registrar "Atropelamento" no log e continuar
            simulation_log.log(event.event_type, event.robot.name, event.machine_name, event.event_time, event.event_time)
            print(f"Atropelamento: {event.robot.name} tentou executar em {event.machine_name}, mas estava ocupada.")
            continue

    # ============================= PROCESSAMENTO DE EVENTO DE FIM (end_execution) =============================
    elif event.event_type == "end_execution":
        machines.make_machine_idle(event.machine_name)
        
        # Set no valor do clock
        clock = event.event_time

        # =================================== LÓGICA PARA A FILA DINÂMICA ===================================
        if not USE_BP_SCHEDULER:
            # Adiciona o robô que terminou de executar na fila novamente
            scheduler.add_robot(event.robot)
            next_robot = scheduler.get_next_robot()  # Pega o próximo robô da fila dinâmica
            if next_robot:
                next_event = Event(event.event_time, "start_execution", next_robot, machines.get_idle_machines()[0])
                event_scheduler.add_event(next_event)
        # ====================================================================================================

# Verificar se todas as execuções foram concluídas
if execution_dataset.all_executions_complete():
    print("Simulação concluída com sucesso!")
else:
    print("Algumas execuções não foram realizadas dentro do tempo disponível.")

