class Machine:
    def __init__(self, name):
        """
        Representa uma máquina dentro da simulação.

        :param name: Nome da máquina.
        """
        self.name = name
        self.status = "idle"  # Inicialmente, todas as máquinas estão ociosas

    def make_idle(self):
        """
        Define o status da máquina como 'idle' (ociosa).
        """
        self.status = "idle"

    def make_busy(self):
        """
        Define o status da máquina como 'busy' (ocupada).
        """
        self.status = "busy"

    def is_idle(self):
        """
        Retorna True se a máquina está ociosa.
        """
        return self.status == "idle"

    def __repr__(self):
        """
        Representação legível da máquina.
        """
        return f"Machine(name={self.name}, status={self.status})"


class Machines:
    def __init__(self, machine_names):
        """
        Gerencia um grupo de máquinas.

        :param machine_names: Lista com os nomes das máquinas.
        """
        self.machines = {name: Machine(name) for name in machine_names}

    def make_machine_idle(self, machine_name):
        """
        Define uma máquina específica como 'idle'.

        :param machine_name: Nome da máquina.
        """
        if machine_name in self.machines:
            self.machines[machine_name].make_idle()

    def make_machine_busy(self, machine_name):
        """
        Define uma máquina específica como 'busy'.

        :param machine_name: Nome da máquina.
        """
        if machine_name in self.machines:
            self.machines[machine_name].make_busy()

    def get_idle_machines(self):
        """
        Retorna uma lista com os nomes das máquinas que estão ociosas.
        """
        return [name for name, machine in self.machines.items() if machine.is_idle()]

    def __repr__(self):
        """
        Representação legível do grupo de máquinas.
        """
        return f"Machines({list(self.machines.values())})"
