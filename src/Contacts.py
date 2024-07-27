import requests
import pandas as pd
import time
import json
import logging

# HubSpot Bearer token
HUBSPOT_BEARER_TOKEN = 'pat-na1-6bc6478a-184c-48ae-b01c-f8fc7821109e'


headers = {
    'Authorization': f'Bearer {HUBSPOT_BEARER_TOKEN}'
}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_hubspot_data(endpoint, limit=100, max_pages=10):
    data_list = []
    url = f'https://api.hubapi.com/{endpoint}?limit={limit}'
    more_data = True
    pages_fetched = 0

    while more_data and pages_fetched < max_pages:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get('contacts', [])
            data_list.extend(results)
            more_data = data.get('has-more', False)
            if more_data:
                if 'vid-offset' in data:
                    url = f'https://api.hubapi.com/{endpoint}?limit={limit}&vid-offset={data["vid-offset"]}'
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
    contacts_data = fetch_hubspot_data('contacts/v1/lists/all/contacts/all', limit=100)
    logger.info(f"Fetched {len(contacts_data)} contacts")

    # Print a sample contact to see available properties
    if contacts_data:
        logger.info("Sample contact properties:")
        logger.info(json.dumps(contacts_data[0]['properties'], indent=2))

    # Extract relevant data
    contact_data = [
        {
            'ID': c['vid'],
            'CREATEDAT': pd.to_numeric(c['properties'].get('createdate', {}).get('value'), errors='coerce'),
            'UPDATEDAT': pd.to_numeric(c['properties'].get('lastmodifieddate', {}).get('value'), errors='coerce'),
            'ARCHIVED': False,
            'CREATEDATE': pd.to_numeric(c['properties'].get('createdate', {}).get('value'), errors='coerce'),
            'EMAIL': c['properties'].get('email', {}).get('value'),
            'FIRSTNAME': c['properties'].get('firstname', {}).get('value'),
            'HS_OBJECT_ID': c['vid'],
            'LASTMODIFIEDDATE': pd.to_numeric(c['properties'].get('lastmodifieddate', {}).get('value'), errors='coerce'),
            'LASTNAME': c['properties'].get('lastname', {}).get('value')
        }
        for c in contacts_data
    ]

    # Convert date fields to appropriate format
    for contact in contact_data:
        if contact['CREATEDAT']:
            contact['CREATEDAT'] = pd.to_datetime(contact['CREATEDAT'], unit='ms')
        if contact['UPDATEDAT']:
            contact['UPDATEDAT'] = pd.to_datetime(contact['UPDATEDAT'], unit='ms')
        if contact['CREATEDATE']:
            contact['CREATEDATE'] = pd.to_datetime(contact['CREATEDATE'], unit='ms').date()
        if contact['LASTMODIFIEDDATE']:
            contact['LASTMODIFIEDDATE'] = pd.to_datetime(contact['LASTMODIFIEDDATE'], unit='ms')


    save_to_csv(contact_data, 'contacts.csv')

    end_time = time.time()
    logger.info(f"Time taken to fetch contacts: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()
