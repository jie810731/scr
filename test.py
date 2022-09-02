from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking import *

if __name__ == '__main__':
    id = os.environ['ID']
    password = os.environ['PASSWORD']
 
    now = datetime.now(pytz.timezone('Asia/Taipei'))
    # now = datetime.strptime("2020-04-19", "%Y-%m-%d")
    print(now)

    logintime = now.replace(hour=23,minute=59,second=30,microsecond=0)
    print(logintime)

    screen_time = logintime + timedelta(seconds=30)
    print(screen_time)


    fourteen_day = str((screen_time + timedelta(days=13)).day)
    fourteen_day = '{0}'.format(fourteen_day.zfill(2))
    print("https://scr.cyc.org.tw/tp03.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2022/05/{}&D2=3".format(fourteen_day))
 
    pause.until(logintime)

    captcha_text = None 
    while not captcha_text:
        captch_request = captchImageResponse()
        captcha_text = getLoginCatchImageCode(captch_request)
        print('captcha txt = {}'.format(captcha_text))

    cookie = loginCookie(captch_request)

    login(id,password,captcha_text,cookie)
    web_driver = web_driver_init()

    web_driver.get("https://scr.cyc.org.tw/tp03.aspx?Module=ind&files=ind")  
    web_driver.add_cookie({'name':'ASP.NET_SessionId', 'value':cookie})

    pause.until(screen_time)

    web_driver.get("https://scr.cyc.org.tw/tp03.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2022/05/{}&D2=3".format(fourteen_day))
    web_driver.save_screenshot("{}.png".format(fourteen_day))