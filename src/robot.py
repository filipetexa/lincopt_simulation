class Robot:
    def __init__(self, name, priority=0):
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