import requests
import re
import sys
import os
import json
import random
import calhelper
from datetime import timedelta
from datetime import datetime

class ScoreInfo:
    def __init__(self):
        self.name = ''
        self.id = ''
        self.cla = ''
        self.points = ''
        self.gpa = ''
        self.scores = ''
        self.des = ''

class ScoreDescrip:
    def __init__(self):
        self.semester = ''
        self.scoredata = list()



# 获取学生成绩单信息
def GetStudentScore(session_value,srvid_value):
    print("正在获取重定向地址...")
    
    cookie_info = 'SESSION=' + session_value + '; SRVID=' + srvid_value

    myheaders = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }
    resp = requests.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/grade/sheet',headers=myheaders,allow_redirects=False)

    print(resp.headers)

    print("已经获取到信息，正在请求成绩。")

    request_url = resp.headers['Location']
    print(request_url)

    infomation = request_url.split('/')
    student_scoreid = infomation[6]
    print(student_scoreid)

    score_requesturl = 'http://jxglstu.hfut.edu.cn/eams5-student/for-std/grade/sheet/info/'+student_scoreid+'?semester='

    request_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Referer':'http://jxglstu.hfut.edu.cn'+request_url,
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }

    respond_data = requests.get(score_requesturl,headers=request_headers,params='semester:')
    
    my_text = respond_data.text

    result = re.findall(r'<div class="row">(.*?)</tbody>',my_text,re.S|re.M)
    
    result_list = list()

    for items in result:
        data_info = ScoreDescrip()
        semester = re.findall(r'<h3>(.*?)</h3>',items,re.S|re.M)
        #print(semester)
        data_info.semester = semester[0]
        scores = re.findall(r'<td>(.*?)</td>',items,re.S|re.M)
        #print(scores)
        count = 0
        while(count<len(scores)):
            temp_scoredata = ScoreInfo()
            temp_scoredata.name = scores[count]
            temp_scoredata.id = scores[count+1]
            temp_scoredata.cla = scores[count+2]
            temp_scoredata.points = scores[count+3]
            temp_scoredata.gpa = scores[count+4]
            temp_scoredata.scores = scores[count+5]
            temp_scoredata.des = scores[count+6]
            temp_scoredata.des = temp_scoredata.des.replace('<br />',' ')
            data_info.scoredata.append(temp_scoredata)
            count = count + 7
        
        result_list.append(data_info)

    storage_data = list()

    for items in result_list:

        dic_2 = {}
        dic_2['semester'] = items.semester
        scores_list = list()
        
        for datas in items.scoredata:
            dic_3 = {}    
            dic_3['name'] = datas.name
            dic_3['id'] = datas.id
            dic_3['cla'] = datas.cla
            dic_3['points'] = datas.points
            dic_3['gpa'] = datas.gpa
            dic_3['scores'] = datas.scores
            dic_3['des'] = datas.des
            scores_list.append(dic_3)
            
        dic_2['values'] = scores_list
        
        storage_data.append(dic_2)
    
    print(storage_data)

    result_text = json.dumps(storage_data,ensure_ascii=False)


    fo = open('scoredata.json','w',encoding='utf-8')
    fo.write(result_text)

    fo.close()
    print("成绩信息已归档于 scoredata.json 中。")

    return result_text

# 获取学生考试信息
def GetStudentExams(session_value,srvid_value):
    print("正在获取重定向地址...")
    
    cookie_info = 'SESSION=' + session_value + '; SRVID=' + srvid_value

    myheaders = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }
    resp = requests.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/exam-arrange',headers=myheaders,allow_redirects=False)

    print(resp.headers)

    print("已经获取到信息，正在请求考试信息。")

    request_url = resp.headers['Location']
    print(request_url)

    infomation = request_url.split('/')
    student_scoreid = infomation[5]
    print(student_scoreid)

    score_requesturl = 'http://jxglstu.hfut.edu.cn/eams5-student/for-std/exam-arrange/info/'+student_scoreid+'?semester='

    request_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Referer':'http://jxglstu.hfut.edu.cn'+request_url,
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }

    respond_data = requests.get(score_requesturl,headers=request_headers)
    
    my_text = respond_data.text


    result = re.findall(r'<td>(.*?)</td>',my_text,re.S)
    time_result = re.findall(r'<td class="time">(.*?)</td>',my_text,re.S)
    print(result)

    for items in result:
        items = items.replace('<br />',' ')
        

    back_result = list()

    i=0

    while(i<len(time_result)):
        datas = {}
        datas['subject'] = result[i*4]
        datas['time'] = time_result[i]
        datas['location'] = result[i*4+1]

        back_result.append(datas)        
        
        i=i+1

    writestring = "BEGIN:VCALENDAR\n"
    writestring += "PRODID:-//Apple Inc.//Mac OS X 10.15.7//EN\n"
    writestring += "VERSION:2.0\n"
    writestring += "CALSCALE:GREGORIAN\n"
    writestring += "METHOD:PUBLISH\n"
    writestring += "X-WR-CALNAME:HFUTPlus 考试安排\n"
    writestring += "X-WR-TIMEZONE:null\n"
    for i in back_result:
        writestring += "BEGIN:VEVENT\n"
        writestring += "SUMMARY:"+i['subject']+" 考试\n"
        # writestring += "ORGANIZER;CN=TRIStudio:mailto:tri.studio@outlook.com\n"
        timezone = i['time'].split(' ')
        datestring = timezone[0].replace('-','')
        timestr = timezone[1].replace(':','')
        betimestr = timestr.split('~')
        writestring += "DTSTART;TZID=Asia/Shanghai:"+datestring+'T'+betimestr[0]+"00\n" 
        writestring += "DTEND;TZID=Asia/Shanghai:"+datestring+'T'+betimestr[1]+"00\n"
        writestring += "UID:"+str(random.randint(0,99999))+"\n"
        writestring += "SEQUENCE:0\n"
        writestring += "DESCRIPTION:\n"
        writestring += "LOCATION:"+i['location']+"\n"
        writestring += "STATUS:CONFIRMED\n"
        writestring += "END:VEVENT\n"

    writestring += "END:VCALENDAR"

    fo = open("Exams.ics","w")
    fo.write(writestring)
    fo.close()   

    print(back_result)

    result_text = json.dumps(back_result,ensure_ascii=False)


    fo = open('examdata.json','w',encoding='utf-8')
    fo.write(result_text)

    fo.close()
    print("考试日程已经输出至 Exams.ics")
    print("考试信息已归档于 examdata.json 中。")

    return result_text

# 获取学生课表信息
def GetStudentClasses(session_value,srvid_value):

    print("正在获取重定向地址...")
    
    cookie_info = 'SESSION=' + session_value + '; SRVID=' + srvid_value

    myheaders = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }
    resp = requests.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-table/',headers=myheaders,allow_redirects=False)

    print(resp.headers)

    print("已经获取到信息，正在请求课表信息。")

    request_url = resp.headers['Location']
    print(request_url)

    infomation = request_url.split('/')
    student_scoreid = infomation[5]
    print(student_scoreid)



    print("正在获取学期信息....")

    semesterheaders = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-CN;q=0.5',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }
    resp = requests.get('http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-table/info/'+student_scoreid,headers=semesterheaders)

    semester_str = resp.text
    semester_result = re.findall(r'<select class="form-control selectize" name="allSemesters" id="allSemesters">(.*?)</select>',semester_str,re.S)

    semester_repo = semester_result[0].split('\n')


    semesterdic = {}
    print("[!] 请选择要打印课表的学期代号：")
    for items in semester_repo:

        
        if(len(items.strip())==0):   
            continue
        semidlist = re.findall(r'"(.*?)"',items,re.S)
        sid = semidlist[0]
        if(len(semidlist)!=1):
            sid = semidlist[1]
        
        snamelist =  re.findall(r'>(.*?)<',items,re.S)
        sname = snamelist[0]

        semesterdic[sid] = sname
        print(sid+":"+sname)        


    
    insm = input()
    smid = insm



    score_requesturl = 'http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-table/semester/'+smid+'/print-data/'+student_scoreid

    request_headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Referer':'http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-table/semester'+smid+'print/'+student_scoreid+'?',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }

    respond_data = requests.get(score_requesturl,headers=request_headers)
    
    print(respond_data)
    json_data = respond_data.json()
    print(json_data)            # json_data 为请求到的课表信息

    date_requesturl = 'http://jxglstu.hfut.edu.cn/eams5-student/ws/semester/get/'+smid

    date_headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-CN;q=0.5',
        'Connection':'keep-alive',
        'Cookie':cookie_info,
        'Host':'jxglstu.hfut.edu.cn',
        'Referer':'http://jxglstu.hfut.edu.cn/eams5-student/for-std/course-table/semester/'+smid+'/print/'+student_scoreid+'?',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
    }

    respond_date = requests.get(date_requesturl,headers=date_headers)
    date_json = respond_date.json()
    date_startdate = date_json['startDate']
    
    print(date_startdate)           # date_startdate 为学期的开始时间


    hp = calhelper.CourseHelper()
    hp.SetStartDate(date_startdate)

    print("是否需要偏移日期？若无需则输入 0 即可")

    shift_time_input = input()
    shift_time_data = int(shift_time_input)

    if(shift_time_data!=0):
        hp.ShiftStartDate(shift_time_data)


    jsondata_step1 = json_data['studentTableVm']
    print(jsondata_step1['id'])
    print(jsondata_step1['code'])
    print(jsondata_step1['adminclass'])

    jsondata_step2 = jsondata_step1['activities']

    for items in jsondata_step2:
        hp.InsertStringCourse(items['courseCode'],items['courseName'],items['room'],items['teachers'],items['lessonName'],items['lessonCode'],items['startUnit'],items['endUnit'],items['weekday'],items['weeksStr'])    
    
    hp.PrintCourse()

    print("课表制作完成，通过 Courses.ics 即可导入到各终端")
    
    return hp


# 调用生成单个课表日程
def GenerateCourse():


    return



    
def DeleteStudentInfomation():
    print("[!] 确定要删除信息吗？你将需要重新登录，目录下的个人信息文件也会被移除。")
    print("n:取消 y:确定")
    
    choose = input()

    if(choose=='y'):
        if os.path.exists("cookiedata.archive"):
            os.remove("cookiedata.archive") 
        if os.path.exists("Courses.ics"):
            os.remove("Courses.ics")    
        if os.path.exists("Exams.ics"):
            os.remove("Exams.ics")                
        if os.path.exists("examdata.json"):
            os.remove("examdata.json")   
        if os.path.exists("scoredata.json"):
            os.remove("scoredata.json")   

        print("删除成功，重新启动程序后生效。")
        sys.exit(0)
    else:
        
        return
   