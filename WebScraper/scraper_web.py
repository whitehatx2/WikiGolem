from bottle import Bottle, request, route, run,hook, response
import urllib2
import re
import json
from bs4 import BeautifulSoup

app = Bottle()

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
 
@app.route('/scraper', method=['OPTIONS'])
def scraper_options():
    return {}
    

@app.route('/scraper', method=['GET', 'POST'])
def scraper():
    top10 = []
    data  = json.loads(json.dumps(request.json));
    print data
    for i in data:
        top10.append(data[i])
    print top10                    
    HashMap = {}
    class DictItem:
        def __init__(self, field1, field2):
            self.field1 = str(field1)
            self.field2 = str(field2)
    for i in range(0,9):
        current_page = "".join(["http://en.wikipedia.org/wiki/",top10[i]])
        print current_page
        current_page_req = urllib2.Request(current_page, headers={'User-Agent' : "Magic Browser"}) 
        try:
            current_page_con = urllib2.urlopen(current_page_req)
        except urllib2.HTTPError as e:
            print e.msg
        current_page_html = current_page_con.read()
        soup = BeautifulSoup(current_page_html)
        HashMap[top10[i]] = ''
        for j in range(0,9):
            if i!=j:
                if '_' in top10[j]:
                    search_title = ''.join([' ', top10[j],' '])
                search_title = top10[j].replace('_', ' ')
                if soup.find_all(text=re.compile(search_title, re.IGNORECASE)):
                    HashMap[top10[i]] = "".join([HashMap[top10[i]],top10[j],','])        
    for k in HashMap.keys():
        HashMap[k] = HashMap[k][:-1]
    return json.dumps(HashMap)

@app.route('/bucket', method=['OPTIONS'])
def scraper_options():
    return {}

@app.route('/bucket', method=['GET', 'POST'])
def scraper_bucket():
    #top10pages = {"1": "Facebook", "0": "Bane_(comics)", "3": "Mark_Zuckerberg", "2": "Google", "5": "Steven_Tyler", "4": "Paul_C\u251c\u2310zanne", "6": "Tom_Hardy", "9": "January_20"}
    top10pages = json.loads(json.dumps(request.json));
    doodles = ["martin luther king", "cezzane", "JFK", "Kennedy", "robert burns", "jules verne", "thomas edison", "ernest schakleton", "constantin brancusi", "st david's day", "will eisner", "women's day", "harry houdini", "robert bunsen", "new year's day", "australia day", "valentine's day", "women's day"] 
    disasters = ["shootout", "earthquake", "tsunami", "famine", "flood", "massacre", "gun", "gun control"]
    events = ["tv show", "movie", "performance", "sitcom", "sports", "finals", "awards", "celebrity", "winner", "champion", "revolution", "annual"]
    HashMap = {}
    for page in top10pages.values():
        current_page = "".join(["http://en.wikipedia.org/wiki/",page])
        current_page_req = urllib2.Request(current_page, headers={'User-Agent' : "Magic Browser"}) 
        try:
            current_page_con = urllib2.urlopen(current_page_req)
        except urllib2.HTTPError, e:
            print e.msg
        current_page_html = current_page_con.read()
        soup = BeautifulSoup(current_page_html)
        HashMap[page] = ''
        if (soup.find_all(text=re.compile('(January|Febraury|March) ([0-9][0-9]?,) (2011)'))):
            if soup.find_all(text=re.compile(' died ', re.IGNORECASE)):
                HashMap[page] = ','.join([HashMap[page],"Death"])  
                continue
        for do in doodles:
            if soup.find_all(text=re.compile(do, re.IGNORECASE)):
                HashMap[page] = ','.join([HashMap[page],"Google Doodle"])
                break
        for di in disasters:
            if soup.find_all(text=re.compile(di, re.IGNORECASE)):
                HashMap[page] = ','.join([HashMap[page],"Disasters"])
                break
        for e in events:
            if soup.find_all(text=re.compile(e, re.IGNORECASE)):
                HashMap[page] = ','.join([HashMap[page],"General Events"])
                break
    for k in HashMap.keys():
        HashMap[k] = HashMap[k][1:]
    return json.dumps(HashMap)

run(app,host='174.127.158.164', port=8081, debug=True)
