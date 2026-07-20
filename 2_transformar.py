import pandas as pd
from banco import conectar

def transformar_viagem():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("TRUNCATE silver_viagem;")
    conn.commit()

    df = pd.read_sql("SELECT * FROM raw_viagem;", conn)
    df = df.applymap(lambda x: str(x).strip() if pd.notnull(x) else None)

    for _, row in df.iterrows():
        valores = tuple(row.values)
        placeholders = ",".join(["%s"] * len(valores))
        sql = f"INSERT INTO silver_viagem VALUES ({placeholders})"
        cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabela silver_viagem carregada com sucesso!")

def transformar_passagem():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("TRUNCATE silver_passagem;")
    conn.commit()

    df = pd.read_sql("SELECT * FROM raw_passagem;", conn)

    # Conversão de datas
    df["data_inicio"] = pd.to_datetime(df["data_inicio"], errors="coerce")
    df["data_fim"] = pd.to_datetime(df["data_fim"], errors="coerce")

    # Conversão de valores
    for col in ["valor_diarias","valor_passagens","valor_devolucao","valor_outros_gastos"]:
        df[col] = df[col].str.replace(",", ".", regex=False).astype(float)

    # Colunas calculadas
    df["valor_total"] = df[["valor_diarias","valor_passagens","valor_devolucao","valor_outros_gastos"]].sum(axis=1)
    df["duracao_dias"] = (df["data_fim"] - df["data_inicio"]).dt.days

    for _, row in df.iterrows():
        valores = tuple(row.values)
        placeholders = ",".join(["%s"] * len(valores))
        sql = f"INSERT INTO silver_passagem VALUES ({placeholders})"
        cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabela silver_passagem carregada com sucesso!")

def transformar_pagamento():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("TRUNCATE silver_pagamento;")
    conn.commit()

    df = pd.read_sql("SELECT * FROM raw_pagamento;", conn)

    # Conversão de valores
    df["valor"] = df["valor"].str.replace(",", ".", regex=False).astype(float)

    for _, row in df.iterrows():
        valores = tuple(row.values)
        placeholders = ",".join(["%s"] * len(valores))
        sql = f"INSERT INTO silver_pagamento VALUES ({placeholders})"
        cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabela silver_pagamento carregada com sucesso!")

def transformar_trecho():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("TRUNCATE silver_trecho;")
    conn.commit()

    df = pd.read_sql("SELECT * FROM raw_trecho;", conn)

    # Conversão de datas
    df["origem_data"] = pd.to_datetime(df["origem_data"], format="%d/%m/%Y", errors="coerce")
    df["destino_data"] = pd.to_datetime(df["destino_data"], format="%d/%m/%Y", errors="coerce")

    # Conversão de valores
    df["numero_diarias"] = df["numero_diarias"].str.replace(",", ".", regex=False).astype(float)

    for _, row in df.iterrows():
        valores = tuple(row.values)
        placeholders = ",".join(["%s"] * len(valores))
        sql = f"INSERT INTO silver_trecho VALUES ({placeholders})"
        cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabela silver_trecho carregada com sucesso!")

if __name__ == "__main__":
    try:
        transformar_viagem()
        transformar_passagem()
        transformar_pagamento()
        transformar_trecho()
        print("Transformações concluídas!")
    except Exception as e:
        print("Erro durante a transformação:", e)
