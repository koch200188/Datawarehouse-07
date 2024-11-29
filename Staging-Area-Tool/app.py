import pandas as pd

def extract_data_csv(file_path: str):
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
        print(f"Erfolgreich Daten aus {file_path} extrahiert")
        return df
    except Exception as e:
        print(f"Fehler beim Extrahieren der Daten aus {file_path}: {e}")
        return None

def extract_data_api():
    try: 
        pass
    except Exception as e:
        pass


def transform_data(df):
    try:
        pass
    except Exception as e:
        pass

def load_data_to_db(df, table_name):
    try:
        pass
    except Exception as e:
        pass

if __name__ == "__main__":
    migration_data = extract_data_csv('data/migration.csv')
    election_data = extract_data_csv('data/election2024_austria.csv')
    education_data = extract_data_csv('data/education.csv')
