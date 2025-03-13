class QueueSortingAlgorithm:
    def __init__(self, strategy="FIFO"):
        """
        Inicializa o algoritmo de ordenação da DynamicQueue.

        :param strategy: Algoritmo de ordenação (FIFO, PRIORITY, WEIGHTED_PRIORITY).
        """
        self.strategy = strategy

    def sort(self, queue, data):
        """
        Aplica a estratégia de ordenação na fila.
        
        :param queue: Lista de robôs a serem ordenados.
        :param data: Dicionário contendo informações auxiliares (ex: pesos dos robôs).
        :return: Lista ordenada conforme a estratégia e o dicionário de dados atualizado.
        """
        if self.strategy == "FIFO":
            return self.fifo(queue, data)
        elif self.strategy == "PRIORITY":
            return self.priority(queue, data)
        elif self.strategy == "WEIGHTED_PRIORITY":
            return self.weighted_priority(queue, data)
        else:
            raise ValueError(f"Algoritmo {self.strategy} não reconhecido")

    def fifo(self, queue, data):
        """
        Ordena a fila por ordem de chegada (FIFO).
        Retorna a fila inalterada e o mesmo data.
        """
        return queue, data  # FIFO já mantém a ordem de chegada

    def priority(self, queue, data):
        """
        Ordena a fila por prioridade (quanto menor o número, maior a prioridade).
        """
        return sorted(queue, key=lambda robot: robot.priority), data

    def weighted_priority(self, queue, data):
        """
        Ordena a fila por pesos acumulados.
        - Robôs com maior peso são executados primeiro.
        - Se pesos forem iguais, usa a prioridade como critério secundário.
        - Se ainda houver empate, segue FIFO.
        """
        # Inicializa os pesos no dicionário, caso não existam
        for robot in queue:
            if robot.name not in data:
                data[robot.name] = {"weight": 0}

        # Set do ultimo robo executado com 0
        last_bot_executed = queue[-1].name
        data[last_bot_executed] = {"weight": 0}


        # Atualiza os pesos dos robôs conforme a prioridade
        for robot in queue:
            if robot.priority == 1:
                data[robot.name]["weight"] += 3
            elif robot.priority == 2:
                data[robot.name]["weight"] += 2
            elif robot.priority == 3:
                data[robot.name]["weight"] += 1

        # Ordena pelo peso acumulado (maior peso primeiro)
        # Em caso de empate, ordena pela menor prioridade
        # Se ainda houver empate, mantém FIFO
        sorted_queue = sorted(queue, key=lambda robot: (-data[robot.name]["weight"], robot.priority))

        return sorted_queue, data  # Retorna a fila reordenada e os dados atualizados
