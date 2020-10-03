import json
from zoomus import ZoomClient

if __name__ == '__main__':

    API_KEY = 'u1rEgx9USkyu8pc6Um4wBw'
    API_SECRET = 'z1YXQb5BE4TdllUgLBeoAjVjMKNMMaxePFgJ'

    client = ZoomClient(API_KEY, API_SECRET)

    user_list_response = client.user.list()
    user_list = json.loads(user_list_response.content)

    for user in user_list['users']:
        user_id = user['id']
        print(json.loads(client.meeting.list(user_id=user_id).content))

    with ZoomClient('API_KEY', 'API_SECRET') as client:
        user_list_response = client.users.list()
        my_user = user_list['users'][0]
