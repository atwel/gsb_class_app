import json
from zoomus import ZoomClient

client = ZoomClient('API_KEY', 'ngluu3LPjIFhKHr2g6ks3tKdxjeNT5zo')

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))
