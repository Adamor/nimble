import pandas as pd
import requests
import base64

# Load the list of Tesco product URLs from the Excel file
file_path = 'Nimble Assignment (1).xlsx'  # Adjust the path as needed
sheet_name = 'Tesco'

# Read the Excel sheet with URLs
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract URLs
urls = df['url'].tolist()

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

# Function to build the parsing payload for a specific URL
def build_parsing_payload(url):
    return {
        "url": url,
        "parse": True,
        "format": "json",
        "render": True,
        "country": "US",
        "parser": {
            "product_title": {
                "type": "item",
                "selectors": ["h1.product-details-tile__title"],
                "extractor": "text"
            },
            "price": {
                "type": "item",
                "selectors": ["span.value"],
                "extractor": "text"
            },
            "product_description": {
                "type": "item",
                "selectors": ["div.product-info-block p"],
                "extractor": "text"
            }
        }
    }

# Function to scrape a single product URL using the parsing template
def scrape_product(url):
    # Build the payload for the API request
    payload = build_parsing_payload(url)

    # Send the scrape request
    response = requests.post(api_base_url, headers=headers, json=payload)

    # Handle the response
    if response.status_code == 200:
        # Extract parsed data from the response
        parsed_data = response.json().get('parsed_data')
        if parsed_data:
            return {
                'url': url,
                'product_title': parsed_data.get('product_title'),
                'price': parsed_data.get('price'),
                'product_description': parsed_data.get('product_description'),
            }
        else:
            return {
                'url': url,
                'error': 'No parsed data found in the response'
            }
    else:
        return {
            'url': url,
            'error': f"Failed to scrape: {response.status_code}, {response.json()}"
        }

# Loop through URLs and scrape product details
product_details = []
for url in urls:
    product_details.append(scrape_product(url))

# Convert the list of dictionaries to a DataFrame
result_df = pd.DataFrame(product_details)

# Save the scraped data to a CSV file
output_file = "scraped_product_details.csv"
result_df.to_csv(output_file, index=False)

print(f"Scraping complete. Data saved to {output_file}")
