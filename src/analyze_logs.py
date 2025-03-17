import os
import pandas as pd
import matplotlib.pyplot as plt

# Definição do diretório de logs
LOGS_DIR = "./logs"

# Coleta todos os arquivos CSV no diretório de logs
log_files = [os.path.join(LOGS_DIR, file) for file in os.listdir(LOGS_DIR) if file.endswith(".csv")]

# Lista para armazenar os dados de cada arquivo
log_data = []

# Carregar os logs
for file in log_files:
    df = pd.read_csv(file)
    
    # Extraindo o nome do método a partir do nome do arquivo
    method_name = os.path.basename(file).replace("simulation_log_data_", "").replace(".csv", "")
    
    # Adicionando a coluna do método no DataFrame
    df["method"] = method_name
    
    # Converter as colunas de data para datetime
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")
    
    # Garantindo que valores nulos sejam tratados
    df.dropna(subset=["start_time", "end_time"], inplace=True)

    # Ajuste: Extraindo completion_percentage corretamente
    df["completion_percentage"] = df.apply(lambda row: float(row["data"]) if row["event_type"] == "completion_percentage" else None, axis=1)
    
    log_data.append(df)

# Combinar todos os logs em um único DataFrame
logs_df = pd.concat(log_data, ignore_index=True)

### FILTRANDO SOMENTE AS EXECUÇÕES VÁLIDAS (removendo execuções sem ID)
logs_df = logs_df[logs_df["execution_id"].notna()]

# Definir os limites de tempo com base nos dados disponíveis
start_time_min = logs_df["start_time"].min()
end_time_max = logs_df["end_time"].max()

# Criar um DataFrame com as métricas agregadas por método
summary_df = logs_df.groupby("method").agg(
    total_executions=pd.NamedAgg(column="execution_id", aggfunc="count"),
    total_run_overs=pd.NamedAgg(column="event_type", aggfunc=lambda x: (x == "run_over").sum()),
    final_completion_logs=pd.NamedAgg(column="event_type", aggfunc=lambda x: (x == "completion_percentage").sum()),
    final_completion_percentage=pd.NamedAgg(column="completion_percentage", aggfunc="mean")
).reset_index()

# Exibir os resultados no terminal
print(summary_df)

# Salvar os resultados em CSV
summary_file = os.path.join(LOGS_DIR, "log_analysis_results.csv")
summary_df.to_csv(summary_file, index=False)

# ========== GERAR GRÁFICOS ==========
# Gráfico de barras comparando a completude final
plt.figure(figsize=(10, 5))
plt.bar(summary_df["method"], summary_df["final_completion_percentage"])
plt.xlabel("Método")
plt.ylabel("Porcentagem Final de Completeza")
plt.title("Comparação de Completeza por Método")
plt.xticks(rotation=30)
plt.savefig(os.path.join(LOGS_DIR, "completion_comparison.png"))
plt.show()

# Gráfico de evolução da completude ao longo do tempo
completion_logs = logs_df[logs_df["event_type"] == "completion_percentage"].dropna(subset=["completion_percentage"])
plt.figure(figsize=(12, 6))

for method, data in completion_logs.groupby("method"):
    plt.plot(data["start_time"], data["completion_percentage"], label=method)

plt.xlabel("Tempo")
plt.ylabel("Porcentagem de Completeza")
plt.title("Evolução da Completeza ao Longo do Tempo")
plt.legend()
plt.xlim(start_time_min, end_time_max)  # Limitando ao tempo dos logs
plt.savefig(os.path.join(LOGS_DIR, "completion_evolution.png"))
plt.show()

# Gráfico de evolução dos atropelamentos ao longo do tempo
run_over_logs = logs_df[logs_df["event_type"] == "run_over"]
plt.figure(figsize=(12, 6))

for method, data in run_over_logs.groupby("method"):
    plt.plot(data["start_time"], range(len(data)), label=method)

plt.xlabel("Tempo")
plt.ylabel("Número Acumulado de Atropelamentos")
plt.title("Evolução dos Atropelamentos ao Longo do Tempo")
plt.legend()
plt.xlim(start_time_min, end_time_max)  # Limitando ao tempo dos logs
plt.savefig(os.path.join(LOGS_DIR, "run_over_evolution.png"))
plt.show()

print(f"✅ Análise concluída! Os resultados foram salvos em: {summary_file}")
