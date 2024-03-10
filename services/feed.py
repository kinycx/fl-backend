import os
import boto3
from django.contrib.syndication.views import Feed
from botocore.exceptions import NoCredentialsError

from podcast.models import Podcast

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="eu-north-1",
)


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except NoCredentialsError:
        print("No AWS credentials found")
        return None

    # The response contains the presigned URL
    return response


class PodcastFeed(Feed):
    title = "Frequenza Libera Podcasts"
    link = "/podcast/"
    description = "Podcasts from Frequenza Libera"

    def items(self):
        return Podcast.objects.all().order_by("-insert_time")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.audio_url

    def item_enclosure_url(self, item):
        # Generate a presigned URL for the S3 object
        presigned_url = create_presigned_url("podcast-fl", item.audio_url)
        return presigned_url

    def item_enclosure_length(self, item):
        return item.duration

    def item_enclosure_mime_type(self, item):
        return "audio/mpeg"

    def item_enclosure_length(self, item):
        bucket_url = f"https://{BUCKET_NAME}.s3.{s3.meta.region_name}.amazonaws.com/"
        audio_file = s3.get_object(
            Bucket=BUCKET_NAME, Key=item.audio_url.replace(bucket_url, "")
        )
        return audio_file["ContentLength"]
