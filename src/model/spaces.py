from io import BytesIO
from boto3 import client
import json
import os


class Spaces:
    """A class for uploading to digital ocean spaces using the boto3 clients."""

    def __init__(self):
        self.__client: client = self.__get_client()

    def __get_client(self) -> client:
        """Return a boto3 client."""
        region_name: str = os.environ.get("REGION_NAME", "sfo3")
        return client(
            "s3",
            region_name=region_name,
            endpoint_url=f"https://{region_name}.digitaloceanspaces.com",
            aws_access_key_id=os.environ.get("ACCESS_ID", ""),
            aws_secret_access_key=os.environ.get("SECRET_KEY", ""),
        )

    def upload(self, data: dict, object_name: str) -> None:
        self.__client.put_object(
            Body=BytesIO(json.dumps(data).encode("utf-8")),
            Bucket=os.environ.get("BUCKET_NAME", ""),
            Key=object_name,
            ACL="public-read",
            ContentType="application/json",
        )
