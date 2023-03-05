from .the_modules import *

def get_cookies():
    cookie_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'}
    err_num = 0
    while err_num < 3:
        try:
            cookie = requests.utils.dict_from_cookiejar(requests.get('https://beian.miit.gov.cn/', headers=cookie_headers).cookies)['__jsluid_s']
            return cookie
        except:
            print("icpchecker() error/n",end='')
            err_num += 1
            time.sleep(3)
    return -1


def get_token():
    timeStamp = round(time.time()*1000)
    authSecret = 'testtest' + str(timeStamp)
    authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
    auth_data = {'authKey': authKey, 'timeStamp': timeStamp}
    url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
    try:
        t_response = requests.post(url=url, data=auth_data, headers=base_header).json()
        token = t_response['params']['bussiness']
    except:
        return -1
    return token


def get_check_pic(token):
    url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
    base_header['Accept'] = 'application/json, text/plain, */*'
    base_header.update({'Content-Length': '0', 'token': token})
    try:
        p_request = requests.post(url=url, data='', headers=base_header).json()
        p_uuid = p_request['params']['uuid']
        big_image = p_request['params']['bigImage']
        small_image = p_request['params']['smallImage']
    except:
        return -1
    # 解码图片，写入并计算图片缺口位置
    with open('bigImage.jpg', 'wb') as f:
        f.write(base64.b64decode(big_image))
    with open('smallImage.jpg', 'wb') as f:
        f.write(base64.b64decode(small_image))
    background_image = cv2.imread('bigImage.jpg', cv2.COLOR_GRAY2RGB)
    fill_image = cv2.imread('smallImage.jpg', cv2.COLOR_GRAY2RGB)
    position_match = cv2.matchTemplate(background_image, fill_image, cv2.TM_CCOEFF_NORMED)
    max_loc = cv2.minMaxLoc(position_match)[3][0]
    mouse_length = max_loc+1
    os.remove('bigImage.jpg')
    os.remove('smallImage.jpg')
    check_data = {'key': p_uuid, 'value': mouse_length}
    return check_data


def get_sign(check_data, token):
    check_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'
    base_header.update({'Content-Length': '60', 'token': token, 'Content-Type': 'application/json'})
    try:
        pic_sign = requests.post(check_url, json=check_data, headers=base_header).json()
        sign = pic_sign['params']
    except:
        return -1
    return sign

# 解析网页，提取信息
def get_beian_info(info_data, p_uuid, token, sign):
    domain_list = []
    info_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
    base_header.update({'Content-Length': '78', 'uuid': p_uuid, 'token': token, 'sign': sign})
    try:
        beian_info = requests.post(url=info_url, json=info_data, headers=base_header).json()
        domain_total = beian_info['params']['total']
        page_total = beian_info['params']['lastPage']
        end_row = beian_info['params']['endRow']
        info = info_data['unitName']
        for i in range(0, page_total):
            for k in range(0, end_row+1):
                info_base = beian_info['params']['list'][k]
                domain_name = info_base['domain']
                domain_type = info_base['natureName']
                domain_licence = info_base['mainLicence']
                website_licence = info_base['serviceLicence']
                domain_status = info_base['limitAccess']
                domain_approve_date = info_base['updateRecordTime']
                domain_owner = info_base['unitName']
                try:
                    domain_content_approved = info_base['contentTypeName']
                    if domain_content_approved == "":
                        domain_content_approved = "无"
                except KeyError:
                    domain_content_approved = "无"
                row_data = {
                    "domain_owner":domain_owner,
                    "domain_name":domain_name,
                    "domain_licence":domain_licence,
                    "website_licence":website_licence,
                    "domain_type":domain_type,
                    "domain_content_approved":domain_content_approved,
                    "domain_status":domain_status,
                    "domain_approve_date":domain_approve_date
                    }
                domain_list.append(row_data)
            info_data = {'pageNum': i+2, 'pageSize': '40', 'unitName': info}
            if beian_info['params']['isLastPage'] is True:
                break
            else:
                beian_info = requests.post(info_url, json=info_data, headers=base_header).json()
                end_row = beian_info['params']['endRow']
                time.sleep(3)
    except:
        return domain_list
    return domain_list

# icp备案查询
def icp_checker(info):
    cookie = get_cookies()
    info = {'pageNum': '1', 'pageSize': '100', 'unitName': info}
    try:
        global base_header
        base_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
            'Origin': 'https://beian.miit.gov.cn',
            'Referer': 'https://beian.miit.gov.cn/',
            'Cookie': f'__jsluid_s={cookie}'
        }
        # -1代表对应步骤失败了，不是-1则正常执行下一步
        token = get_token()
        check_data = get_check_pic(token)
        sign = get_sign(check_data, token)
        p_uuid = check_data['key']
        domain_list = get_beian_info(info, p_uuid, token, sign)
        return domain_list
    except BaseException:
        print("icp checker {}\n".format(info),end="")
        return []