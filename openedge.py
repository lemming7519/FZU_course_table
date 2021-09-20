import getpass
number = input("请输入你的学号：")
key = getpass.getpass("请输入你的密码：")

from selenium import webdriver
wd = webdriver.Chrome()

wd.get('https://jwch.fzu.edu.cn/html/login/1.html')

inuttext = wd.find_element_by_class_name('inut-text')
inutpassword = wd.find_element_by_class_name('input-password')

inuttext.send_keys(number)
inutpassword.send_keys(key)

from time import sleep
sleep(3) #等网站加载完毕

vercode=input('请输入验证码：') 
inputyzm = wd.find_element_by_class_name('input-yzm')
inputyzm.send_keys(vercode)

loginbtn = wd.find_element_by_class_name('btn')
loginbtn.click()

from selenium import webdriver
from time import sleep

sleep(5)

url= wd.current_url
print(url)
import re
result = re.findall(".*id=(.*)&host.*", url)
if(result == ''):
    print('登录出现错误，请重试！')
idd=''
for x in result:
    idd = idd + x
newurl = 'https://jwcjwxt2.fzu.edu.cn:81/student/xkjg/wdkb/kb_xs.aspx?id=' + idd
wd.get(newurl)
sleep(1)

html = wd.page_source
td = wd.find_elements_by_tag_name('td')
lessoninfo = []
for y in td:
    lessoninfo.append(y.text)
wd.quit()

del lessoninfo[15]
del lessoninfo[47]
del lessoninfo[79]
i = 15
err1 = list(range(15,102,8))
lessonsum=[]

def findname(num):
    fenge = re.split('\n',lessoninfo[num])
    name = fenge[0]
    name = name.replace('＃','')
    name = name.replace('*','')
    name = name.replace('△','')
    name = name.replace('★','')
    return name
    
def findteacher(num):
    fenge = re.split('\n',lessoninfo[num])
    teacher= fenge[3]
    return teacher

def findloca(num):
    fenge = re.split('\n',lessoninfo[num])
    location= fenge[2]
    location = location.replace('[','')
    location = location.replace(']','')
    location = location.replace(' ','')
    location = location.replace('旗山','')
    return location

def findweeks(num):
    fenge = re.split('\n',lessoninfo[num])
    weekstart= fenge[4]
    weekstart = weekstart[0:2]
    return weekstart

def findweeke(num):
    fenge = re.split('\n',lessoninfo[num])
    weekend= fenge[4]
    weekend = weekend[3:5]
    return weekend


import time

calen = input('给你的课表起个名字吧：')
calen = 'BEGIN:VCALENDAR\nVERSION:2.0\nX-WR-CALNAME:' + calen + '\nPRODID:FZU\nCALSCALE:GREGORIAN\nMETHOD:REQUEST\n\n'
timebegin = input('输入开学日（第一周周一），例如20210830：') + '000000'
#转换成时间数组
timeArray = time.strptime(timebegin, "%Y%m%d%H%M%S")
#转换成时间戳
timestamp = time.mktime(timeArray)

for i in range(15,102,1):
    if i in err1:
        continue
    else:
        if(lessoninfo[i] == ''):
            continue
        else:
            name = findname(i)
            teacher = findteacher(i)
            location = findloca(i)
            day = (i-15) % 8
            weekstart = int(findweeks(i))
            weekover = int(findweeke(i))
            routin = 1
            if(location.find('单') != -1):
                location = location.replace('单','')
                routin = 2
            if(location.find('双') != -1):
                location = location.replace('双','')
                routin = 2
            lessonstart = (i-15) // 8 + 1
            lessonover = lessonstart -1
            for j in range(i,102,8):
                if(name == findname(j)):
                    lessoninfo[j]=''
                    lessonover = lessonover + 1
                else:
                    break

            timestart = ((day-1) + (weekstart-1) * 7) * 86400 + timestamp
            time_local = time.localtime(timestart)
            realtimestart = time.strftime("%Y%m%d",time_local)

            if(lessonstart == 1): realclassstart = '002000Z\nDTEND:'
            elif(lessonstart == 2): realclassstart = '011500Z\nDTEND:'
            elif(lessonstart == 3): realclassstart = '022000Z\nDTEND:'
            elif(lessonstart == 4): realclassstart = '031500Z\nDTEND:'
            elif(lessonstart == 5): realclassstart = '060000Z\nDTEND:'
            elif(lessonstart == 6): realclassstart = '065500Z\nDTEND:'
            elif(lessonstart == 7): realclassstart = '075000Z\nDTEND:'
            elif(lessonstart == 8): realclassstart = '084500Z\nDTEND:'
            elif(lessonstart == 9): realclassstart = '110000Z\nDTEND:'
            elif(lessonstart == 10): realclassstart = '115500Z\nDTEND:'
            elif(lessonstart == 11): realclassstart = '125000Z\nDTEND:'

            if(lessonover == 1): realclassover = '010500Z'
            elif(lessonover == 2): realclassover = '020000Z'
            elif(lessonover == 3): realclassover = '030500Z'
            elif(lessonover == 4): realclassover = '040000Z'
            elif(lessonover == 5): realclassover = '064500Z'
            elif(lessonover == 6): realclassover = '074000Z'
            elif(lessonover == 7): realclassover = '083500Z'
            elif(lessonover == 8): realclassover = '093000Z'
            elif(lessonover == 9): realclassover = '114500Z'
            elif(lessonover == 10): realclassover = '124000Z'
            elif(lessonover == 11): realclassover = '133500Z'

            if(day == 1): byday = 'MO'
            elif(day == 2): byday = 'TU'
            elif(day == 3): byday = 'WE'        
            elif(day == 4): byday = 'TH'     
            elif(day == 5): byday = 'FR'     
            elif(day == 6): byday = 'SA'     
            elif(day == 7): byday = 'SU'

            times = weekover - weekstart +1

            calen = calen + 'BEGIN:VEVENT\nORGANIZER:' + teacher + '\nLOCATION:' + location + '\nDTSTART:' + str(realtimestart) + 'T' + str(realclassstart) + str(realtimestart) + 'T' + str(realclassover) + '\nRRULE:FREQ=WEEKLY;INTERVAL=' + str(routin) + ';BYDAY=' + byday +';COUNT=' + str(times) + '\nSUMMARY:' + name + '\nDESCRIPTION:' + teacher + '\nEND:VEVENT\n\n'
            
calen = calen + '\nEND:VCALENDAR'

with open('课表utf-8.ics', 'w', encoding='utf-8') as f:
    f.write(calen)


print('成功！')