import os
import pandas as pd
import matplotlib.pyplot as plt

# Definir a pasta base onde estão os arquivos de log
LOGS_DIR = "./logs"

# Listar automaticamente todos os arquivos CSV dentro da pasta de logs
log_files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".csv")]

# Estrutura para armazenar os resultados
analysis_results = []

# Função para processar um único arquivo de log
def process_log(file_path, method_name):
    df = pd.read_csv(file_path)

    # Verificar se as colunas esperadas estão no arquivo
    required_columns = {"event_type", "execution_id", "robot", "machine", "start_time", "end_time"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        print(f"⚠️ Aviso: O arquivo {file_path} está faltando as colunas: {missing_columns}")
        return None

    # Total de execuções concluídas (event_type = "robot_execution")
    total_executions = df[df["event_type"] == "robot_execution"].shape[0]

    # Execuções canceladas ou ignoradas (event_type = "run_over")
    total_run_overs = df[df["event_type"] == "run_over"].shape[0]

    # Verificar se a coluna 'completion_percentage' existe antes de acessá-la
    if "completion_percentage" in df.columns:
        completion_logs = df[df["event_type"] == "completion_percentage"]
        final_completion = completion_logs["execution_id"].count()
        completion_percentage = completion_logs["completion_percentage"].max() if not completion_logs.empty else 0
    else:
        final_completion = 0
        completion_percentage = 0

    return {
        "method": method_name,
        "total_executions": total_executions,
        "total_run_overs": total_run_overs,
        "final_completion_logs": final_completion,
        "final_completion_percentage": completion_percentage
    }

# Processar todos os arquivos encontrados na pasta
for log_file in log_files:
    method_name = log_file.replace("simulation_log_data_", "").replace(".csv", "").replace(".csv_", "")
    file_path = os.path.join(LOGS_DIR, log_file)

    if os.path.exists(file_path):
        result = process_log(file_path, method_name)
        if result:
            analysis_results.append(result)

# Criar DataFrame com os resultados
results_df = pd.DataFrame(analysis_results)

# Salvar os resultados em CSV
output_file = os.path.join(LOGS_DIR, "log_analysis_results.csv")
results_df.to_csv(output_file, index=False)

# Exibir os resultados no terminal
print(results_df)

# Criar gráfico de execuções concluídas por método
plt.figure(figsize=(8, 5))
plt.bar(results_df["method"], results_df["total_executions"], color="blue")
plt.xlabel("Método de Execução")
plt.ylabel("Total de Execuções Concluídas")
plt.title("Comparação de Execuções Concluídas por Método")
plt.xticks(rotation=25)
plt.show()

# Criar gráfico de atropelamentos por método
plt.figure(figsize=(8, 5))
plt.bar(results_df["method"], results_df["total_run_overs"], color="red")
plt.xlabel("Método de Execução")
plt.ylabel("Total de Atropelamentos")
plt.title("Comparação de Atropelamentos por Método")
plt.xticks(rotation=25)
plt.show()

# Criar gráfico de porcentagem de completude final
plt.figure(figsize=(8, 5))
plt.bar(results_df["method"], results_df["final_completion_percentage"], color="green")
plt.xlabel("Método de Execução")
plt.ylabel("Porcentagem Final de Completude")
plt.title("Comparação de Completude por Método")
plt.xticks(rotation=25)
plt.show()

# Informar o usuário que a análise foi concluída
print(f"✅ Análise concluída! Os resultados foram salvos em: {output_file}")
