import requests
import xlrd
import xlwt
import json

url = "http://newh-contract.nhservice.ke.com/home/decoration/contract/list"

params = {
    "type": "25",
    "form_type": "1,3,4,11",
    "approval_status": "1,2,3,4,5,6,7,8,9",
    "resblock_id": "1620055180617849"
}


class OrderContractInfoData:
    pass


def get_contract_info_by_dev_id(dev_id, url_cur):
    paramsArr = []
    params["resblock_id"] = dev_id
    contract_nos = []
    for key in params:
        paramsArr.append(key + "=" + params[key])

    url_cur = url_cur + "?" + "&".join(paramsArr)
    try:
        result = requests.get(url_cur)
        # print("result" + result)
    except Exception as e:
        print("request contract is exception:", e)
    resultJsonStr = result.json()
    if resultJsonStr['errno'] != 0:
        print("request contract is error!!!!!")
    else:
        data = resultJsonStr['data']
        if data and data['records']:
            records = data['records']
            for record in records:
                contract_nos.append(record['contract_no'])
            print("dev_id=" + dev_id + ",contract_nos=" + contract_nos.__str__())
        else:
            print("request contract result.data is null ,dev_id=", dev_id)

    # if result.json()[]
    if contract_nos.__len__() > 0:
        return contract_nos
    else:
        return

def get_city_info_by_dev_id(dev_id, url_cur):
    paramsArr = []
    params["resblock_id"] = dev_id
    contract_nos = []
    for key in params:
        paramsArr.append(key + "=" + params[key])

    url_cur = url_cur + "?" + "&".join(paramsArr)
    try:
        result = requests.get(url_cur)
        # print("result" + result)
    except Exception as e:
        print("request contract is exception:", e)
    resultJsonStr = result.json()
    if resultJsonStr['errno'] != 0:
        print("request contract is error!!!!!")
    else:
        data = resultJsonStr['data']
        if data and data['records']:
            records = data['records']
            for record in records:
                contract_nos.append(record['contract_no'])
            print("dev_id=" + dev_id + ",contract_nos=" + contract_nos.__str__())
        else:
            print("request contract result.data is null ,dev_id=", dev_id)

    # if result.json()[]
    if contract_nos.__len__() > 0:
        return contract_nos
    else:
        return


def process_contract_info(ocInfoArr):
    for ocInfo in ocInfoArr:
        # ocInfo = ocInfoArr[i]
        if ocInfo.dev_id:
            contract_nos = get_contract_info_by_dev_id(ocInfo.dev_id, url)
            if contract_nos:
                ocInfo.contract_nos = contract_nos
    # return ocInfoArr


# 读excel
def get_home_order_info_from_excle():
    # 打开Excel文件
    workbook = xlrd.open_workbook('/Users/xugao/Downloads/项目导出1685090745219.xls')
    # workbook = xlrd.open_workbook('/Users/xugao/Downloads/test1.xls')

    # 获取所有sheet名称
    # sheet_names = workbook.sheet_names()
    # print(sheet_names)
    # 获取第一个sheet
    sheet = workbook.sheet_by_index(0)
    # 获取第一行
    first_row = sheet.row_values(1)
    # 获取第一列的值
    # first_col = sheet.col_values(0)
    print(first_row)
    ocInfoArr = []

    for i in range(sheet.nrows):
        if i == 0:
            continue
        else:
            ocInfo = OrderContractInfoData()
            current_row = sheet.row_values(i)
            # 二赛道项目id
            ocInfo.home_project_id = current_row[0]
            # 大部
            ocInfo.project_big_area = current_row[2]
            # 新房家装项目id
            ocInfo.nh_project_Id = current_row[3]
            # 项目来源
            ocInfo.project_source = current_row[5]
            # 主体类型
            ocInfo.subject_type = current_row[6]
            # 新房楼盘名称
            ocInfo.dev_name = current_row[7]
            # 新房楼盘id
            ocInfo.dev_id = current_row[8]
            # 合作模式
            ocInfo.cooperate_model = current_row[9]
            # 合同编号
            ocInfo.contract_nos = []
            ocInfo.city_id = 0
            ocInfo.city_name = ''
            if (
                    ocInfo.project_source == "城市业务-一赛道新房-客发导流" or ocInfo.project_source == "城市业务-一赛道新房-新代理导流") and ocInfo.subject_type == "开发商":
                ocInfoArr.append(ocInfo)
    print("projectNum = %d" % ocInfoArr.__len__())
    process_contract_info(ocInfoArr)

    # for ocInfo in ocInfoArr:
    #     print(ocInfo.contract_nos)
    return ocInfoArr

    # # 将对象列表转换为字典列表
    # data_dict = [item.to_dict() for item in ocInfoArr]
    #
    # # 使用 JSON 序列化器将字典列表转换为 JSON 字符串
    # json_str = json.dumps(data_dict)
    #
    # print(json_str)


# 写excel
def save_process_info_to_excle(oc_info_arr):
    if not oc_info_arr:
        print("save_process_info_to_excle.oc_info_arr is null")
        return
    # 创建一个新的工作簿
    workbook = xlwt.Workbook(encoding='utf-8')

    # 创建一个工作表
    sheet = workbook.add_sheet('Sheet1')

    # 标题行
    row0 = ["二赛道项目id", "大部", "项目来源", "主体类型", "新房楼盘名称", "新房楼盘id", "合作模式", "合同编号"]
    # 写第一行
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    j=1
    for info in oc_info_arr:
        # 数据行
        sheet.write(j, 0, info.home_project_id)
        sheet.write(j, 1, info.project_big_area)
        sheet.write(j, 2, info.project_source)
        sheet.write(j, 3, info.subject_type)
        sheet.write(j, 4, info.dev_name)
        sheet.write(j, 5, info.dev_id)
        sheet.write(j, 6, info.cooperate_model)
        if info.contract_nos:
            sheet.write(j, 7, ",".join(info.contract_nos))
        j = j+1
    # 保存工作簿
    workbook.save('/Users/xugao/Downloads/项目合同映射表.xls')


OrderContractInfoDataArr = get_home_order_info_from_excle()
save_process_info_to_excle(OrderContractInfoDataArr)


# response = get_home_order_info_from_excle("1620055180617849", url)

# http://newh-contract.nhservice.ke.com/home/decoration/contract/list?type=25&form_type=1,3,4,11&approval_status=1,2,3,4,5,6,7,8,9&resblock_id="1620055180617849"
