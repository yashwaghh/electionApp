from google.cloud import secretmanager
import logging


def get_secret(secret_id: str, version_id: str = "latest", project_id: str = "election-project-096") -> str:
    """Retrieves a secret from Google Cloud Secret Manager."""
    try:
        client = secretmanager.SecretManagerServiceClient()

        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logging.warning(f"Could not retrieve secret {secret_id}: {e}")
        # Return fallback for local testing without actual secrets configured yet
        return "development_fallback_key"
