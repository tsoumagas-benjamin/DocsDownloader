# Docs Downloader
 This program is made to allow the user to download all the images from a given Google Docs to a given folder. It prompts the user for a Google Docs link and a folder where the media will be downloaded. Then it downloads all the media with sequential names (i.e. media1.png, media2.gif, etc.) with a high degree of accuracy. Depending on how the images are placed the API/tool may be unable to pick out the media so please keep this in mind and review what is downloaded.

 ## How to Run
1. Start by cloning the GitHub repository where you'd like the program to run.
   - Follow the steps here depending on how you'd like to clone this repository.
2. Make sure you have access to a Google Cloud project and a Google account. (https://workspace.google.com/intl/en_ca/)
3. Make sure you have Python 3.10.7 or later installed. (https://www.python.org/downloads/)
4. Make sure you have the pip package management tool installed. (https://pip.pypa.io/en/stable/installation/)
5. Follow these steps in Google's Python quickstart. (https://developers.google.com/workspace/docs/api/quickstart/python)
   - Enable the Google Docs API in the Google Cloud console.
   - Configure the OAuth consent screen.
   - Authorize credentials for a desktop application.
     - Make sure the downloaded JSON file gets renamed to `credentials.json` and is in the same folder as `docs_downloader.py`
   - Install the Google client library for Python:
     - `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
6. In a terminal of your choice, navigate to the folder containing `docs_downloader.py` and `credentials.json` and run the command `python3 docs_downloader.py` or `py docs_downloader.py`.
