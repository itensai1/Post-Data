import requests # to request Pages
from bs4 import BeautifulSoup # to manipulate data 


link= input('Contest link : ')
Data = {}
statusLink = link+"/status/page/{}?order=BY_ARRIVED_ASC"
problemLink = link+"/status/{}?order=BY_ARRIVED_ASC"
standingLink = link+"/standings/groupmates/true"
num_pages = 1
num_problems = 1

def contest_info(page):
    try:
        contest = requests.get(page.format(1))
    except:
        Data.update({"Error":"invalid link"})
        return False
    src = contest.content
    soup = BeautifulSoup(src,'lxml')
    global num_pages,num_problems
    num_pages = int(soup.find_all("span" , {"class":"page-index"})[-1].text)
    num_problems = len(soup.find("select", {"name":"frameProblemIndex",}).find_all("option"))-1
    return True
 
def get_first_ACC(page):
    for p in range(1,num_pages+1):
        status = requests.get(page.format(p))
        src = status.content
        soup = BeautifulSoup(src,'lxml')
        table = soup.find("div" , {"class":"datatable"}).find("table" , {"class" : "status-frame-datatable"}).find_all("tr")
        i = 1
        while i in range(len(table)) :
            if table[i].find_all("td")[5].find("span",{"class":"verdict-accepted"}) :
                handle = table[i].find_all("td")[2].find("a").text
                Data.setdefault("First Accepted",handle)
                return   
            i+=1

def get_problems(page):
    for i in range(num_problems):
        status = requests.get(page.format(chr(ord('A')+i)))
        src = status.content
        soup = BeautifulSoup(src,'lxml')
        table = soup.find("div" , {"class":"datatable"}).find("table" , {"class" : "status-frame-datatable"}).find_all("tr")
        if table[1].find("span",{"class":"verdict-accepted"}) :
            handle = table[1].find_all("td")[2].find("a").text
            problem = table[1].find_all("td")[3].find("a").text.strip()[0]
            Data.setdefault(problem,handle)

def check_if_official(s_link):
    standings = requests.get(s_link)
    src = standings.content
    soup = BeautifulSoup(src,'lxml')
    Row = soup.find("tr",{"class":"standingsStatisticsRow"}).find_all("span" ,{"class":"cell-passed-system-test cell-accepted"})
    for cell in range(len(Row)):
        if Row[cell].text=="0" and Data.get(chr(ord('A')+cell-1)):
            Data.pop(chr(ord('A')+cell-1))


if contest_info(statusLink):
    get_first_ACC(statusLink)
    get_problems(problemLink)
    check_if_official(standingLink)
    print()

for x, y in Data.items():
    print(x," : ",y)
else:
    print("\n>>>> Done :) <<<<")
