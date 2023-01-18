import requests
import constant

url = constant.BASE_URL + constant.PROJECT + '/auth/login'

header = {'Content-Type': 'application/json'}

body = {
    'email': 'duxiying@ones.cn',
    'password': 'WO5531608wo'
}

response = requests.post(url= url, headers= header, json= body).json()
# print(json.dumps(response, indent=4, separators=(',',':')))

team_uuid = response['teams'][0]['uuid']
org_uuid = response['org']['uuid']
user_uuid = response['user']['uuid']
user_token = response['user']['token']
