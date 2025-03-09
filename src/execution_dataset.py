import pandas as pd
from datetime import datetime

class ExecutionDataset:
    def __init__(self, file_path):
        """
        Inicializa o ExecutionDataset e carrega as execuções do arquivo CSV.

        :param file_path: Caminho do arquivo CSV contendo as execuções.
        """
        self.file_path = file_path
        self.executions = self._load_executions()
        self._total_execution_time = self._calculate_total_execution_time()  # Calcula o tempo total planejado

    def _load_executions(self):
        """
        Lê o arquivo CSV e carrega as execuções em um conjunto de dicionários.
        """
        df = pd.read_csv(self.file_path)
        executions = set()

        for _, row in df.iterrows():
            execution = {
                "execution_id": row["execution_id"],
                "robot": row["robot"],
                "items": row["items"],
                "time_per_item": row["time_per_item"],
                "start_window": None if pd.isna(row["start_window"]) or row["start_window"] == "" else self._parse_datetime(row["start_window"]),
                "end_window": None if pd.isna(row["end_window"]) or row["end_window"] == "" else self._parse_datetime(row["end_window"]),
                "completed": row["completed"] if "completed" in row else False  # Respeita o valor existente ou assume False
            }
            executions.add(frozenset(execution.items()))

        return executions

    def _calculate_total_execution_time(self):
        """
        Calcula o tempo total planejado de execução somando items * time_per_item de todas as execuções.
        """
        return sum(dict(exec)["items"] * dict(exec)["time_per_item"] for exec in self.executions)

    def _parse_datetime(self, datetime_str):
        """
        Converte um valor de string no formato 'YYYY-MM-DD HH:MM' para um objeto datetime.
        """
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    def get_execution_by_robot_and_time(self, robot, execution_time):
        """
        Retorna a primeira execução correspondente ao robô e ao horário.

        :param robot: Nome do robô.
        :param execution_time: Data e hora da execução.
        :return: Execução correspondente ou None se não encontrar.
        """
        best_match = None

        for execution in self.executions:
            exec_dict = dict(execution)
            if exec_dict["robot"] == robot and not exec_dict["completed"]:
                if exec_dict["start_window"] and exec_dict["end_window"]:
                    if exec_dict["start_window"] <= execution_time <= exec_dict["end_window"]:
                        return exec_dict  # Retorna imediatamente se houver um match exato
                elif best_match is None:
                    best_match = exec_dict

        return best_match  # Retorna a execução sem restrição se nenhuma com janela foi encontrada

    def mark_execution_complete(self, execution_id):
        """
        Marca uma única execução correspondente como concluída.

        :param execution_id: ID único da execução.
        """
        for execution in self.executions:
            exec_dict = dict(execution)
            if exec_dict["execution_id"] == execution_id and not exec_dict["completed"]:
                
                # Marcar como concluído
                exec_dict["completed"] = True
                
                # Atualizar o conjunto
                self.executions.remove(execution)
                self.executions.add(frozenset(exec_dict.items()))
                return True  # Retorna sucesso

        return False  # Nenhuma execução encontrada para marcar

    def all_executions_complete(self):
        """
        Retorna True se todas as execuções foram concluídas.
        """
        return all(dict(execution)["completed"] for execution in self.executions)

    def get_completion_percentage(self):
        """
        Retorna a porcentagem de execuções concluídas com base no tempo total de execução.

        :return: Valor float representando a porcentagem de completude (0 a 100).
        """
        if self._total_execution_time == 0:
            return 0.0  # Evita divisão por zero

        completed_time = sum(
            dict(exec)["items"] * dict(exec)["time_per_item"]
            for exec in self.executions if dict(exec)["completed"]
        )
        return (completed_time / self._total_execution_time) * 100  # Retorna a porcentagem

    def get_pending_executions(self):
        """
        Retorna todas as execuções pendentes.
        """
        return [dict(execution) for execution in self.executions if not dict(execution)["completed"]]

    def __repr__(self):
        """
        Representação legível do ExecutionDataset.
        """
        return f"ExecutionDataset({[dict(exec) for exec in self.executions]})"
