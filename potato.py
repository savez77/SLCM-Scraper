import requests,bs4,re,time,os,pprint,json
from selenium import webdriver
from stateval import *


def loginForm(browser):

   
    
    '''res = requests.get(mainUrl + 'studenthomepage.aspx')
    if res.status_code == 200:
        raise Exception('Already logged in')
        soup = bs4.BeautifulSoup(res.text)

        #Get the cookie value
        
        return cookieValue'''
    
    res = requests.get('https://slcm.manipal.edu/')
    if res.status_code == 200:
       
        

        browser.get('https://slcm.manipal.edu/')
        uname = browser.find_element_by_css_selector('#txtUserid')
        uname.send_keys('USERNAME') #CHANGE THIS
        passwd = browser.find_element_by_css_selector('#txtpassword')
        passwd.send_keys('PASSWORD') #CHANGE THIS
        UnsessID = browser.get_cookie('ASP.NET_SessionId')
        sessID = UnsessID['value']
        #print(sessID)
        time.sleep(15)
        cookieValue = {'ASP.NET_SessionId':sessID}
        semValue = {'ctl00$ContentPlaceHolder1$ddlSemester':'I', '__VIEWSTATE':viewStatedata, '__EVENTVALIDATION':eventValdata} #Change sem value dynamically
        #print(semValue)
        #print(cookieValue)
        return cookieValue,semValue
        '''
        
        sendForm = requests.get(mainUrl + 'StudentProfile.aspx', cookies=cookieValue)
        print(sendForm.status_code)
        print(sendForm.text)'''
        
def getCrap(cookieValue,semValue):
    sendForm = requests.post('https://slcm.manipal.edu/GradeSheet.aspx', cookies=cookieValue, data=semValue)
    crap = bs4.BeautifulSoup(sendForm.text, 'html.parser')
    crap2 = crap.select('option', class_='form_control')
    totalSemesters = int(len(crap2)) - 1
    #print("Total Semesters: " + str(totalSemesters))
    crap2 = crap.find_all('tr')
    totalSubjectsinSem = int(len(crap2)) - 1
    #print(totalSemesters)
    #print(totalSubjectsinSem)
    #print(semValue)
    return totalSemesters,totalSubjectsinSem,crap2
  
def checkEx(x):
    y = re.match('^[0-9]?$', x)
    if x == y.group():
         return 'slno'
    y = re.match('.{3} [0-9]{4}', x)
    if x == y.group():
         return 'subcode'
    y = re.match('[a-zA-Z]+', x)
    if x == y.group():
        return 'subname'
    y = re.match('I|II|III|IV|V|VI|VII|VIII', x)
    if x == y.group():
         return 'sem'
    y = re.match('A\+|A|B|C|D|E|F|I', x)
    if x == y.group():
         return 'grade'
    y = re.match('[0-9]\.[0-9]{2}', x)
    if x == y.group():
         return 'credit'
     
         
     
 
           
def scrapeSheet(cookieValue,semValue,totalSemesters,totalSubjectsinSem,crap2):
    semDict = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII'}
    #headDict = {'Sl_No':slno, 'Subject_Code':subcode, 'Subject_Name':subname, 'Semester':sem, 'Grade':grade, 'Credit':credit}
    #baseList = []    
    #for semes in range(1,totalSemesters):
    #    baseList[semes] = {}.append()
    #print(baseList)

        
    for semList in range(1, totalSemesters+1):
        #results = ['Sl_No ']

        print('\n')
        for subject in range(1, totalSubjectsinSem+1):
            for field in range(1, 7):
                x = crap2[subject].contents[field].text.strip()
                x = x + ' ' + checkEx(x)        
                print(x)
                
            print('\n')

        print("=================================================")
        
        semValue["ctl00$ContentPlaceHolder1$ddlSemester"] = semDict[semList+1]       
        totalSemesters,totalSubjectsinSem,crap2 = getCrap(cookieValue,semValue)
        
    print('END OF ENTIRE LOOP') 
         
        
def main():
    
    options = webdriver.FirefoxOptions()
    options.binary_location = r'/usr/lib/firefox/firefox'
    browser = webdriver.Firefox(executable_path=r'/home/savez/Desktop/vscode/SLCMscraper/geckodriver', options = options)
    
    cookieValue,semValue = loginForm(browser)
    sendForm = requests.get('https://slcm.manipal.edu/GradeSheet.aspx', cookies=cookieValue)
    if len(sendForm.text)>50000:
        print("Login Successful!")
        #print(cookieValue)
        #print(semValue)
        browser.close()
    else:
        print("Login unsuccessful!")
        print("Please run the program again")
        browser.close()
        os.exit()
    
    totalSemesters,totalSubjectsinSem,crap2 = getCrap(cookieValue,semValue)
    
    scrapeSheet(cookieValue,semValue,totalSemesters,totalSubjectsinSem,crap2)
    
        
if __name__ == '__main__':
    main()
    
        

        
        
            
