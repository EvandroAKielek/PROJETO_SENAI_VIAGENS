import pandas as pd

# Teste com Latin-1
df = pd.read_csv("2025_Viagem.csv", sep=";", encoding="latin-1")
print(df.head())

# Se ainda der erro, teste com ISO-8859-1
df = pd.read_csv("2025_Viagem.csv", sep=";", encoding="ISO-8859-1")
print(df.head())
