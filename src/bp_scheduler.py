import heapq
import pandas as pd
from datetime import datetime

class ScheduledExecution:
    def __init__(self, start_time, robot_name, machine_name):
        """
        Representa uma execução programada no BP Scheduler.

        :param start_time: Data e hora da execução.
        :param robot_name: Nome do robô a ser executado.
        :param machine_name: Nome da máquina onde o robô será executado.
        """
        self.start_time = start_time
        self.robot_name = robot_name
        self.machine_name = machine_name

    def __lt__(self, other):
        """
        Permite a ordenação automática no MinHeap pelo tempo de início.
        """
        return self.start_time < other.start_time

    def __repr__(self):
        """
        Representação legível da execução programada.
        """
        return (f"ScheduledExecution(time={self.start_time}, robot={self.robot_name}, "
                f"machine={self.machine_name})")

class BPScheduler:
    def __init__(self, file_path):
        """
        Inicializa o BP Scheduler e carrega as execuções programadas automaticamente.

        :param file_path: Caminho do arquivo CSV contendo os agendamentos.
        """
        self.file_path = file_path
        self.scheduled_heap = []  # MinHeap para armazenar as execuções programadas
        self._load_schedule()

    def _load_schedule(self):
        """
        Lê o arquivo CSV e carrega as execuções programadas no MinHeap.
        """
        df = pd.read_csv(self.file_path)

        for _, row in df.iterrows():
            robot_name = row["robot"]
            machine_name = row["machine"]
            start_time = datetime.strptime(f"{row['date']} {row['start_time']}", "%Y-%m-%d %H:%M")

            execution = ScheduledExecution(start_time, robot_name, machine_name)
            heapq.heappush(self.scheduled_heap, execution)

        print(f"{len(self.scheduled_heap)} execuções programadas carregadas no BP Scheduler.")

    def get_all_executions(self):
        return sorted(self.scheduled_heap)
    
    def get_next_execution(self):
        """
        Retorna a próxima execução programada.
        """
        if self.scheduled_heap:
            return heapq.heappop(self.scheduled_heap)  # Remove e retorna a próxima execução
        return None  # Retorna None se não houver mais execuções programadas
