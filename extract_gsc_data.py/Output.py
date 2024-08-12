import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Chemin vers ton fichier JSON de clés de service Google
KEY_FILE = '/Users/coolingeoffrey/Downloads/cuisineconfort-service-account.json'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SITE_URL = 'https://cuisineconfort.com/'  # URL de ton site

# Authentification
credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('searchconsole', 'v1', credentials=credentials)

# Fonction pour extraire les données GSC
def extract_gsc_data(start_date, end_date):
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page', 'query'],
        'rowLimit': 10000  # Ajuste selon tes besoins
    }

    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()

    # Conversion en DataFrame
    data = []
    for row in response['rows']:
        data.append({
            'page': row['keys'][0],
            'query': row['keys'][1],
            'clicks': row['clicks'],
            'impressions': row['impressions'],
            'ctr': row['ctr'],
            'position': row['position']
        })

    return pd.DataFrame(data)

# Exemple d'utilisation
df = extract_gsc_data('2024-06-01', '2024-08-12')
df.to_csv('gsc_data.csv', index=False)
print("Extraction terminée ! Données sauvegardées dans 'gsc_data.csv'")
