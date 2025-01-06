import requests
import logging
from typing import Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommerceToolsClient:
    def __init__(self, project_key, client_id, client_secret):
        self.project_key = project_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = "https://auth.europe-west1.gcp.commercetools.com/oauth/token"
        self.api_url = "https://api.europe-west1.gcp.commercetools.com"
        self.token = None

    def get_token(self):
        response = requests.post(
            self.auth_url,
            auth=(self.client_id, self.client_secret),
            data={'grant_type': 'client_credentials'}
        )
        response.raise_for_status()
        self.token = response.json()['access_token']
        return self.token

    def get_users(self, limit: int = 20) -> list:
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f'{self.api_url}/{self.project_key}/customers',
            headers=headers,
            params={'limit': limit}
        )
        response.raise_for_status()
        return response.json()['results']

    def delete_user(self, user_id: str, version: int) -> None:
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.delete(
            f'{self.api_url}/{self.project_key}/customers/{user_id}',
            headers=headers,
            params={'version': version}
        )
        response.raise_for_status()

def delete_all_users(client: CommerceToolsClient, batch_size: int = 20, delay: float = 0.5):
    """
    Delete all users from CommerceTools with error handling and rate limiting.

    Args:
        client: Initialized CommerceToolsClient
        batch_size: Number of users to fetch per request
        delay: Delay between deletions in seconds
    """
    try:
        client.get_token()
        total_deleted = 0

        while True:
            users = client.get_users(limit=batch_size)
            if not users:
                break

            for user in users:
                try:
                    client.delete_user(user['id'], user['version'])
                    logger.info(f"Deleted user {user['id']}")
                    total_deleted += 1
                    time.sleep(delay)
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to delete user {user['id']}: {str(e)}")

        logger.info(f"Successfully deleted {total_deleted} users")

    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        raise

if __name__ == "__main__":
    PROJECT_KEY = "UPDATE"
    CLIENT_ID = "UPDATE"
    CLIENT_SECRET = "UPDATE"

    client = CommerceToolsClient(
        PROJECT_KEY,
        CLIENT_ID,
        CLIENT_SECRET
    )

    delete_all_users(client)
