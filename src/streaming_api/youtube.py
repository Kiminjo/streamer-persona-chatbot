import os
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

os.chdir(Path(__file__).resolve().parents[2])

def convert_chat_format(chat: str,
                        livechatid: str,
                        display_content: bool = True
                        ):
    snippet = {
        'snippet': {
            'liveChatId': livechatid,
            'type': 'textMessageEvent',
            'hasDisplayContent': display_content,
            'textMessageDetails': {
                'messageText': chat
            }
        }
    }
    return snippet

class YouTubeAPI:
    def __init__(self, 
                 client_secrets_file: str, 
                 scopes: list = ['https://www.googleapis.com/auth/youtube.force-ssl'], 
                 api_service_name: str = 'youtube', 
                 api_version: str = 'v3', 
                ):
        
        self.CLIENT_SECRETS_FILE = client_secrets_file
        self.SCOPES = scopes
        self.API_SERVICE_NAME = api_service_name
        self.API_VERSION = api_version

        # Get authenticated service
        self.service = self._get_authenticated_service()

        # Get livechatid
        self.livechatid = self._get_livechatid('active')

    def _get_authenticated_service(self,
                                   port: int = 0):
        flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, 
                                                         self.SCOPES)
        credentials = flow.run_local_server(port=port)
        return build(self.API_SERVICE_NAME, 
                     self.API_VERSION, 
                     credentials=credentials)
    
    def _get_livechatid(self, broadcast_status: str):
        list_broadcasts_request = self.service.liveBroadcasts().list(
            broadcastStatus=broadcast_status,
            part='id,snippet',
            maxResults=50
        )

        list_broadcasts_response = list_broadcasts_request.execute()

        return list_broadcasts_response['items'][0]['snippet']['liveChatId']
    
    def get_live_chat(self,
                      part: str = 'id,snippet,authorDetails',
                      nextpagetoken: str = None
                      ):
        if nextpagetoken:
            response = self.service.liveChatMessages().list(
                liveChatId=self.livechatid,
                part=part,
                pageToken=nextpagetoken
            ).execute()

        else:
            response = self.service.liveChatMessages().list(
                liveChatId=self.livechatid,
                part=part
            ).execute()

        nextpagetoken = response['nextPageToken']
        output_chat = []

        for chat in response.get('items', []):
            output_chat.append(chat['snippet']['textMessageDetails']['messageText'])
        return output_chat, nextpagetoken
    
    def send_live_chat(self,
                       snippet: dict
                       ):
        self.service.liveChatMessages().insert(
            part='snippet',
            body=snippet
        ).execute()
        
        

if __name__=="__main__":
    yt = YouTubeAPI('client_secret.json')
    chat, nextpagetoken = yt.get_live_chat()
    print(chat)

    snippet = convert_chat_format('소소연 사랑해', yt.livechatid)
    yt.send_live_chat(snippet)
    print("here")

    snippet = convert_chat_format('소소연 뻐뀨', yt.livechatid, False)
    yt.send_live_chat(snippet)
    print("here")
