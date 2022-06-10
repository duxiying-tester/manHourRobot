import requests
import schedule
import ones
import constant

def sendToWechat(department):

    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + department["robot_key"]

    header = {'Content-Type': 'application/json'}

    body = {
        "msgtype": "markdown",
        "markdown": {
            "content": ones.robot_push_message(ones.getManHours(department))
        }
    }

    # 给企业微信发送信息
    requests.post(url=url, headers=header, json=body)


def job():
    sendToWechat(constant.open_platform_tester)

    

if __name__ == '__main__':

    schedule.every(0.5).minutes.do(job)

    while True:
        schedule.run_pending()

    # sendToWechat(constant.open_platform_tester)
