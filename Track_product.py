import sqlite3 
from win10toast import ToastNotifier
import requests
from bs4 import BeautifulSoup as bs
notify = ToastNotifier()
def scpr(ur):
    url=requests.get(ur)
    soup=bs(url.text)
    elements=soup.find("div",class_="_2c7YLP UtUXW0 _6t1WkM _3HqJxg")
    if elements:
        a=elements.find("div",class_="_1YokD2 _2GoDe3")
        if a:
            b=a.find("div",class_="_1YokD2 _3Mn1Gg col-8-12")
            if b:
                c=b.find("div",class_="aMaAEs")
                if c:
                    d=c.find("div",class_="dyC4hf")
                    if d:
                        e=d.find("div",class_="_25b18c")
                        if e:
                            f=e.find("div",class_="_30jeq3 _16Jk6d")
                            print(f.text)
                            return float("".join(f.text[1:].split(",")))

conn=sqlite3.connect("db.sqlite")
cursor=conn.cursor()
cursor.execute("SELECT * FROM price_tracker")
a=cursor.fetchall()
t=True
for i in a:
    b=scpr(i[3])
    if b<i[1]:
        notify.show_toast("Price Tracker"," Price Decreases For "+i[0] +" Current price is "+ str(b))
        t=False
if t:
    notify.show_toast("Price Tracker","NO Change in Price ")


conn.close()
        
