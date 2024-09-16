import sqlite3
import csv

def migrate_to_db(csv_file):
    conn = sqlite3.connect('gov_sites.db')
    cursor = conn.cursor()

    # Cria a tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_name TEXT,
            url TEXT
        )
    ''')

    # Lê a planilha CSV
    with open(csv_file, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho, se houver
        for row in reader:
            # Remove espaços em branco nas bordas e ignora linhas vazias
            row = [item.strip() for item in row]
            if len(row) != 2 or not row[0] or not row[1]:
                print(f"Erro: linha inválida no CSV: {row}")
                continue
            site_name, url = row

            # Verifica se a URL já existe na tabela
            cursor.execute('SELECT url FROM sites WHERE url = ?', (url,))
            if cursor.fetchone() is None:
                print(f"Inserindo: {site_name}, {url}")  # Exibe as linhas lidas
                cursor.execute('INSERT INTO sites (site_name, url) VALUES (?, ?)', (site_name, url))
            else:
                print(f"URL já existente: {url}")

    conn.commit()
    conn.close()

# Exemplo de uso
migrate_to_db('sites_planilha.csv')
