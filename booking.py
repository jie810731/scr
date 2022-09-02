from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from urllib import response
import requests
import threading
from datetime import datetime,timedelta
import pause
import pytz
import pytesseract
from PIL import Image
import re
import os

mapping = {
        1:{
            6:[8,10],
            7:[8,10],
            8:[1,2,3,4,5,7,8,9,10],
            9:[1,2,3,4,5,7,8,9,10],
            10:[5,7,8,9,10],
            11:[5,7,8,9,10],
            12:[8,10],
            13:[8,10],
            14:[7,8,9,10],
            15:[7,8,9,10],
            16:[7,8,9,10],
            17:[7,8,9,10],
            18:[8,10],
            19:[8,10],
            20:[8,10],
            21:[8,10],
        },
        2:{
            6:[8,10],
            7:[8,10],
            8:[1,2,3,4,5,7,8,9,10],
            9:[1,2,3,4,5,7,8,9,10],
            10:[1,2,3,4,7,8,9,10],
            11:[1,2,3,4,7,8,9,10],
            12:[1,2,3,4,7,8,9,10],
            13:[1,2,3,4,7,8,9,10],
            14:[1,2,3,4,5,7,8,9,10],
            15:[1,2,3,4,5,7,8,9,10],
            16:[1,2,3,4,5,6,7,8,9,10],
            17:[1,2,3,4,5,6,7,8,9,10],
            18:[1,2,3,4,8,10],
            19:[1,2,3,4,8,10],
            20:[1,2,3,4,8,10],
            21:[1,2,3,4,8,10],
        },
        3:{
            6:[8,10],
            7:[8,10],
            8:[1,2,3,4,5,7,8,9,10],
            9:[1,2,3,4,5,7,8,9,10],
            10:[5,7,8,9,10],
            11:[5,7,8,9,10],
            12:[8,10],
            13:[8,10],
            14:[1,2,3,4,7,8,9,10],
            15:[1,2,3,4,7,8,9,10],
            16:[1,2,3,4,7,8,9,10],
            17:[1,2,3,4,7,8,9,10],
            18:[8,10],
            19:[8,10],
            20:[8,10],
            21:[8,10],
        },
        4:{
            6:[8,10],
            7:[8,10],
            8:[1,2,3,4,5,7,8,9,10],
            9:[1,2,3,4,5,7,8,9,10],
            10:[1,2,3,4,7,8,9,10],
            11:[1,2,3,4,7,8,9,10],
            12:[1,2,3,4,7,8,9,10],
            13:[1,2,3,4,7,8,9,10],
            14:[1,2,3,4,5,7,9,10],
            15:[1,2,3,4,5,7,9,10],
            16:[1,2,3,4,5,6,7,8,9,10],
            17:[1,2,3,4,5,6,7,8,9,10],
            18:[1,2,3,4,8,10],
            19:[1,2,3,4,8,10],
            20:[1,2,3,4,8,10],
            21:[1,2,3,4,8,10],
        },
        5:{
            6:[8,10],
            7:[8,10],
            8:[1,2,3,4,5,7,8,9,10],
            9:[1,2,3,4,5,7,8,9,10],
            10:[1,2,3,4,7,8,9,10],
            11:[1,2,3,4,7,8,9,10],
            12:[1,2,3,4,7,8,9,10],
            13:[1,2,3,4,7,8,9,10],
            14:[1,2,3,4,5,7,9,10],
            15:[1,2,3,4,5,7,9,10],
            16:[1,2,3,4,8,10],
            17:[1,2,3,4,8,10],
            18:[1,2,3,4,8,10],
            19:[1,2,3,4,8,10],
            20:[1,2,3,4,8,10],
            21:[1,2,3,4,8,10],
        },
    }
def web_driver_init(): 
    options = Options()

    options.add_argument('--headless')
    options.add_argument("window-size=1440,1900")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('–incognito')


    web_driver = webdriver.Chrome(options=options)

    return web_driver

def wait(book_date):
    book_date_in_date_time = datetime.strptime(book_date, "%Y-%m-%d")
    
    start_book_date = book_date_in_date_time - timedelta(days=14)
    start_book_time = start_book_date.replace(hour=23,minute=59,second=50)
    tw_zone = pytz.timezone('Asia/Taipei')

    tw_start_book_time = tw_zone.localize(start_book_time)
    print(f"can start book time = {tw_start_book_time}")
    pause.until(tw_start_book_time)
    print(f"start process time in utc = {datetime.now()}")

def book(date,time,cout,cookie):
    my_cookies = {'ASP.NET_SessionId': cookie}
    request = requests.get('https://scr.cyc.org.tw/tp03.aspx?module=net_booking&files=booking_place&StepFlag=25&QPid={}&QTime={}&PT=1&D={}'.format(cout,time,date),cookies=my_cookies)

def captchImageResponse():
    request = requests.get('https://scr.cyc.org.tw/NewCaptcha.aspx')

    return request
   

def loginCookie(request):
    return request.cookies['ASP.NET_SessionId']

def getLoginCatchImageCode(captch_request):
    open('img.png', 'wb').write(captch_request.content)
    img = Image.open(r"img.png")

    # Adding custom options
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    image_string = pytesseract.image_to_string(img, config=custom_config)

    regx_catch_string = re.findall("\d+", image_string)

    if not regx_catch_string:
        return None

    catch_string = regx_catch_string[0]

    if len(catch_string) < 5:
        return None
    
    return catch_string

def login(id,password,captcha_text,cookie):
    my_data = {
        'loginid':id,
        'loginpw':password,
        'Captcha_text':captcha_text
    }
    cookies = {'ASP.NET_SessionId': cookie}
    r = requests.post('https://scr.cyc.org.tw/tp03.aspx?Module=login_page&files=login', data = my_data ,cookies=cookies)

def isCanBook(cookie,book_date):
    cookies = {'ASP.NET_SessionId': cookie}
    book_date = book_date.replace("-", "/")
    url = 'https://scr.cyc.org.tw/tp03.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D={}&D2=1'.format(book_date)

    r = requests.get(url,cookies=cookies)
    
    if r.history:
        return False
    else:
        return True

def getCourtCode(court_number):
    court_mapping = {
        '1':'1085',
        '2':'1086',
        '3':'1087',
        '4':'1088',
        '5':'1089',
        '6':'1090',
        '7':'1091',
        '8':'1092',
        '9':'1093',
        '10':'1094'
    }

    return court_mapping[court_number]

# def canBookTime(day,time):
#     date = mapping[day]
  
#     return mapping

if __name__ == '__main__':
    book_date = os.environ['BOOK_DATE']
    book_time = os.environ['BOOK_TIME']
    court_number = os.environ['COURT_NUMBER']
    id = os.environ['ID']
    password = os.environ['PASSWORD']

    book_times = book_time.split(',')
    court_code = getCourtCode(court_number)

    wait(book_date)

    captcha_text = None 
    while not captcha_text:
        captch_request = captchImageResponse()
        captcha_text = getLoginCatchImageCode(captch_request)
        print('captcha txt = {}'.format(captcha_text))

    cookie = loginCookie(captch_request)
    
    login(id,password,captcha_text,cookie)

    is_can_book = False
    print('start check can book')
    while not is_can_book:
        is_can_book = isCanBook(cookie,book_date)
    print('end check can book')
    for time in book_times:
        print('booking time = {}'.format(datetime.now()))
        threading.Thread(target = book, args = (book_date,time,court_code,cookie,)).start()
    







    # try:
    #     web_driver = web_driver_init()

    #     web_driver.get("https://scr.cyc.org.tw/tp03.aspx?Module=ind&files=ind")
            
    #     web_driver.add_cookie({'name':'ASP.NET_SessionId', 'value':'avkpg205przxjlihfilfwy5m'})
    #     web_driver.save_screenshot("ss.png")

    #     web_driver.get("https://scr.cyc.org.tw/tp03.aspx?module=net_booking&files=booking_place&PT=1")

    #     web_driver.get("https://scr.cyc.org.tw/tp03.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2022/04/04&D2=1")

    #     web_driver.execute_script("Step3Action(1093,6)")
        
    #     web_driver.save_screenshot("ss.png")
    # except Exception as e:
    #     print('c')
    #     print(e)

    # for request in web_driver.requests:  
    #     if request.response:  
    #         print(  
    #             request.url, 
    #             request.headers,
    #         )  

