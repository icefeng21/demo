import requests


def test(a, b, c):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f'实时新增用户反馈<font color=\"warning\">{a}</font>，'
                       f'请相关同事注意。\n> 类型:<font color=\"comment\">用户反馈</font>\n> '
                       f'普通用户反馈:<font color=\"comment\">{b}</font>\n> VIP用户反馈:<font color=\"comment\">{c}</font>'
        }
    }

    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=67f7f785-3d62-4973-afd2-8b800e34fda4"
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url=url, json=data, headers=headers)


test("121", "12321", "212")
