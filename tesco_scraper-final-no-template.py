import pandas as pd
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the list of Tesco product URLs from the Excel file
file_path = 'Nimble Assignment (1).xlsx'  # Adjust the path as needed
sheet_name = 'Tesco'

# Read the Excel sheet with URLs
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract URLs
urls = df['url'].tolist()

headers = {
    'Authorization': f'Basic Y3MtY2FuZGlkYXRlQG5pbWJsZXdheS5jb206Sm9pblVzMzIxIUA=',
    'Content-Type': 'application/json'
}

# Nimbleway API base URL
api_base_url = "https://api.webit.live/api/v1/realtime/web"

# Function to scrape a single product URL and info using the parsing template
def scrape_product(url):
    # Payload for the API request
    payload = {
        "url": url,
        "method": "GET",
        "format": "json",
        "parse": True,  # Enable parsing for dynamic content
        "render": True,  # Enable rendering for dynamic content
        "render_options": {
            # "timeout": 60000,  # Set timeout to 60 seconds
            "render_type": "idle0" # Consider the page fully loaded when no new network requests are made in the last 500ms
        },
        "country": "GB",  # Set country
    }

    # Send the scrape request
    logging.info(f"Sending scrape request to {url}")
    response = requests.post(api_base_url, headers=headers, json=payload)
    logging.info(f"Response status code: {response.status_code}")

    # Handle the response
    if response.status_code == 200:
        result = response.json()
       # logging.debug(f"Response JSON: {response.json()}")
        if result and 'parsing' in result:
            parsed_data = result['parsing'].get('entities', {}).get('Product', [])
            if parsed_data:
                parsed_data = parsed_data[0]  # Assuming the first 'Product' entity
                return {
                    'url': url,
                    'product_name': parsed_data.get('name'),
                    'price': parsed_data['offers'].get('price'),
                    'description': parsed_data.get('description')
                }
            else:
                return {
                    'url': url,
                    'error': 'No Product data found in the response'
                }
        else:
            logging.warning("No HTML content found in the response")
            logging.error(f"Failed to scrape: {response.json().get('error')}")
            logging.debug(f"Response JSON: {response.json()}")
            return {
                'url': url,
                'error': f"Failed to scrape: {response.json().get('error')}"
            }
    else:
        logging.error(f"Failed to scrape: {response.status_code}")
        logging.debug(f"Response text: {response.text}")
        return {
            'url': url,
            'error': f"Failed to scrape: {response.status_code}"
        }

# Loop through URLs and scrape product details
product_details = []
for url in urls:
    product_details.append(scrape_product(url))

# Convert the list of dictionaries to a DataFrame
result_df = pd.DataFrame(product_details)

# Save the scraped data to a CSV file
output_file = "scraped_product_details-4.csv"
result_df.to_csv(output_file, index=False)

print(f"Scraping complete. Data saved to {output_file}")
