class QueueSortingAlgorithm:
    def __init__(self, strategy="FIFO"):
        """
        Inicializa o algoritmo de ordenação da DynamicQueue.

        :param strategy: Algoritmo de ordenação (FIFO, PRIORITY).
        """
        self.strategy = strategy

    def sort(self, queue):
        """
        Aplica a estratégia de ordenação na fila.
        
        :param queue: Lista de robôs a serem ordenados.
        :return: Lista ordenada conforme a estratégia.
        """
        if self.strategy == "FIFO":
            return self.fifo(queue)
        elif self.strategy == "PRIORITY":
            return self.priority(queue)
        else:
            raise ValueError(f"Algoritmo {self.strategy} não reconhecido")

    def fifo(self, queue):
        """
        Ordena a fila por ordem de chegada (mantém a posição original).
        """
        return queue  # FIFO já mantém a ordem de chegada

    def priority(self, queue):
        """
        Ordena a fila por prioridade (quanto menor o número, maior a prioridade).
        """
        return sorted(queue, key=lambda robot: robot.priority)
