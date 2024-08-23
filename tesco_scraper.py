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

# Nimbleway API base URL (adjust based on the actual API documentation)
api_base_url = "https://api.webit.live/api/v1/realtime/web"

# Parsing template for extracting product name, price, and description
parsing_template = {
    "product_name": {
        "type": "item",
        "selectors": ["h1"],
        "extractor": "text"
    },
    "price": {
        "type": "item",
        "selectors": ["p.text__StyledText-sc-1jpzi8m-0.lmgzsH.ddsweb-text.styled__PriceText-sc-v0qv7n-1"],
        "extractor": "text"
    },
    "product_description": {
        "type": "item",
        "selectors": ["#accordion-panel-product-description > div > div:nth-child(2) > span"],
        "extractor": "text"
    }
}

# Function to scrape a single product URL and info using the parsing template
def scrape_product(url):
    # Payload for the API request
    payload = {
        "url": url,
        "method": "GET",
        "parse": parsing_template,  # Use the parsing template directly here
        "render": True,  # Enable rendering for dynamic content
        "country": "GB",  # Set country
    }

    # Send the scrape request
    response = requests.post(api_base_url, headers=headers, json=payload)

    # Handle the response
    if response.status_code == 200:
        # Extract parsed data from the response
        parsed_data = response.json().get('parsing')
        if parsed_data:
            return {
                'url': url,
                'product_name': parsed_data.get('product_name'),
                'price': parsed_data.get('price'),
                'description': parsed_data.get('product_description'),
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
