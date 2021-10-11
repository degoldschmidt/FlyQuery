import pygsheets as pyg
from pygsheets.client import Client

def authorize(jsonfile=None, custom_credentials=None):
    try:
        if custom_credentials is not None:
            return pyg.authorize(custom_credentials=custom_credentials)
        elif jsonfile is None:
            return pyg.authorize()
        else:
            return pyg.authorize(client_secret=jsonfile)
    except FileNotFoundError:
        print('Client_secret.json has not been found. Please go here {} and follow the steps shown below:\n'.format('https://console.cloud.google.com/apis/dashboard'))
        print('1) Click on \"Credentials\" in the left bar. Create a project if you have not done so before. You can give it any name.')
        print('2) Click on \"+ CREATE CREDENTIALS\" in the top bar and choose the option \"OAuth client ID\".')
        print('3) Follow the instructions to configure a consent screen and create your credentials.')
        print('4) Download the json file and add its path to the jsonfile keyword of this authorize function.')
        print('More detailed instructions can be found here: https://pygsheets.readthedocs.io/en/stable/authorization.html')

class GoogleClient(Client):
    def __init__(self, jsonfile=None, custom_credentials=None):
        self.client = authorize(jsonfile=jsonfile, custom_credentials=custom_credentials)

    def list_sheets(self):
        return sorted(self.client.spreadsheet_titles())

    def read_sheet(self, _id, sheet=None):
        if sheet is None:
            return self.client.open(_id).sheet1.get_as_df()
        else:
            return self.client.open(_id).worksheet('title', sheet).get_as_df()
