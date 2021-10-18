from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import Combobox, Checkbutton,Radiobutton,Notebook, Frame
import urllib.request
from xml.dom.minidom import *
from datetime import *
import matplotlib
import matplotlib.pyplot as plt

def vvod(abc,d):
   now=datetime.now()
   now=(now.strftime("%d/%m/%Y"))
   response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+now)
   dom=xml.dom.minidom.parse(response)
   dom.normalize()
   nodeArray=dom.getElementsByTagName("Valute")
   for node in nodeArray:
       childList=node.childNodes
       for child in childList:          
         #  a.append(child.nodeName)
          if(child.nodeName =="Name"):          
             a.append( child.childNodes[0].nodeValue)
             k.append(child.childNodes[0].nodeValue)
             if((a[-1]==abc)and(d==3)):
                #print(ab,abc,child.childNodes[0].nodeValue)
                #c.append( child.childNodes[0].nodeValue)
                return int(ab)          
          if(child.nodeName =="Value"):
             if((a[-1]==abc)and(d==2)):             
                #b.append( child.childNodes[0].nodeValue)
               # print(child.childNodes[0].nodeValue)
                return str( child.childNodes[0].nodeValue)     
          
          if(child.nodeName =="Nominal"):
             ab=child.childNodes[0].nodeValue
           #  if((b[-1]==abc)and(d==3)):
                #print(ab,abc,child.childNodes[0].nodeValue)
                #c.append( child.childNodes[0].nodeValue)
              #  return int(ab)

   
def btn1_click():
   #d=label1.configure(text=entry1.get())
   h=float(entry1.get())
   
   #g=combo1.configure(text=combo1.get())
   d=combo.get()
   if(d!="Российский рубль"):
      e=vvod(d,2)#Стоимость   
      e=float(e.replace(',','.'))
      e1=vvod(d,3)#Номинал
   
   g=combo1.get()
   if(g!="Российский рубль"):
      f=vvod(g,2)#Стоимость 2
      f=float(f.replace(',','.'))   
      f1=vvod(g,3)#Номинал 2   
   
   if(d=="Российский рубль"):
      end=(h*f1/f)
   elif(g=="Российский рубль"):
      end=(h/e1*e)
   else:
      end=(e/e1*h/(f/f1))
   label1.configure(text=end)
   
def poisk():
   d=combo2.get()
   ar=False
   while(ar==False):
      now=c.pop()
      date=now      
      if(now.strftime("%B %Y")==d):
         ar=True
         date=date.strftime("/%m/%Y")      
  
   g=combo3.get()  
   first=1
   last= 30 
   d=0
   while(first!=last):
      days.append(first)
      if(first<10):
         response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+str(0)+str(first)+date)
      else:
         response = urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req="+str(first)+date)
      first=first+1
      dom=xml.dom.minidom.parse(response)
      dom.normalize()
      nodeArray=dom.getElementsByTagName("Valute")
      for node in nodeArray:
          childList=node.childNodes
          for child in childList: 
             if(child.nodeName =="Name"):          
                a.append( child.childNodes[0].nodeValue)                            
             if(child.nodeName =="Value"):
                if(a[-1]==g):
                   e=child.childNodes[0].nodeValue
                   e=float(e.replace(',','.'))
                   e=e/int(ab)
                   value.append(e)
             if(child.nodeName =="Nominal"):
                ab=child.childNodes[0].nodeValue
   
def btn2_click():
   poisk()
   matplotlib.use('TkAgg')
   fig = plt.figure()
   canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig,master=tab2)
   plot_widget=canvas.get_tk_widget()
   fig.clear()
   plt.plot(days,value)
   plt.grid()
   plot_widget.grid(row=5,column=5)
   days.clear()
   value.clear()
   time()

def time():
   now=datetime.now()
   d=12
   i=0
   while(i<d):
      i+=1
      now=((now-timedelta(days=30)))
      c.append(now)
      b.append((now.strftime("%B %Y")))

   
window = Tk()
window.title("Конвертер валют")
window.geometry("800x600")

tab_control=Notebook(window)
tab1=Frame(tab_control)
tab_control.add(tab1,text='Курсы валют')

tab2=Frame(tab_control)
tab_control.add(tab2,text="График")

entry1=Entry(tab1,text="") #Поле ввода текста
entry1.grid(column=1,row=2)#Его расположение

label1=Label(tab1,text="Поле вывода")#Поле вывода
label1.grid(column=3,row=2)

button1 = Button(tab1, text="Конвертировать",command=btn1_click)
button1.grid(column=6,row=1)

button2 = Button(tab2, text="График",command=btn2_click)
button2.grid(column=0,row=4)

a=[]
b=[] 
c=[]
k=[]
days=[]
value=[]

time()

combo=Combobox(tab1)
combo1=Combobox(tab1)
combo2=Combobox(tab2)
combo3=Combobox(tab2)

vvod(1,0)
a.append("Российский рубль")

combo["value"]=(a)
combo1["value"]=(a)
combo2["value"]=(b)
combo3["value"]=(k)
combo.grid(column=1,row=1)
combo1.grid(column=3,row=1)
combo2.grid(column=0,row=0)
combo3.grid(column=0,row=2) 
tab_control.pack(expand = True, fill = 'both')
window.mainloop()
