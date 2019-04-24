# encoding = 'utf-8'
from selenium import webdriver
from selenium.common import exceptions
import os
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText

def open_chrome():
    # 1.使用桌面环境，调出Chrome浏览器
    # 设置DISPLAY环境变量，用来显示图形界面，放在crontab里执行，在桌面环境运行
    # os.environ['DISPLAY'] = ':0'
    # 2.使用Chrome-headless 静默模式，在后台运行，方便在服务器运行
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # 使用chrome驱动，并打开网址，option设置静默模式
    browser = webdriver.Chrome(executable_path='/home/langxiaowei/appointment/chromedriver', chrome_options=option)
    browser.get('https://www.jiandaoyun.com/f/5ae88ad4e6772129e072bc15')
    time.sleep(2)  # 停顿2秒，防止网页未加载完，找不到元素报错

    # js method
    # js = '$("input").eq(0).val("17638581226");\
    #         $("input").eq(0).blur();\
    #         $("input").eq(1).click();\
    #         $("a.x-dropdown-item").eq(0).click();\
    #         $("div.foot-btn").eq(0).click();\
    #         $("div.x-msg-toast-wrapper").text()'
    # browser.execute_script(js)

    # self method
    browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/div/ul/li[4]/div[3]/div/input').send_keys("17638581226")
    browser.find_element_by_class_name('fui_trigger-btn').click()
    browser.find_element_by_class_name('x-dropdown-item').click()
    browser.find_element_by_class_name('foot-btn').click()
    try:
        prompt = browser.find_element_by_class_name("x-msg-toast-wrapper").text
    except exceptions.NoSuchElementException:
        prompt = '预约成功'
        
    print(prompt)
    print(time.asctime())

    browser.close()

    return prompt


def sendmail(text):
    # 发件人和收件人
    sender = 'lxwno.1@163.com'
    receiver = 'langxw@efushui.com'

    # 用来发邮件的stmp服务器
    smtp_server = 'smtp.163.com'
    username = 'lxwno.1@163.com'
    password = '123456lxw!'

    # 邮件的主题和正文
    mail_title = '学车预约结果'
    mail_body = text

    # 创建一个实例
    # message是字符串，表示邮件。我们知道邮件一般由标题，发信人，收件人，邮件内容，附件等构成
    message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文,plain格式
    message['From'] = sender                         # 邮件上显示的发件人
    message['To'] = receiver                         # 邮件上显示的收件人
    message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题

    try:
        smtp = smtplib.SMTP()                        # 创建一个链接
        smtp.connect(smtp_server)                    # 链接发送邮件的服务器
        smtp.login(username, password)               # 登录服务器
        smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
        print('Mail send success.')
        smtp.quit()
    except smtplib.SMTPException:
        print('Mail send failed.')


if __name__ == '__main__':
    res = open_chrome()
    sendmail(res)
