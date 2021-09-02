import requests, json
import time
import csv
from bs4 import BeautifulSoup

url         = "https://xenforourl.com/index.php" #Url do forum.
user        = "" #Nome de usuário para login.
password    = "" #Senha para login.

def SendMessageTest(session, token):
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept" : "text/plain"            
    }    
    data =  {
        "recipients" : "",  #Nome de quem vai receber.
        "title" : "", #Titulo da mensagem
        "message_html" : "", #Mensagem
        "_xfRelativeResolver" : url + "?conversations/add",
        "_xfToken" : token,
        "_xfRequestUri" : "/index.php?conversations/add",
        "_xfNoRedirect" : "1",
        "_xfToken" : token,
        "_xfResponseType" : "json"
    }    
    response_json = requests.post(url + "?conversations/insert", data=data, headers=header, cookies=session).json()

    if "_redirectStatus" in response_json :
        if response_json["_redirectStatus"] == "ok" :
            print("Mensagem enviada com sucesso para: ", data["recipients"])                

    if "error" in response_json :
        print(response_json["error"])

def GetXfSession():
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept" : "text/plain"
    }
    return requests.get(url + "?login", headers=header).cookies["xf_session"]

def GetXfToken(session):
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  
        "Accept-Encoding": "identity, deflate, compress, gzip",
        "Accept-Language" : "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3" 
    }   
    response = requests.get(url, headers=header, cookies=session)
    soup = BeautifulSoup(response.text, "lxml")
    try:
        return soup.find("input", {"name": "_xfToken"}).get("value")        
    except Exception as e:
        print("Falha ao obter token: %s" % str(e))

def AuthUser(user, password):
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Content-type": "application/x-www-form-urlencoded",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language" : "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3"                  
    }
    data = {
        "remember" : "1",
        "register" : "0",
        "redirect" : url,
        "password" : password,
        "login" : user,
        "cookie_check" : "1",
        "_xfToken" : ""
    }
    cookies = {
        "xf_session" : GetXfSession()
    }
    return requests.post(url + "?login/login", data=data, cookies=cookies, headers=header).cookies

session = AuthUser(user, password)
token = GetXfToken(session)
SendMessageTest(session, token)
