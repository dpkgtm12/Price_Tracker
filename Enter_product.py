from tkinter import *
import sqlite3
from tkinter import messagebox
from turtle import back, bgcolor
import requests
from bs4 import BeautifulSoup as bs
from PIL import ImageTk,ImageFilter,Image
conn=sqlite3.connect("db.sqlite")
cursor=conn.cursor()
def show_product(name,img_url,price,pname,purl):
    global win2
    win2=Toplevel()
    win2.title("Check Data")
    win2.config(bg="black")
    win2.geometry("1250x750")
    try:
        with open("rcm.png","wb") as f:
            f.write(requests.get(img_url).content)
        img=Image.open("rcm.png")
        img=img.resize((400,500))
        img=ImageTk.PhotoImage(img)
        lw2=Label(win2,image=img)
        lw2.place(x=50,y=50) 
    except:
        pass
    lw1=Label(win2,text="Product: " +name,font=("Forte",40))
    lw3=Label(win2,text=pname,font=("Algerian",20),wraplength=600,bg="white")
    lw4=Label(win2,text="Price = "+str(price),font=("Algerian",25))
    b2=Button(win2,text="ok",font=("Forte",20),command=lambda:save_data(name,purl,pname,price),activebackground="Yellow",width=20,bg="red")
    b2.place(x=600,y=480)
    lw1.place(x=600,y=50) 
    lw3.place(x=500,y=150) 
    lw4.place(x=630,y=350) 
    win2.mainloop()

def save_data(name,url,p_name,price):
    global win2
    cursor.execute("""create table if not exists price_tracker
    (name varchar(100),
    price float,
    pro_name text,
    url text unique
    )
    """)
    cursor.execute("insert into price_tracker (name , url ,pro_name, price) values(?, ?,?,?)",[name,url,p_name,price])
    conn.commit()
    win2.destroy()

def scrap_details(name,ur):
    url=requests.get(ur)
    soup=bs(url.text)
    price=0
    img_url=""
    pro_name=""
    #ScrapPrice
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
                            price=float("".join(f.text[1:].split(",")))
    #Scrap Image
    elements = soup.find("div", class_="_2c7YLP UtUXW0 _6t1WkM _3HqJxg")
    if elements:
        a = elements.find("div", class_="_1YokD2 _2GoDe3")
        if a:
            b = a.find("div", class_="_1YokD2 _3Mn1Gg col-5-12 _78xt5Y")
            if b:
                c = b.find("div", class_="_1AtVbE col-12-12")
                if c:
                    d = c.find("div", class_="_1iyjIJ")
                    if d:
                        e = d.find("div", class_="_3li7GG")
                        if e:
                            f = e.find("div", class_="_1BweB8")
                            if f:
                                g=f.find("div", class_="_3kidJX")
                                
                                if g:
                                        i=g.find("img")
                                        print(i["src"])
                                        print(i)
                                        img_url=i["src"].replace("/0/0","/714/857")

    elements = soup.find("div", class_="_2c7YLP UtUXW0 _6t1WkM _3HqJxg")
    if elements:
            a = elements.find("div", class_="_1YokD2 _2GoDe3")
            if a:
                b = a.find("div", class_="_1YokD2 _3Mn1Gg col-8-12")
                if b:
                    c = b.find("div", class_="aMaAEs")
                    if c:
                        d = c.find("h1", class_="yhB1nd")
                        
                        if d:
                            e = d.find("span", class_="B_NuCI")
                            print(e.text)
                            pro_name = e.text
    show_product(name,img_url,price,pro_name,ur)

def input_data():
    url=mail.get()
    name=pname.get()
    scrap_details(name,url)

def dlt_prd(l):
    try:
        prd=l.get(ACTIVE)
        a=prd[2]
        cursor.execute("Delete from price_tracker where pro_name== ?",[a])
        conn.commit()
    except:
        messagebox.showinfo("Empty","NO product Available")
    win.destroy()

def delete_product():
    
    win3=Toplevel()
    win3.geometry("600x600")
    lst=Listbox(win3,width=400,height=400)
    cursor.execute("select * from price_tracker")
    b=cursor.fetchall()
    for ip in b:
        lst.insert(END,ip[:-1])
    print(lst)
    lst.place(x=100,y=100,width=800,height=400)
    b=Button(win3,text="Delete",font=("Algerian",20),command=lambda:dlt_prd(lst),activebackground="Yellow",bg="red")
    b.place(x=600,y=550)
    win3.mainloop()

win=Tk()
win.geometry("1280x720")
win.title("Price Track")

bg=Image.open("bg.jpeg")
bg=bg.resize((1280,750))
bg=bg.filter(ImageFilter.BoxBlur(3))
bg=ImageTk.PhotoImage(bg)
bglabel=Label(win,image=bg)


l1=Label(win,text="Track your Price Here ",font=("Forte",40))
l1.place(x=400,y=100)
l2=Label(win,text="Product name ",font=("Arial",20))
l2.place(x=250,y=250)
l3=Label(win,text="Enter Url ",font=("Arial",20))
l3.place(x=250,y=300)
pname=Entry(win)
pname.place(x=450,y=250,width="300",height="30")

mail=Entry(win)
mail.place(x=450,y=300,width="350",height="30")

b1=Button(win,text="Submit",font=("Algerian",20),command=input_data,activebackground="Yellow",bg="red")
b2=Button(win,text="Delete Product",font=("Algerian",20),command=delete_product,activebackground="Yellow",bg="red")
b3=Button(win,text="Exit",font=("Algerian",20),command=lambda:win.destroy(),activebackground="Yellow",bg="red")

b1.place(x=500,y=400,width="200",height="40")
b2.place(x=500,y=450,width="300",height="40")
b3.place(x=500,y=500,width="200",height="40")
bglabel.place(x=0,y=0)
win.mainloop()
conn.close()
