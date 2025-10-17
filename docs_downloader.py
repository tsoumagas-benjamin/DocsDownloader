import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import urllib.request
import requests
from pathlib import Path
from tkinter.filedialog import askdirectory
from tkinter import simpledialog

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

# The ID of a sample document.
DOCUMENT_ID = "1mu8mOlSC439LqktMk1ADbl1vDgY6-h_j6d_Kv2Z191U"

#Function to prompt folder location for downloads and the Google Docs link
def prompt_user():
  link = simpledialog.askstring(
    title="Google Docs Link", 
    prompt="What is the link to the Google Docs?"
  )
  docs_id = link.split("/")[5]
  folder = askdirectory()

  return docs_id, folder

# Function to check the file type of a given URL
def get_file_type(url: str):
  
  # Perform a HEAD request to the URL and check Content Type header
  response = requests.head(url)
  content_type = response.headers['Content-Type']

  # Split response on / and return whatever is after. i.e. image/png becomes png
  return content_type.split('/')[1]

# Function to dynamically create files TODO: Include folder path
def create_file(file_type: str, iterable: int, content_uri: str, folder: str):
  # Create the file name given
  file_name = f"media{iterable}.{file_type}"
  full_path = Path(folder) / file_name

  # Retrieve the content and store it in the given file name
  urllib.request.urlretrieve(content_uri, full_path)
  return file_name

# Function to get the order of media in the Google Docs
def get_media_order(body: dict):
  inline_object_ids = []

  # Iterate over all body objects and if they are inlineObjects store their IDs in the array
  for object in body['content']:
    if "paragraph" in object:
      try:
        inline_object_id = object['paragraph']['elements'][0]['inlineObjectElement']['inlineObjectId']
        inline_object_ids.append(inline_object_id)
      except:
        pass

  return inline_object_ids

# Function to create a dict with media id and uri, then arrange them for download in order
def order_media(inline_objects: dict):
  media_dict = {}

  # Iterate over each object and store it in a dict
  for inline_object in inline_objects:
    object_id = inline_objects[inline_object]['objectId']
    content_uri = inline_objects[inline_object]['inlineObjectProperties']['embeddedObject']['imageProperties']['contentUri']
    media_dict[object_id] = content_uri

  return media_dict

# Function to download all the media objects in sequence
def download_media(id_list: list, media_dict: dict, folder: str):

  # Iterate over each object and download it
  for position, id in enumerate(id_list, start=1):
    target_uri = media_dict[id]
    file_type = get_file_type(target_uri)
    create_file(file_type, position, target_uri, folder)

def main():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("docs", "v1", credentials=creds)

    # Prompt the user for the folder location to download to and the Google Docs link
    docs_id, folder = prompt_user()

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=docs_id).execute()

    print(f"The title of the document is: {document.get('title')}")

    # Get the order of IDs for media objects in the Google Docs
    inline_object_ids = get_media_order(document.get('body'))

    # Order the media based on their order in the document
    media_dict = order_media(document.get('inlineObjects'))

    # Download each media object in order
    download_media(inline_object_ids, media_dict, folder)
      
  except HttpError as err:
    print(err)

if __name__ == "__main__":
  main()