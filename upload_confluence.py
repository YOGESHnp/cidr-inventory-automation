import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Confluence details
confluence_url = 'https://yogeshnptc.atlassian.net/wiki/rest/api/content/'  # Replace with your Confluence instance URL
username = os.getenv('CONFLUENCE_USERNAME')  # Your Confluence username (email) from .env
api_token = os.getenv('CONFLUENCE_API_TOKEN')  # API token from .env
space_key = 'MFS'  # Space key for 'My first space'
parent_page_id = None  # Replace with parent page ID if required

# Read the HTML content from the file
html_file = 'subnets.html'  # The HTML file you want to upload
with open(html_file, 'r') as file:
    html_content = file.read()

# Prepare the request payload
data = {
    "type": "page",
    "title": "New Page Title 4",  # Replace with the title you want for the new page
    "space": {
        "key": space_key
    },
    "body": {
        "storage": {
            "value": html_content,
            "representation": "storage"
        }
    }
}

# If you want to create the page under a specific parent, add the parent page ID
if parent_page_id:
    data["ancestors"] = [{"id": parent_page_id}]

# Set headers for the request
headers = {
    'Content-Type': 'application/json'
}

# Authenticate using HTTPBasicAuth
auth = HTTPBasicAuth(username, api_token)

# Send the POST request to create the page
response = requests.post(
    confluence_url,
    auth=auth,
    headers=headers,
    data=json.dumps(data)
)

# Check if the request was successful
if response.status_code == 200 or response.status_code == 201:
    print("Page created successfully.")
    print("View the page at:", response.json()["_links"]["webui"])
elif response.status_code == 403:
    print("Failed to create the page. Status code: 403")
    print("Reason: Current user does not have permission to use Confluence.")
else:
    print(f"Failed to create the page. Status code: {response.status_code}")
    print("Response:", response.json())
