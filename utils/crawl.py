import re
import requests


def get_origin_view_count(url):
    for i in range(5):
        try:
            res = requests.get(
                url=url,
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                    "referer": "https://m.yangshipin.cn/"
                },
            )
            match_object = re.findall(r'"subtitle":"(.+)次观看","', res.text)
            if not match_object:
                return True, 0
            return True, match_object[0]
        except Exception as e:
            print(e)
            pass
    return False, 0
