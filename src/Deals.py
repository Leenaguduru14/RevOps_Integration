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
            results = data.get('deals', [])
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
    deals_data = fetch_hubspot_data('deals/v1/deal/paged', limit=100)
    logger.info(f"Fetched {len(deals_data)} deals")

    
    if deals_data:
        logger.info("Sample deal properties:")
        logger.info(json.dumps(deals_data[0]['properties'], indent=2))

    # Extract relevant data
    deal_data = [
        {
            'ID': d['dealId'],
            'CREATEDAT': pd.to_numeric(d['properties'].get('createdate', {}).get('value'), errors='coerce'),
            'UPDATEDAT': pd.to_numeric(d['properties'].get('lastmodifieddate', {}).get('value'), errors='coerce'),
            'ARCHIVED': d.get('isDeleted', False),
            'AMOUNT': pd.to_numeric(d['properties'].get('amount', {}).get('value'), errors='coerce'),
            'CLOSEDATE': pd.to_numeric(d['properties'].get('closedate', {}).get('value'), errors='coerce'),
            'CREATEDATE': pd.to_numeric(d['properties'].get('createdate', {}).get('value'), errors='coerce'),
            'DEALNAME': d['properties'].get('dealname', {}).get('value', ''),
            'DEALSTAGE': d['properties'].get('dealstage', {}).get('value', ''),
            'HS_LASTMODIFIEDDATE': pd.to_numeric(d['properties'].get('lastmodifieddate', {}).get('value'), errors='coerce'),
            'HS_OBJECT_ID': d['dealId']
        }
        for d in deals_data
    ]

    # Convert date fields to appropriate format
    for deal in deal_data:
        if deal['CREATEDAT']:
            deal['CREATEDAT'] = pd.to_datetime(deal['CREATEDAT'], unit='ms')
        if deal['UPDATEDAT']:
            deal['UPDATEDAT'] = pd.to_datetime(deal['UPDATEDAT'], unit='ms')
        if deal['CLOSEDATE']:
            deal['CLOSEDATE'] = pd.to_datetime(deal['CLOSEDATE'], unit='ms')
        if deal['CREATEDATE']:
            deal['CREATEDATE'] = pd.to_datetime(deal['CREATEDATE'], unit='ms')
        if deal['HS_LASTMODIFIEDDATE']:
            deal['HS_LASTMODIFIEDDATE'] = pd.to_datetime(deal['HS_LASTMODIFIEDDATE'], unit='ms')

    # Save data to CSV files
    save_to_csv(deal_data, 'deals.csv')

    end_time = time.time()
    logger.info(f"Time taken to fetch deals: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()
