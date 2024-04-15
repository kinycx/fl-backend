import boto3
import sqlite3
from datetime import datetime

from podcast.models import Podcast

def get_s3_objects(bucket_name, prefix):
  s3 = boto3.client('s3')
  response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

  if 'Contents' in response:
    return [obj['Key'] for obj in response['Contents']]
  else:
    return []

def fetch_podcasts_from_database(database_path):
  conn = sqlite3.connect(database_path)
  cursor = conn.cursor()

  podcasts = []
  for row in cursor.execute('SELECT title, description, date, file_name FROM podcasts'):
    title, description, date_str, file_name = row
    date = datetime.strptime(date_str, '%Y-%m-%d')  # Assuming date format YYYY-MM-DD
    podcast = {
      'title': title,
      'description': description,
      'date': date,
      'file_name': file_name
    }
    podcasts.append(podcast)

  conn.close()
  return podcasts

def process_data(bucket_name, prefix, database_path):
  s3_objects = get_s3_objects(bucket_name, prefix)
  print(s3_object)
  podcasts_data = fetch_podcasts_from_database(database_path)
  print(podcast_data)

  for podcast_data in podcasts_data:
    for s3_object in s3_objects:
      if podcast_data['date'].strftime('%Y-%m-%d') in s3_object:
        podcast_data['file_url'] = f"https://{bucket_name}.s3.amazonaws.com/{s3_object}"
        Podcast.objects.create(**podcast_data)

bucket_name = 'podcast-fl'
prefix = 'mp3/'
database_path = './podcast_db.sqlite'

process_data(bucket_name, prefix, database_path)
