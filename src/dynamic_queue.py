import pandas as pd
from queue_sorting import QueueSortingAlgorithm
from robot import Robot

class DynamicQueue:
    def __init__(self, file_path, sorting_algorithm="FIFO", data=None):
        """
        Inicializa a fila dinâmica de robôs.

        :param file_path: Caminho do arquivo CSV contendo os robôs.
        :param sorting_algorithm: Algoritmo de ordenação da fila.
        :param data: Dicionário opcional para armazenar informações auxiliares do algoritmo.
        """
        self.robots = self._load_queue(file_path)
        self.sorting_algorithm = sorting_algorithm
        self.data = data if data is not None else {}  # Inicializa o data
        self._apply_sorting()

    def _load_queue(self, file_path):
        """
        Lê o arquivo CSV e carrega os robôs na fila inicial.
        """
        df = pd.read_csv(file_path)
        robots = [Robot(row["robot"], row["priority"]) for _, row in df.iterrows()]
        return robots

    def _apply_sorting(self):
        """
        Aplica o algoritmo de ordenação definido e atualiza o data.
        """
        self.robots, self.data = QueueSortingAlgorithm(self.sorting_algorithm).sort(self.robots, self.data)

    def get_next_robot(self):
        """
        Retorna o próximo robô da fila e remove da lista.
        """
        if self.robots:
            return self.robots.pop(0)  # Remove e retorna o primeiro robô
        return None  # Retorna None se a fila estiver vazia

    def add_robot(self, robot):
        """
        Adiciona um novo robô à fila e reordena.
        """
        self.robots.append(robot)
        self._apply_sorting()  # Ordena a fila novamente

    def __repr__(self):
        """
        Representação legível da fila de robôs.
        """
        return f"DynamicQueue({self.robots})"
