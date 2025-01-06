import json
import requests
import logging
from typing import Dict, List, Any
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommerceToolsClient:
    def __init__(self, project_key: str, client_id: str, client_secret: str):
        self.project_key = project_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = "https://auth.europe-west1.gcp.commercetools.com/oauth/token"
        self.api_url = "https://api.europe-west1.gcp.commercetools.com"
        self.token = None

    def get_token(self) -> str:
        response = requests.post(
            self.auth_url,
            auth=(self.client_id, self.client_secret),
            data={'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        self.token = response.json()['access_token']
        return self.token

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f'{self.api_url}/{self.project_key}/customers',
            headers=headers,
            json=user_data
        )
        response.raise_for_status()
        return response.json()

def load_users_from_json(filename: str) -> List[Dict[str, Any]]:
    with open(filename, 'r') as f:
        return json.load(f)

def create_users(client: CommerceToolsClient, users: List[Dict[str, Any]], delay: float = 0.5):
    successful = 0
    failed = 0

    for user in users:
        try:
            result = client.create_user(user)
            logger.info(f"Created user: {result['customer']['email']}")
            successful += 1
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create user {user.get('email')}: {str(e)}")
            failed += 1

    logger.info(f"Creation complete. Successful: {successful}, Failed: {failed}")

if __name__ == "__main__":
    PROJECT_KEY = "CHANGEME"
    CLIENT_ID = "CHANGEME"
    CLIENT_SECRET = "CHANGEME"
    JSON_FILE = "users.json"

    client = CommerceToolsClient(
        PROJECT_KEY,
        CLIENT_ID,
        CLIENT_SECRET
    )

    try:
        client.get_token()
        users = load_users_from_json(JSON_FILE)
        create_users(client, users)
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise

"""
Example users.json file:
[
    {
        "email": "john.doe@example.com",
        "password": "SecurePass123!",
        "firstName": "John",
        "lastName": "Doe",
        "addresses": [
            {
                "country": "DE",
                "city": "Berlin",
                "postalCode": "10115",
                "streetName": "Alexanderplatz",
                "streetNumber": "1"
            }
        ]
    },
    {
        "email": "jane.smith@example.com",
        "password": "StrongPass456!",
        "firstName": "Jane",
        "lastName": "Smith",
        "addresses": [
            {
                "country": "DE",
                "city": "Munich",
                "postalCode": "80331",
                "streetName": "Marienplatz",
                "streetNumber": "8"
            },
            {
                "country": "DE",
                "city": "Hamburg",
                "postalCode": "20095",
                "streetName": "Rathausmarkt",
                "streetNumber": "1"
            }
        ]
    }
]
"""
