import requests,bs4,re,time,sys 
from selenium import webdriver
from stateval import *


def loginForm(browser):       

    res = requests.get('https://slcm.manipal.edu/', verify=False)   #Makes a GET request to the website   
    if res.status_code == 200:                                      #If OK, inject username & password. 
        
        browser.get('https://slcm.manipal.edu/')
        uname = browser.find_element_by_css_selector('#txtUserid')
        uname.send_keys('USER_REGNO')                               #!CHANGE THIS
        passwd = browser.find_element_by_css_selector('#txtpassword')
        passwd.send_keys('USER_PASSWORD')                           #!CHANGE THIS
      
        sessID = browser.get_cookie('ASP.NET_SessionId')['value']   #Retrieves the SessionID    
        time.sleep(15)
        cookieValue = {'ASP.NET_SessionId':sessID}
        semValue = {'ctl00$ContentPlaceHolder1$ddlSemester':'I', '__VIEWSTATE':viewStatedata, '__EVENTVALIDATION':eventValdata} #Changes semester value dynamically

    return cookieValue,semValue
        
def getResponse(cookieValue,semValue):
    
    sendForm = requests.post('https://slcm.manipal.edu/GradeSheet.aspx', cookies=cookieValue, data=semValue, verify=False)  #POST request to retrieve the Grade Sheet
    soup = bs4.BeautifulSoup(sendForm.text, 'html.parser')  #Parse the response 
    
    selSoup = soup.select('option', class_='form_control')  #Counts total semesters until date
    totalSemesters = int(len(selSoup)) - 1
    print("Total Semesters: " + str(totalSemesters))
    
    selSoup = soup.find_all('tr')   #Counts total subjects in semester
    totalSubjectsinSem = int(len(selSoup)) - 1

    return totalSemesters,totalSubjectsinSem,selSoup
  
def checkEx(x):     #Regular expression matching to retrieve column names
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
             
def scrapeSheet(cookieValue,semValue,totalSemesters,totalSubjectsinSem,selSoup):    #Scrapes individual column data and prints it out
    semDict = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII'}
    #headDict = {'Sl_No':slno, 'Subject_Code':subcode, 'Subject_Name':subname, 'Semester':sem, 'Grade':grade, 'Credit':credit}
    baseList = []    
    for semes in range(1,totalSemesters):
        baseList[semes] = {}.append()
        
    for semList in range(1, totalSemesters+1):
        print('\n')
        for subject in range(1, totalSubjectsinSem+1):
            for field in range(1, 7):
                x = selSoup[subject].contents[field].text.strip()
                x = x + ' ' + checkEx(x)        
                print(x)
            print('\n')
        print("=================================================")
        
        semValue["ctl00$ContentPlaceHolder1$ddlSemester"] = semDict[semList+1]       
        totalSemesters,totalSubjectsinSem,selSoup = getResponse(cookieValue,semValue)        
        
def main():   #Main function
    options = webdriver.FirefoxOptions()
    options.binary_location = r'/usr/lib/firefox/firefox'
    browser = webdriver.Firefox(executable_path=r'/home/savez/Desktop/vscode/SLCMscraper/geckodriver', options = options)
    
    cookieValue,semValue = loginForm(browser)
    sendForm = requests.get('https://slcm.manipal.edu/GradeSheet.aspx', cookies=cookieValue, verify=False)
    
    if len(sendForm.text)>50000:        #Checks if response is valid
        print("Login Successful!")
        browser.close()
    else:
        browser.close()
        sys.exit("Login unsuccessful. Please run the program again!")
    
    totalSemesters,totalSubjectsinSem,selSoup = getResponse(cookieValue,semValue)  #Calls the necessary functions and displays the output
    scrapeSheet(cookieValue,semValue,totalSemesters,totalSubjectsinSem,selSoup)
        
if __name__ == '__main__':
    main()
    
        

        
        
            
