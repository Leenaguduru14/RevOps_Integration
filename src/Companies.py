import requests
import pandas as pd
import time
import json
import logging


HUBSPOT_BEARER_TOKEN = 'pat-na1-6bc6478a-184c-48ae-b01c-f8fc7821109e'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {HUBSPOT_BEARER_TOKEN}'
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch data from HubSpot with pagination handling
def fetch_hubspot_data(endpoint, limit=100, max_pages=10):
    data_list = []
    url = f'https://api.hubapi.com/{endpoint}?limit={limit}'
    more_data = True
    pages_fetched = 0

    while more_data and pages_fetched < max_pages:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get('companies', [])
            data_list.extend(results)
            more_data = data.get('has-more', False)
            if more_data:
                if 'offset' in data:
                    url = f'https://api.hubapi.com/{endpoint}?limit={limit}&offset={data["offset"]}'
            pages_fetched += 1
        else:
            logger.error(f"Error fetching data from {url}: {response.status_code} - {response.text}")
            response.raise_for_status()

    return data_list


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def main():
    start_time = time.time()
    
    # Fetch data from HubSpot
    companies_data = fetch_hubspot_data('companies/v2/companies/paged', limit=100)
    logger.info(f"Fetched {len(companies_data)} companies")

    # Print a sample company to see available properties
    if companies_data:
        logger.info("Sample company properties:")
        logger.info(json.dumps(companies_data[0]['properties'], indent=2))

    # Extract relevant data
    company_data = [
        {
            'ID': c['companyId'],
            'CREATEDAT': pd.to_numeric(c['properties'].get('createdate', {}).get('value'), errors='coerce'),
            'UPDATEDAT': pd.to_numeric(c['properties'].get('lastmodifieddate', {}).get('value'), errors='coerce'),
            'ARCHIVED': c.get('isDeleted', False),
            'CREATEDATE': pd.to_numeric(c['properties'].get('createdate', {}).get('value'), errors='coerce'),
            'DOMAIN': c['properties'].get('domain', {}).get('value', ''),
            'HS_LASTMODIFIEDDATE': pd.to_numeric(c['properties'].get('lastmodifieddate', {}).get('value'), errors='coerce'),
            'HS_OBJECT_ID': c['companyId'],
            'NAME': c['properties'].get('name', {}).get('value', '')
        }
        for c in companies_data
    ]

    # Convert date fields to appropriate format
    for company in company_data:
        if company['CREATEDAT']:
            company['CREATEDAT'] = pd.to_datetime(company['CREATEDAT'], unit='ms')
        if company['UPDATEDAT']:
            company['UPDATEDAT'] = pd.to_datetime(company['UPDATEDAT'], unit='ms')
        if company['CREATEDATE']:
            company['CREATEDATE'] = pd.to_datetime(company['CREATEDATE'], unit='ms')
        if company['HS_LASTMODIFIEDDATE']:
            company['HS_LASTMODIFIEDDATE'] = pd.to_datetime(company['HS_LASTMODIFIEDDATE'], unit='ms')

    save_to_csv(company_data, 'companies.csv')

    end_time = time.time()
    logger.info(f"Time taken to fetch companies: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()
