import csv
import os
import uuid

class SimulationLog:
    def __init__(self, file_path="simulation_log.csv"):
        """
        Inicializa o SimulationLog e cria o arquivo CSV se ele não existir.

        :param file_path: Caminho do arquivo CSV onde os logs serão armazenados.
        """
        self.file_path = file_path

        # Criar o arquivo e cabeçalho caso ele não exista
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["log_id", "execution_id", "robot", "machine", "start_time", "end_time"])

    def log_execution(self, robot, machine, start_time, end_time, execution_id=None):
        """
        Adiciona uma entrada ao log.

        :param robot: Nome do robô executado.
        :param machine: Nome da máquina onde a execução ocorreu.
        :param start_time: Hora de início da execução.
        :param end_time: Hora de término da execução.
        :param execution_id: (Opcional) ID da execução do ExecutionDataset.
        """
        log_id = str(uuid.uuid4())  # Gera um identificador único para cada entrada

        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([log_id, execution_id, robot, machine, start_time, end_time])

    def get_logs(self):
        """
        Retorna todos os registros do log como uma lista de dicionários.
        """
        logs = []
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append(row)
        return logs

    def __repr__(self):
        """
        Representação legível do log.
        """
        return f"SimulationLog(file_path={self.file_path})"
