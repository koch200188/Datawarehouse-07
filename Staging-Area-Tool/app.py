import pandas as pd
import requests
from sqlalchemy import create_engine

def extract_data_csv(file_path: str):
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
        print(f"Erfolgreich Daten aus {file_path} extrahiert")
        return df
    except Exception as e:
        print(f"Error extracting data from {file_path}: {e}")
        return None


def extract_data_api(api_url: str):
    try:
        response = requests.get(api_url)

        data = response.json()
        timestamps = data.get('timestamps', [])
        features = data.get('features', [])

        if not timestamps or not features:
            print("Required data not found in the API response.")
            return None

        feature = features[0]
        properties = feature.get("properties", {}).get("parameters", {})
        station_id = feature.get("properties", {}).get("station", None)

        df = pd.DataFrame({'timestamp': pd.to_datetime(timestamps)})

        params = ['ff', 'p', 'rf', 'rr', 'tl']
        for param in params:
            if param in properties:
                df[param] = properties[param].get('data', [])

        df['station'] = station_id

        print(f"Erfolgreich API Daten extrahiert")
        return df
    except Exception as e:
        print(f"Error extracting data from API: {e}")
        return None


def transform_population_data(data):
    try:
        data = data.drop(columns=['AGR3', 'SEX', 'NUTS', 'REF_YEAR', 'DISTRICT_CODE'])
        data = data.rename(columns={
            'SUB_DISTRICT_CODE': 'districtCode',
            'REF_DATE': 'date',
            'AUT': 'austrianCitizens',
            'FOR': 'foreignCitizens',
        })
        data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y%m%d')

        aggregated_data = data.groupby(
            ['districtCode', 'date'], as_index=False
        ).agg({
            'austrianCitizens': 'sum',
            'foreignCitizens': 'sum'
        })


        print(f'Population:\n{aggregated_data.head()}')
        return aggregated_data
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None

def transform_election_data(data):
    try:
        data['OTHER'] = data[['BIER', 'MFG', 'BGE', 'LMP', 'GAZA', 'KPÖ', 'KEINE']].sum(axis=1, skipna=True)
        data = data.drop(columns=['BIER', 'MFG', 'BGE', 'LMP', 'GAZA', 'KPÖ', 'KEINE', 'Wahlberechtigte', 'Abgegebene', 'Ungültige', 'Gültige'])

        data = data.rename(columns={
            'Gebietsnummer': 'districtCode',
            'Gebietsname': 'districtName',
            'ÖVP': 'övpVotes',
            'SPÖ': 'spöVotes',
            'FPÖ': 'fpöVotes',
            'GRÜNE': 'grüneVotes',
            'NEOS': 'neosVotes',
            'OTHER': 'otherVotes'
        })

        data['districtCode'] = data['districtCode'].str[1:]

        data['date'] = '2024-09-29 00:00:00'

        aggregated_data = data.groupby(
            ['districtCode', 'districtName'], as_index=False
        ).sum()
        
        location_data = aggregated_data[['districtCode', 'districtName']].drop_duplicates()

        aggregated_data = data.drop(columns=['districtName'])

        print(f'Election:\n{aggregated_data.head()}')
        return aggregated_data, location_data
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None 

def transform_education_data(data):
    try:
        data = data.dropna(axis=1, how='all')
        data = data.drop(columns=['NUTS', 'REF_YEAR', 'DISTRICT_CODE'])

        cols_to_convert = ['EDU_UNI', 'EDU_ACA', 'EDU_AKA', 'EDU_LEH', 'EDU_BMS', 'EDU_BHS', 'EDU_KOL', 'EDU_AHS', 'EDU_ALL']
        for col in cols_to_convert:
            if col in data.columns:
                data[col] = data[col].str.replace(',', '.').astype(float)

        data['academicEducation'] = data[['EDU_UNI', 'EDU_ACA', 'EDU_AKA']].sum(axis=1, skipna=True)
        data['statutoryEducation'] = data['EDU_ALL']
        data['highschoolEducation'] = data['EDU_AHS']
        data['vocationalEducation'] = data[['EDU_LEH', 'EDU_BMS', 'EDU_BHS', 'EDU_KOL']].sum(axis=1, skipna=True)

        data = data.drop(columns=['EDU_LEH', 'EDU_BMS', 'EDU_BHS', 'EDU_KOL', 'EDU_AHS', 'EDU_ALL', 'EDU_UNI', 'EDU_ACA', 'EDU_AKA'])

        data = data.rename(columns={
            'SUB_DISTRICT_CODE': 'districtCode',
            'REF_DATE': 'date',
        })

        data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y%m%d')

        aggregated_data = data.groupby(
            ['districtCode', 'date'], as_index=False
        ).sum()

        print(f'Education:\n{aggregated_data.head()}')
        return aggregated_data
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None

def transform_weather_data(data):
    try:
        if data is None:
            print("No data available to transform.")
            return None

        if not all(col in data.columns for col in ['timestamp', 'ff', 'p', 'rf', 'rr', 'tl']):
            print("Expected columns are missing. Check the data extraction step.")
            return None
        
        data = data.drop(columns=['station'])
        data['districtCode'] = 90000
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        numeric_columns = ['ff', 'p', 'rf', 'rr', 'tl']
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')


        data = data.rename(columns={
            'timestamp': 'date',
            'ff': 'wind',
            'p': 'airPressure',
            'rf': 'humidity',
            'rr': 'rainfall',
            'tl': 'temperature',
        })

        print(f'Weather:\n{data.head()}')
        return data
    except Exception as e:
        print(f"Error transforming weather data: {e}")
        return None


def create_db_engine():
    db_url = "postgresql://admin:Kennwort1@localhost:5432/datawarehouse"
    engine = create_engine(db_url)
    return engine

def load_data_to_db(data, table_name:str):
    try:
        if data is not None and not data.empty:
            engine = create_db_engine()

            data.to_sql(table_name, engine, if_exists='replace', index=False)

            print(f"Data successfully loaded into {table_name} table.")
        else:
            print(f"No data available to load into {table_name}.")
    except Exception as e:
        print(f"Error loading data into {table_name}: {e}")


if __name__ == "__main__":
    population_data = extract_data_csv('data/population.csv')
    election_data = extract_data_csv('data/election2024-09-29_austria.csv')
    education_data = extract_data_csv('data/education.csv')
    weather_data = extract_data_api('https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1h?parameters=P%2CTL%2CRF%2CFF%2CRR&start=2024-09-29T00%3A00&end=2024-09-30T00%3A00&station_ids=5925&output_format=geojson')

    transformed_population_data = transform_population_data(population_data)
    transformed_election_data, transformed_location_data = transform_election_data(election_data)
    transformed_education_data = transform_education_data(education_data)
    transformed_weather_data = transform_weather_data(weather_data)

    load_data_to_db(transformed_population_data, 'PopulationData')
    load_data_to_db(transformed_election_data, 'ElectionData')
    load_data_to_db(transformed_education_data, 'EducationData')
    load_data_to_db(transformed_weather_data, 'WeatherData')
    load_data_to_db(transformed_location_data, 'Location')
