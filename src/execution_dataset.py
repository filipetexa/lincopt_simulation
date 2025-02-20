import pandas as pd
from datetime import datetime

class ExecutionDataset:
    def __init__(self, file_path):
        """
        Inicializa o ExecutionDataset e carrega os dados do arquivo Excel.

        :param file_path: Caminho do arquivo Excel contendo as execuções.
        """
        self.file_path = file_path
        self.executions = self._load_executions()

    def _load_executions(self):
        """
        Lê o arquivo Excel e carrega as execuções em um conjunto de dicionários.
        """
        df = pd.read_excel(self.file_path)
        executions = set()

        for _, row in df.iterrows():
            execution = {
                "execution_id": row["execution_id"],
                "robot": row["robot"],
                "items": row["items"],
                "time_per_item": row["time_per_item"],
                "start_window": '' if pd.isna(row["start_window"]) else datetime.strptime(row["start_window"], "%Y-%m-%d %H:%M"),
                "end_window": '' if pd.isna(row["end_window"]) else datetime.strptime(row["end_window"], "%Y-%m-%d %H:%M"),
                "completed": False
            }
            executions.add(frozenset(execution.items()))  # Armazenamos como um conjunto imutável

        return executions

    def get_execution_by_robot_and_time(self, robot, execution_time):
        """
        Retorna a primeira execução correspondente ao robô e ao horário.

        :param robot: Nome do robô.
        :param execution_time: Data e hora da execução.
        :return: Execução correspondente ou None se não encontrar.
        """
        for execution in self.executions:
            exec_dict = dict(execution)
            if exec_dict["robot"] == robot and not exec_dict["completed"]:
                # Se a execução tem uma janela de tempo, verifica se está dentro dela
                if exec_dict["start_window"] and exec_dict["end_window"]:
                    if not (exec_dict["start_window"] <= execution_time <= exec_dict["end_window"]):
                        continue  # Ignora essa execução se estiver fora da janela

                return exec_dict  # Retorna a primeira execução encontrada
        
        return None  # Nenhuma execução encontrada

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
