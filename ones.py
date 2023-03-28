import constant
import login
import requests
import datetime


def getManHours(department):
    
    # 获取当前时间
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    # 获取上周一的时间
    last_week = now - datetime.timedelta(days=6)
    last_week_str = last_week.strftime('%Y-%m-%d')
    # print(last_week_str, now_str)
    
    # 获取团队成员的工时
    url = constant.BASE_URL + constant.PROJECT + '/team/' + login.team_uuid + '/items/graphql'

    headers = {
        'Ones-User-ID': login.user_uuid,
        'Ones-Auth-Token': login.user_token
    }

    query = '''{
        buckets(groupBy: $groupBy, filter: $filter, orderBy: $orderBy) {    
            key
            columnField: aggregateUser(source: $columnSource) {
                name
            }
            actualHoursSeries(timeSeries: $timeSeries) {
                times        
                values
            } 
        } 
    }'''

    variables = {
        "groupBy": {
            "users": {
                "uuid": {}
            }
        },
        "filter": {
            "users": {
                "uuid_in": [ user["user_uuid"] for user in department["user_infos"] ]
            }
        },
        "timeSeries": {
            "timeField": "users.manhours.startTime",
            "valueField": "users.manhours.hours",
            "unit": "day",
            # "quick": "last_7_days" # last_7_days  this_week
            "from": last_week_str,
            "to": now_str,
        },
        "columnSource": "uuid",
        "orderBy":{"aggregateUser":{"namePinyin":"ASC"}}
    }

    # graphql请求，在python中的写法
    response = requests.post(url=url, headers=headers, json={'query': query, 'variables': variables}).json()
    # print(json.dumps(response, indent=4, separators=(',', ':')))


    text_list = []
    for person in response['data']['buckets']:
        times = [time[5:] for time in person['actualHoursSeries']['times']]
        # name = str(person['columnField']['name']).ljust(3, '　') # 空汉字，需要「全角」空格
        name = person['columnField']['name']
        values = [str(value/100000).ljust(1, ' ') for value in person['actualHoursSeries']['values']]


        text_list.append({"times":'🕙'.join(times), "values":' / '.join([str(a) for a in values]), "user_name":name})

    return text_list


def robot_push_message(text_list):
    member_text = ""
    for text in text_list:
        title = "工时提醒：请同学们根据工时记录检查是否及时登记工时~\n" + text["times"] + "\n"
        member_text = member_text + text["user_name"] + "\n" + text["values"] + "\n"
    
    # print(title + member_text)

    return title + member_text



if __name__ == '__main__':

    text_list = getManHours()
    robot_push_message(text_list)