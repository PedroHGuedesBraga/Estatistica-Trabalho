import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="idades"
)

try:
    if conn.is_connected():
        print("Conexão com o MySQL foi bem-sucedida!")

        # Criar um cursor para executar consultas
        cursor = conn.cursor()

        # Consultar as idades da tabela pessoas
        query = "SELECT idade FROM pessoas"
        df = pd.read_sql(query, conn)

        if not df.empty:
            print("Idades inseridas na tabela:")
            print(df['idade'].tolist())
            
            # Cálculos das medidas de posição
            media = df['idade'].mean()
            mediana = df['idade'].median()
            moda = df['idade'].mode()[0]
            
            # Cálculos das medidas de dispersão
            variancia = df['idade'].var()
            desvio_padrao = df['idade'].std()
            amplitude = df['idade'].max() - df['idade'].min()
            
            # Cálculos de probabilidade
            prob_idade_30 = len(df[df['idade'] == 30]) / len(df)
            prob_intervalo = len(df[(df['idade'] >= 20) & (df['idade'] <= 30)]) / len(df)
            
            # Resultados
            print(f"\nMédia: {media}")
            print(f"Mediana: {mediana}")
            print(f"Moda: {moda}")
            print(f"Variância: {variancia}")
            print(f"Desvio Padrão: {desvio_padrao}")
            print(f"Amplitude: {amplitude}")
            print(f"Probabilidade de ter 30 anos: {prob_idade_30}")
            print(f"Probabilidade de ter entre 20 e 30 anos: {prob_intervalo}")
            
            # Gerar gráficos
            plt.figure(figsize=(14, 10))
            
            # Gráficos de barras para medidas estatísticas
            plt.subplot(2, 2, 1)
            plt.bar(['Média', 'Mediana', 'Moda'], [media, mediana, moda], color=['blue', 'green', 'red'])
            plt.title('Medidas de Posição')
            plt.ylabel('Valor')
            
            plt.subplot(2, 2, 2)
            plt.bar(['Variância', 'Desvio Padrão', 'Amplitude'], [variancia, desvio_padrao, amplitude], color=['purple', 'orange', 'cyan'])
            plt.title('Medidas de Dispersão')
            plt.ylabel('Valor')
            
            # Gráfico de pizza para probabilidades
            plt.subplot(2, 2, 3)
            plt.pie([prob_idade_30, prob_intervalo], 
                    labels=['Probabilidade 30 anos', 'Probabilidade 20-30 anos'], 
                    autopct='%1.1f%%', 
                    startangle=140)
            plt.title('Probabilidades')
            
            plt.tight_layout()
            plt.show()
            
        else:
            print("Nenhuma idade encontrada na tabela.")

except Exception as e:
    print(f"Erro ao conectar ao MySQL ou processar dados: {e}")

finally:
    # Fechar a conexão se ela foi estabelecida
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexão com o MySQL foi encerrada.")
