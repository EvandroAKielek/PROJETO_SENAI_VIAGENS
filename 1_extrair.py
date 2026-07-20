import os
import zipfile
import gdown
import pandas as pd
from banco import conectar

# Caminho para salvar o arquivo zip
ZIP_PATH = r"C:\Users\user\Desktop\PROJETO_SENAI_VIAGENS\data\viagens.zip"
CSV_DIR = r"C:\Users\user\Desktop\PROJETO_SENAI_VIAGENS\data"

# ID do arquivo no Google Drive
DRIVE_FILE_ID = "1R6re1574aCeqNfwJXQ_T7BwHCEsPfgvc"
URL = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"

def baixar_zip():
    print("Baixando arquivo com gdown...")
    gdown.download(URL, ZIP_PATH, quiet=False)

    if not zipfile.is_zipfile(ZIP_PATH):
        raise Exception("O arquivo baixado não é um ZIP válido. Verifique permissões ou ID.")
    print("Download concluído!")

def extrair_zip():
    print("Extraindo arquivos...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(CSV_DIR)
    print("Extração concluída!")

def carregar_csv_para_raw(nome_csv, tabela_raw):
    print(f"Carregando {nome_csv} na tabela {tabela_raw}...")
    conn = conectar()
    cur = conn.cursor()

    cur.execute(f"TRUNCATE {tabela_raw};")
    conn.commit()

    file_path = os.path.join(CSV_DIR, nome_csv)

    # Lê CSV em blocos com encoding ISO-8859-1
    for chunk in pd.read_csv(
        file_path,
        sep=";",
        encoding="ISO-8859-1",   # força encoding correto
        on_bad_lines="skip",     # pula linhas problemáticas
        chunksize=1000
    ):
        for _, row in chunk.iterrows():
            valores = tuple(row.values)
            placeholders = ",".join(["%s"] * len(valores))
            sql = f"INSERT INTO {tabela_raw} VALUES ({placeholders})"
            cur.execute(sql, valores)
        conn.commit()

    cur.close()
    conn.close()
    print(f"{nome_csv} carregado com sucesso!")

if __name__ == "__main__":
    try:
        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)

        baixar_zip()
        extrair_zip()
        carregar_csv_para_raw("2025_Viagem.csv", "raw_viagem")
        carregar_csv_para_raw("2025_Pagamento.csv", "raw_pagamento")
        carregar_csv_para_raw("2025_Passagem.csv", "raw_passagem")
        carregar_csv_para_raw("2025_Trecho.csv", "raw_trecho")
        print("Carga concluída!")
    except Exception as e:
        print("Erro durante a execução:", e)
