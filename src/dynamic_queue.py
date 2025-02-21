import pandas as pd
from queue_sorting import QueueSortingAlgorithm

class Robot:
    def __init__(self, name, priority):
        """
        Representa um robô na DynamicQueue.

        :param name: Nome do robô.
        :param priority: Prioridade do robô (quanto menor, maior a prioridade).
        """
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        """
        Permite ordenar robôs por prioridade automaticamente.
        """
        return self.priority < other.priority

    def __repr__(self):
        """
        Representação legível do robô.
        """
        return f"Robot(name={self.name}, priority={self.priority})"

class DynamicQueue:
    def __init__(self, file_path, sorting_algorithm="FIFO"):
        """
        Inicializa a fila dinâmica de robôs.

        :param file_path: Caminho do arquivo Excel contendo os robôs.
        :param sorting_algorithm: Algoritmo de ordenação da fila (padrão: FIFO).
        """
        self.robots = self._load_queue(file_path)
        self.sorting_algorithm = sorting_algorithm
        self._apply_sorting()

    def _load_queue(self, file_path):
        """
        Lê o arquivo Excel e carrega os robôs na fila inicial.
        """
        df = pd.read_excel(file_path)
        robots = [Robot(row["robot"], row["priority"]) for _, row in df.iterrows()]
        return robots

    def _apply_sorting(self):
        """
        Aplica o algoritmo de ordenação definido.
        """
        self.robots = QueueSortingAlgorithm(self.sorting_algorithm).sort(self.robots)

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
