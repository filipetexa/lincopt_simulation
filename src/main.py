import argparse
from datetime import datetime, timedelta
from event_scheduler import EventScheduler, Event
from bp_scheduler import BPScheduler
from dynamic_queue import DynamicQueue
from execution_dataset import ExecutionDataset
from simulation_log import SimulationLog
from machines import Machines
from robot import Robot


# python main.py -ubp -bsf "custom_bp_scheduler.csv" -dq "custom_dynamic_queue.csv" -eds "custom_execution_dataset.csv" -sa "FIFO" or "WEIGHTED_PRIORITY"
# Configurar Argumentos do Terminal
parser = argparse.ArgumentParser(description="Simulação de Execução de Robôs")

parser.add_argument("-ubp", "--use_bp", action="store_true", help="Se definido, usa o BP Scheduler ao invés da Fila Dinâmica.")
parser.add_argument("-bsf", "--bp_scheduler_file", type=str, help="Arquivo CSV do BP Scheduler.")
parser.add_argument("-dq", "--dynamic_queue_file", type=str, help="Arquivo CSV da Fila Dinâmica.")
parser.add_argument("-eds", "--execution_dataset_file", type=str, default="data/execution_dataset.csv", help="Arquivo CSV do Execution Dataset.")
parser.add_argument("-sa", "--sort_algorithm", type=str, default="FIFO", help="Algoritmo de ordenação da Fila Dinâmica.")

args = parser.parse_args()

# Configuração baseada nos argumentos do terminal
USE_BP_SCHEDULER = args.use_bp
BP_SCHEDULER_FILE = args.bp_scheduler_file
DYNAMIC_QUEUE_FILE = args.dynamic_queue_file
EXECUTION_DATASET_FILE = args.execution_dataset_file
SORT_ALGORITHM = args.sort_algorithm

if BP_SCHEDULER_FILE:
    SIMULATION_LOG_FILE = f'logs/simulation_log_{BP_SCHEDULER_FILE.replace('/','_')}.csv'
else:
    SIMULATION_LOG_FILE = f'logs/simulation_log_{DYNAMIC_QUEUE_FILE.replace('/','_')}_{SORT_ALGORITHM}.csv'

# Inicializar as estruturas do sistema
start_time = datetime(2025, 2, 20, 8, 0)  # Data inicial da simulação
clock = start_time
finish_time = datetime(2025, 3, 20, 0, 0)
event_scheduler = EventScheduler(start_time)
execution_dataset = ExecutionDataset(EXECUTION_DATASET_FILE)
simulation_log = SimulationLog(SIMULATION_LOG_FILE)
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
    scheduler = DynamicQueue(DYNAMIC_QUEUE_FILE, sorting_algorithm=SORT_ALGORITHM)

    for machine in machines.get_idle_machines():
        # Adicionar o primeiro evento da DynamicQueue ao EventScheduler
        robot = scheduler.get_next_robot()
        if robot:
            initial_event = Event(start_time, "start_execution", robot, machine)
            event_scheduler.add_event(initial_event)
# =================================================================================================================================

# Executar a simulação
while (event_scheduler.has_pending_events() and USE_BP_SCHEDULER) or clock <= finish_time:
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
            simulation_log.log("robot_execution", event.robot.name, event.machine_name, event.event_time, end_time, execution_id)

            # Marcar a execução como concluída se for do ExecutionDataset
            if execution_id:
                execution_dataset.mark_execution_complete(execution_id)
                
                # Faz log da porcentagem de completudo do execution_dataset.
                completion_percentage = round(execution_dataset.get_completion_percentage(), 2)
                
                simulation_log.log("completion_percentage", None, None, event.event_time, event.event_time, execution_id, completion_percentage)

        else:
            # Registrar "Atropelamento" no log e continuar
            simulation_log.log("run_over", event.robot.name, event.machine_name, event.event_time, event.event_time)
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

