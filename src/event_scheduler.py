import heapq

class Event:
    def __init__(self, event_time, event_type, robot_name, machine_name):
        """
        Representa um evento dentro da simulação.

        :param event_time: Tempo no qual o evento deve ser processado.
        :param event_type: Tipo do evento ('start_execution' ou 'end_execution').
        :param robot_name: Nome do robô envolvido na execução.
        :param machine_name: Nome da máquina onde o robô será executado.
        """
        self.event_time = event_time  
        self.event_type = event_type  
        self.robot_name = robot_name  
        self.machine_name = machine_name  

    def __lt__(self, other):
        """
        Método para comparar eventos no MinHeap.
        O menor `event_time` será processado primeiro.
        """
        return self.event_time < other.event_time

    def __repr__(self):
        """
        Representação legível do evento para debug.
        """
        return (f"Event(time={self.event_time}, type={self.event_type}, "
                f"robot={self.robot_name}, machine={self.machine_name})")


class EventScheduler:
    def __init__(self, start_time):
        """
        Inicializa o escalonador de eventos.
        
        :param start_time: Tempo inicial da simulação (datetime).
        """
        self.event_heap = []  # MinHeap para armazenar os eventos
        self.current_time = start_time  # Clock interno da simulação
    
    def add_event(self, event):
        """
        Adiciona um evento ao heap.
        
        :param event: Instância da classe Event.
        """
        heapq.heappush(self.event_heap, (event.event_time, event))
    
    def get_next_event(self):
        """
        Retorna o próximo evento a ser processado e avança o clock.
        """
        if self.event_heap:
            self.current_time, event = heapq.heappop(self.event_heap)
            return event
        return None
    
    def has_pending_events(self):
        """
        Retorna True se ainda há eventos pendentes no heap.
        """
        return len(self.event_heap) > 0


