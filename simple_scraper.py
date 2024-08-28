import requests
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials for authentication
username = 'cs-candidate@nimbleway.com'
password = 'JoinUs321!@'

# Encode credentials in base64
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# Set up headers with the encoded credentials
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json'
}


# Nimbleway API base URL
api_base_url = "https://api.webit.live/api/v1/realtime/web"

# URL to scrape
url_to_scrape = "https://www.tesco.com/groceries/en-GB/products/310162011"

# Payload for the API request
payload = {
    "url": url_to_scrape,
    "method": "GET",
    "format": "json",
    "parse": True,  # Enable parsing for dynamic content
    "render": True,  # Enable rendering for dynamic content
    "render_options": {
        "timeout": 60000,  # Wait up to 35 seconds for the page to fully load
        "render_type": "idle0"  # Consider the page fully loaded when no new network requests are made in the last 500ms
    },
    "country": "US",  # Set country
}

# Send the scrape request
logging.info(f"Sending scrape request to {url_to_scrape}")
response = requests.post(api_base_url, headers=headers, json=payload)
logging.info(f"Response status code: {response.status_code}")

# Handle the response
if response.status_code == 200:
    result = response.json()
    # logging.info(f"Response JSON: {response.json()}")
    if result and 'parsing' in result:
        parsed_data = result['parsing']['entities']['Product'][0]  # Access the 'Product' entity
        
        # Extract product name, price, and description
        product_name = parsed_data.get('name')
        product_description = parsed_data.get('description')
        product_price = parsed_data['offers'].get('price')

        # Print the extracted data
        print("Parsed Data:")
        print(f"Product Name: {product_name}")
        print(f"Price: {product_price} GBP")
        print(f"Description: {product_description}")
    else:
        print("No parsed data found in the response")
else:
    print(f"Failed to scrape: {response.status_code}")