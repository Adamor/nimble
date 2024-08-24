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

# Parsing template for extracting product name, price, and description
parsing_template = {
    "product_name": {
        "type": "item",
        "selectors": ["//h1"],
        "extractor": "text"
    },
    "price": {
        "type": "item",
        "selectors": ["//span[@class='price-per-sellable-unit']"],
        "extractor": "text"
    },
    "product_description": {
        "type": "item",
        "selectors": ["//div[@class='product-details-tile-description']"],
        "extractor": "text"
    }
}

# URL to scrape
url_to_scrape = "https://www.tesco.com/groceries/en-GB/products/299154020"

# Payload for the API request
payload = {
    "url": url_to_scrape,
    "method": "GET",
    "parse": parsing_template,  # Use the parsing template directly here
    "render": True,  # Enable rendering for dynamic content
    "country": "US",  # Set country
}

# Send the scrape request
logging.info(f"Sending scrape request to {url_to_scrape}")
response = requests.post(api_base_url, headers=headers, json=payload)
logging.info(f"Response status code: {response.status_code}")

# Handle the response
if response.status_code == 200:
    result = response.json().get('result')
    if result:
        parsed_data = result.get('parse')
        if parsed_data:
            print("Parsed Data:")
            print(f"Product Name: {parsed_data.get('product_name')}")
            print(f"Price: {parsed_data.get('price')}")
            print(f"Description: {parsed_data.get('product_description')}")
        else:
            print("No parsed data found in the response")
    else:
        print("No HTML content found in the response")
else:
    print(f"Failed to scrape: {response.status_code}")