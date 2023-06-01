# encoding:utf-8
# 根据您选择的AK以为您生成调用代码
# 检测您当前的AK设置了sn检验，本示例中已为您生成sn计算代码
# encoding:utf-8
# python版本为3.6.2
import requests
import urllib
import hashlib
import json

def ParseJsonToObj(jsonStr, yourCls):
    parseData = json.loads(jsonStr.strip('\t\r\n'))
    result = yourCls()
    result.__dict__ = parseData
    return result


def ParseObjToJson(yourObj):
    return yourObj.__dict__.__str__().replace("\'", "\"")

# 服务地址
host = "https://api.map.baidu.com"

# 接口地址
uri = "/place/v2/search"

# 此处填写你在控制台-应用管理-创建应用后获取的AK
# ak = "Rv7zNDS6a6xltH5KZHbpnHfp8MNqqgyV"
ak = "kQ5mf5IdOF5L4vgPOrvYkgq5GQeQtBLZ"

# 此处填写你在控制台-应用管理-创建应用时，校验方式选择sn校验后生成的SK
# sk = "qbFwT7RHaIrTPvDPW5fOVazFsqGnab6z"
sk = "tIAex5rsrrA8oltTT7PW59PRfHxMUkg9"
# 设置您的请求参数
params = {
    "query": "住宅区",
    "tag": "房地产",
    "region": "北京市石景山区",
    "output": "json",
    "scope": "1",
    "page_size": "20",
    "page_num": "0",
    "ak": ak,

}
pageNum = 1
resultList = []
while True:
    # 拼接请求字符串
    paramsArr = []
    for key in params:
        paramsArr.append(key + "=" + params[key])

    queryStr = uri + "?" + "&".join(paramsArr)

    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = urllib.request.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上您的SK
    rawStr = encodedStr + sk

    # 计算sn
    sn = hashlib.md5(urllib.parse.quote_plus(rawStr).encode("utf8")).hexdigest()

    # 将sn参数添加到请求中
    queryStr = queryStr + "&sn=" + sn

    # 请注意，此处打印的url为非urlencode后的请求串
    # 如果将该请求串直接粘贴到浏览器中发起请求，由于浏览器会自动进行urlencode，会导致返回sn校验失败
    url = host + queryStr
    response = requests.get(url)
    if response:
        if response.json()['total'] <= 0:
            break
        resultList.append(response.json()['results'])
        # print(response.json())
        # print(json.dumps(response, ensure_ascii=False))
        params["page_num"] = str(pageNum)
        pageNum += 1
print(json.dumps(resultList, ensure_ascii=False))
    # print(str(json.dumps(resultList)))



