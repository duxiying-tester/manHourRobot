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
    sendToWechat(constant.open_platform)

    

if __name__ == '__main__':

    schedule.every().monday.at("18:00").do(job)
    schedule.every().tuesday.at("18:00").do(job)
    schedule.every().wednesday.at("18:00").do(job)
    schedule.every().thursday.at("18:00").do(job)
    schedule.every().friday.at("18:00").do(job)
    # schedule.every().saturday.at("18:00").do(job)
    # schedule.every().sunday.at("18:00").do(job)

    while True:
        schedule.run_pending()

    # sendToWechat(constant.local_test)
