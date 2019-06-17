import tkinter as tk
from report import Report
from tkinter import ttk
import threading
import datetime
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showerror,showinfo,askyesnocancel,askyesno
import pickle
from math import *
import os
#import subprocess


################################################################################

#Remember to make your own dialogue for french users
################################################################################

class List(list):

    def __init__(self,iterable):

        list.__init__(self,iterable)

    def replace(self,former,new=None):
        try:
            place = self.index(former)
            self[place] = new
        except ValueError:
            print("Former value not found in list")



class Product:
    def __init__(self,productname,unitprice,qty,bulkqty=None,sold=0):
        self.sold = sold
        self.productname=productname
        self.productdescription='A product'
        self.unitprice=unitprice
        self.quantity=qty#This specifies the number of individual units of the product itself
        self.bulkquantity=bulkqty#This specifies the number of cartons packets trays etc of the product
        self.quantityleft=self.quantity#Quantity left is initially the same as the original quantity


    def __str__(self):
        return self.productname

    def setproductname(self,name):
        self.productname=name

    def setunitprice(self,price):
        self.unitprice=price

    def setquantity(self,quantity):
        self.quantityleft=quantity

    def setbulkqty(self,quantity):
        self.bulkquantity=quantity

    def setamt(self,value):
        self.sold=value

    def getproductname(self):
        return self.productname

    def getunitprice(self):
        return self.unitprice

    def getquantity(self):
        return self.quantity

    def getbulkqty(self):
        return self.bulkquantity

    def getquantityleft(self):
        return self.quantityleft

    def getamt(self):
        return self.sold

    def incrementqytby(self,amount):
        self.quantity+=amount

    def reduceqtyby(self,amount):
        self.quantity-=amount




class BusinessManager(tk.Tk):
    def __init__(self,businessname,owner, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.businessname = businessname
        self.description = 'A buiness'
        self.owner = owner
        self.products = []

        self.productnames = []
        self.saves=[self.businessname,self.description,self.owner,self.products,self.productnames]

        self.numberOfvisits=0

        self.currentProduct=0
        self.nname = tk.StringVar()
        #self.overrideredirect(True)

        #We Try automatic load at program start still got some issues with this
        ''' try:
                name= open('lastsave', 'rb')
                self.savename = pickle.load(name)
                self.nname.set(self.savename)
    
            except FileNotFoundError:
                pass
            else:
    
    
                try:
                    bus = open(self.savename, 'rb')
                    recover = pickle.load(bus)
                    self.businessname = recover[0]
                    self.description = recover[1]
                    self.owner = recover[2]
                    self.products = recover[3]
                    self.productnames = recover[4]
                    bus.close()
    
                except FileNotFoundError:
                    pass
                '''

        width=self.winfo_screenwidth()
        height=self.winfo_screenheight()
        self.geometry('%dx%d-0+0'%(width,height))
        self.title('Ndjock Market App {}'.format(self.nname.get()))
        self.minsize(500, 500)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)



        container = tk.Frame(self,width=500,height=500)

        container.grid(row=0,column=0,sticky='nsew')
        container.configure(bg='blue')

        container.columnconfigure(0,weight=1)
        container.rowconfigure(0,weight=1)

        self.currentframe=None

        self.frames = {}

        for F in (WelcomePage,NouveauProduit,GererProduit,Produit,DayReport):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(WelcomePage)#initially we see the login page

        print(self.frames)

        # The Menu
        MyMenu = tk.Menu(self)

        fileMenu = tk.Menu(MyMenu, tearoff=0)
        fileMenu.add_command(label='Nouveau Fichier',accelerator='Ctrl+n',command=self.newin)
        fileMenu.add_command(label='Sauvegarder',accelerator='Ctrl+s',command=self.save)
        fileMenu.add_command(label='Charger',accelerator='Ctrl+l',command=self.load)
        fileMenu.add_command(label="Quiter l'application",accelerator='Alt+F4',command=self.askclose)
        MyMenu.add_cascade(label='Fichiers', menu=fileMenu)

        Gotomenu=tk.Menu(MyMenu,tearoff=0)
        Gotomenu.add_command(label='Page de Démarage',command=lambda :self.show_frame(WelcomePage))
        Gotomenu.add_command(label='Ajouter Produit', command=lambda: self.show_frame(NouveauProduit))
        Gotomenu.add_command(label='Gérrer Produits', command=lambda: self.show_frame(GererProduit))
        Gotomenu.add_command(label='Totaux', command=lambda: self.show_frame(DayReport))
        MyMenu.add_cascade(label='Aller à...', menu=Gotomenu)

        Toolmenu=tk.Menu(MyMenu,tearoff=0)
        Toolmenu.add_command(label='Calculatrice',accelerator='Ctrl+c',command=lambda dummy=0:self.showcalc())
        MyMenu.add_cascade(label='Outils',menu=Toolmenu)
        self.configure(menu=MyMenu)
    
        self.protocol('WM_DELETE_WINDOW', self.askclose)
        
        #Shortcuts of the app
        self.bind('<Control-s>',lambda dummy=0 :self.save())
        self.bind('<Control-l>', lambda dummy=0: self.load())
        self.bind('<Alt-F4>', lambda dummy=0: self.askclose())
        self.bind('<Control-n>', lambda dummy=0: self.newin())
        self.bind('<Control-c>', lambda dummy=0: self.showcalc())




    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def newin(self):
        pass
        #When i am done change .py to .exe

        response=askyesno(title="Fermer cette Session?",message="Voulez vous fermer cette session avant d'ouvrir la nouvelle session?")
        if response==True:
            self.askclose()
            os.startfile("NdjockMarket.py")
        else:
            os.startfile("NdjockMarket.py")

            


    def addproduct(self,name='',unitprice=0,quantity=0,bulkqty=0):
        prod=Product(name,unitprice,quantity,bulkqty)
        self.productnames.append(name)
        self.products.append(prod)

    def removeproduct(self,name):
        try:
            index=self.productnames.index(name)
            self.products.__delitem__(index)
            self.productnames.__delitem__(index)
        except IndexError:
            return "Index is not found in the range of the list"
        except ValueError:
            return " Product not Found in the list of Products"

    def save(self,event=None):
        self.saves = [self.businessname, self.description, self.owner, self.products, self.productnames]

        self.savename=asksaveasfilename(initialdir='C:\\',defaultextension='.obj',filetypes=[('Business Objects','.obj')])

        try:
            savenamefile=open('lastsave','wb')
            

        except:
            pass
        else:
            pickle.dump(self.savename,savenamefile)
            self.title(self.savename)
            self.nname.set(self.savename)  # to change the title of the app
            print(self.productnames)
        try:
            busi=open(self.savename,'wb')
            pickle.dump(self.saves,busi)
            busi.close()

        except:
            showerror(title='Erreur', message="Desole le Fichier n'a pas pu etre sauvegarde")

    def load(self,event=None):
        name=askopenfilename(initialdir='C:\\',defaultextension='.obj',filetypes=[('Business Objects','.obj')])
        try:
            bus=open(name,'rb')
            recover=pickle.load(bus)
            self.businessname=recover[0]
            self.description=recover[1]
            self.owner=recover[2]
            self.products=recover[3]
            self.productnames=recover[4]
            bus.close()
            self.show_frame(WelcomePage)
        except FileNotFoundError:
            showerror(title='File Not found', message="Desole nous n'avons pas trouve le Fichier veuillez reesayer svp")

    def askclose(self):
        reply=askyesnocancel(title='Sauvegarder session', message='Voulez sauvegarder votre session avant de quitter?')
        if reply==True:
            self.save()
            self.destroy()
        elif reply==False:
            self.destroy()
        else:
            pass


    def showcalc(self):
        # The calculator
        a = tk.Toplevel(self)

        a.title("Achilis's Calculator")
        a.minsize(500, 500)
        global equa
        equa= ""
        equation = tk.StringVar()
        label1 = tk.Label(a, textvariable=equation, bg='yellow', font=('Times', 16))
        label1.grid(row=0, column=0, columnspan=4, sticky='nsew')

        equation.set("Enter expression here")
        Ans = ""

        # Button press function
        def bPress(num):
            global equa
            equa = equa + str(num)
            equation.set(equa)

        # Equal function
        def EPress():
            global equa
            global Ans
            try:
                total = str(eval(equa))
                equation.set(total)
                Ans = total
            except:
                equation.set("syn error")
            equa = ""

        # clear function
        def clear():
            global equa
            equa = ""
            equation.set("")

        # Delete function
        def d():
            global equa
            equa = equa[:-1]
            equation.set(equa)

        # cos function
        def c(x):
            try:
                y = cos(radians(x))
                equation.set(str(y))
            except:
                equation.set("syn error")
            else:
                global equa
                global Ans
                Ans = str(y)
                equa = ""

        # sin function
        def s(x):
            try:
                y = sin(radians(x))
                equation.set(str(y))
            except:
                equation.set("syn error")
            else:
                global equa
                global Ans
                Ans = str(y)
                equa = ""

        # Tan function
        def t(x):
            try:
                y = tan(radians(x))
                equation.set(str(y))
            except:
                equation.set("syn error")
            else:
                global equa
                global Ans
                Ans = str(y)
                equa = ""

        # Ans function
        def A():
            global Ans
            global equa
            equa = equa + Ans
            equation.set(equa)

        # factorial function
        def fact(n):
            global equa
            global Ans
            ans = 1
            for i in range(1, n + 1):
                ans = ans * i
            equa = str(ans)
            Ans = equa
            equation.set(equa)
            equa = ""

        # square root function
        def squareroot(n):
            global Ans
            global equa
            x = sqrt(n)
            Ans = str(x)
            equation.set(Ans)
            equa = ""

        def inverse(n):
            global Ans
            global equa
            try:
                x = 1 / n
            except ZeroDivisionError:
                equation.set("Division by Zero not possible")
            else:
                Ans = str(x)
                equation.set(Ans)
                equa = ""

        for i in range(8):
            a.rowconfigure(i, weight=1)

        for i in range(4):
            a.columnconfigure(i, weight=1)

        button0 = tk.Button(a, text='0', font=('Times', 14), fg="white", bg="blue", width=8,
                            command=lambda: bPress(0))


        button0.grid(row=4, column=0, sticky='nsew')
        button1 = tk.Button(a, text="1", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(1))

        button1.grid(row=1, column=0, sticky='nsew')

        button2 = tk.Button(a, text="2", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(2))
        button2.grid(row=1, column=1, sticky='nsew')

        button3 = tk.Button(a, text="3", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(3))
        button3.grid(row=1, column=2, sticky='nsew')
        button4 = tk.Button(a, text=4, fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(4))
        button4.grid(row=2, column=0, sticky='nsew')
        button5 = tk.Button(a, text="5", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(5))
        button5.grid(row=2, column=1, sticky='nsew')
        button6 = tk.Button(a, text="6", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(6))
        button6.grid(row=2, column=2, sticky='nsew')
        button7 = tk.Button(a, text="7", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(7))
        button7.grid(row=3, column=0, sticky='nsew')
        button8 = tk.Button(a, text="8", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(8))
        button8.grid(row=3, column=1, sticky='nsew')
        button9 = tk.Button(a, text="9", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress(9))
        button9.grid(row=3, column=2, sticky='nsew')
        plus = tk.Button(a, text="+", fg="white", bg="blue", font=('Times', 14), width=8,
                         command=lambda: bPress("+"))
        plus.grid(row=1, column=3, sticky='nsew')
        minus = tk.Button(a, text="-", fg="white", bg="blue", font=('Times', 14), width=8,
                          command=lambda: bPress("-"))
        minus.grid(row=2, column=3, sticky='nsew')
        mutiply = tk.Button(a, text="x", fg="white", bg="blue", font=('Times', 14), width=8,
                            command=lambda: bPress("*"))
        mutiply.grid(row=3, column=3, sticky='nsew')
        divide = tk.Button(a, text="/", fg="white", bg="blue", font=('Times', 14), width=8,
                           command=lambda: bPress("/"))
        divide.grid(row=4, column=3, sticky='nsew')
        equal = tk.Button(a, text="=", fg="white", bg="blue", font=('Times', 14), width=8, command=EPress)
        equal.grid(row=4, column=2, sticky='nsew')
        clear = tk.Button(a, text="clear", fg="white", bg="blue", font=('Times', 14), width=8, command=clear)
        clear.grid(row=6, column=3, sticky='nsew')
        delete = tk.Button(a, text="Del", fg="white", bg="blue", font=('Times', 14), width=8, command=d)
        delete.grid(row=5, column=3, sticky='nsew')
        si = tk.Button(a, text="sin", fg="white", bg="blue", font=('Times', 14), width=8,
                       command=lambda: s(float(equa)))
        si.grid(row=5, column=0, sticky='nsew')
        cosine = tk.Button(a, text="cos", fg="white", bg="blue", font=('Times', 14), width=8,
                           command=lambda: c(float(equa)))
        cosine.grid(row=5, column=1, sticky='nsew')
        ta = tk.Button(a, text="tan", fg="white", bg="blue", font=('Times', 14), width=8,
                       command=lambda: t(float(equa)))  # Ans button
        ta.grid(row=5, column=2, sticky='nsew')
        An = tk.Button(a, text="Ans", fg="white", bg="blue", font=('Times', 14), width=8, command=A)
        An.grid(row=6, column=0, sticky='nsew')
        dp = tk.Button(a, text=".", fg="white", bg="blue", font=('Times', 14), width=8,
                       command=lambda: bPress("."))  # decimal point
        dp.grid(row=4, column=1, sticky='nsew')
        power = tk.Button(a, text="x^y", fg="white", bg="blue", font=('Times', 14), width=8,
                          command=lambda: bPress("**"))
        power.grid(row=6, column=1, sticky='nsew')
        lb = tk.Button(a, text="(", fg="white", bg="blue", font=('Times', 14), width=8,
                       command=lambda: bPress("("))
        lb.grid(row=7, column=2, sticky='nsew')
        rb = tk.Button(a, text=")", fg="white", bg="blue", font=('Times', 14), width=8,
                       command=lambda: bPress(")"))
        rb.grid(row=7, column=3, sticky='nsew')
        fac = tk.Button(a, text="!", fg="white", bg="blue", font=('Times', 14), width=8,
                        command=lambda: fact(int(equa)))
        fac.grid(row=6, column=2, sticky='nsew')
        inversebut = tk.Button(a, text='1/x', fg='white', bg='blue', font=('Times', 14), width=8,
                               command=lambda: inverse(float(equa)))
        inversebut.grid(row=7, column=0, sticky='nsew')
        sr = tk.Button(a, text="sqrt", fg="white", bg="blue", font=('Times', 14), width=8,
                       command=lambda: squareroot(float(equa)))
        sr.grid(row=7, column=1, sticky='nsew')

        a.mainloop()




class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        self.configure(width=500,height=500)



        style=ttk.Style()
        print(style.theme_names())
        #style.theme_use('equilux')
        style.configure('Log.TButton',foreground='green', font=("Times",20),background='skyblue')
        style.configure('W.TLabel',background='#ff9999',foreground='#606060',anchor=tk.CENTER)


        self.configure(bg='#ff9999')
        for i in range (4):
            self.rowconfigure(i,weight=1)
        self.columnconfigure(0,weight=1)




        introLabel=ttk.Label(self,text="Bienvenue a l'application Ndjock Market , Que voulez vous faire aujourd'hui??" ,style='W.TLabel',font=('Georgia',19))
        Ajouter = ttk.Button(self,text='Ajouter un Nouveau Produit',style='Log.TButton',width=60,command=lambda:self.controller.show_frame(NouveauProduit))
        Gerer = ttk.Button(self,text='Gerer mes Produits',style='Log.TButton',width=60,command=lambda:self.controller.show_frame(GererProduit))
        Comptes = ttk.Button(self, text='Comptes Total du Jour', style='Log.TButton', width=60,
                           command=lambda: self.controller.show_frame(DayReport))
        Quiter = ttk.Button(self,text='Quiter',style='Log.TButton',width=60,command=self.quitt)

        introLabel.grid(row=0, column=0, padx=60, pady=60)

        Ajouter.grid(row=1, column=0,padx=50,pady=10,ipady=10)
        Gerer.grid(row=2, column=0,pady=10,ipady=10)
        Comptes.grid(row=3, column=0, pady=10, ipady=10)
        Quiter.grid(row=4, column=0,pady=10,ipady=10)



    def quitt(self,event=None):
        response=askyesnocancel(title='Sauvegarder?',message='Voulez vous sauvegarder votre session avant de quiter?')
        if response==True:
            self.controller.save()
            self.controller.destroy()
        elif response==False:
            self.controller.destroy()
        else:
            pass



class NouveauProduit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller


        self.configure(width=500,height=500)
        self.configure(bg='skyblue')
        sty=ttk.Style()
        sty.configure('D.TLabel', background='skyblue')
        sty.configure('D.TEntry')
        sty.configure('D.TButton', padding=20, foreground='black', background='black',font=('times',20),width=20)

        NameLabel=ttk.Label(self,text='Entrez le Nom du produit :',style="D.TLabel",font=('Times',20))
        self.NAmeEntry=ttk.Entry(self,name="nameEntry",font=('Times',23))

        UnitpriceLabel = ttk.Label(self,text="Entrez le prix d'une unite:",style='D.TLabel',font=('Times',20))
        self.UnitpriceEntry = ttk.Entry(self,name="priceEntry",font=('Times',23))

        QtyLabel = ttk.Label(self, text='Entrez la quantité initiale  :', style="D.TLabel", font=('Times', 20))
        self.QtyEntry = ttk.Entry(self,name="qtyEntry", font=('Times', 23))

       # bulkQtyLabel = ttk.Label(self, text='Entrez le nombre de cartons/paquets  :', style="D.TLabel", font=('Times', 20))
        #self.bulkQtyEntry = ttk.Entry(self, font=('Times', 23))

        self.SubmitButton=ttk.Button(self,text='Ajouter',style='D.TButton',command=self.getinputs)

        self.controller.bind('<Down>', lambda dummy=0: self.changefocus())


        self.rowconfigure(0,weight=4)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=4)
        self.rowconfigure(3,weight=4)
        self.rowconfigure(4, weight=1)

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1, weight=1)



        NameLabel.grid(row=0,column=0,padx=10,sticky='e')
        self.NAmeEntry.grid(row=0,column=1,ipadx=40,sticky='w')

        UnitpriceLabel.grid(row=1,column=0,padx=10,sticky='e')
        self.UnitpriceEntry.grid(row=1,column=1,ipadx=40,sticky='w')

        QtyLabel.grid(row=2,column=0,padx=10,sticky='e')
        self.QtyEntry.grid(row=2,column=1,ipadx=40,sticky='w')

        #bulkQtyLabel.grid(row=3, column=0, padx=10, sticky='e')
        #self.bulkQtyEntry.grid(row=3, column=1, ipadx=40, sticky='w')


        self.SubmitButton.grid(row=4,column=1,padx=45,columnspan=1,sticky='w')

        self.NAmeEntry.focus_set()




    def getintt(self,item:ttk.Entry):


        try:
            value = int(item.get())

        except ValueError :
            return 'Error'

        else:

            return value


    def getinputs(self, event=None):
        if self.NAmeEntry.get()=='':
            name='Inconnu'

        else:
            name=self.NAmeEntry.get()
            self.NAmeEntry.delete(0,tk.END)

        price=self.getintt(self.UnitpriceEntry)
        if self.getintt(self.UnitpriceEntry)!='Error':

            self.UnitpriceEntry.delete(0,tk.END)
        else:
            showerror(title='Erreur', message='La valeur du prix doit etre un nombre entier')
            self.UnitpriceEntry.delete(0, tk.END)

        qty = self.getintt(self.QtyEntry)

        if self.getintt(self.QtyEntry) != 'Error':
            self.QtyEntry.delete(0, tk.END)
            response = askyesno(title='Continuer?', message="Etes vous sur de vouloir valider ces valeurs?")
            if response==True:
                self.controller.addproduct(name, price, qty)

                showinfo(title='Succes', message='Le produit a été ajouté avec succès')
                self.controller.show_frame(WelcomePage)
            else:
                showinfo(title="Nouvelles Valeurs", message="S'il vous plait entrez des Nouvelles valeurs")
        else:
            showerror(title='Erreur', message='La valeur de la quantité doit etre un nombre entier')
            self.QtyEntry.delete(0, tk.END)





        ################################# work on this later

    def changefocus(self):
        if self.focus_get().__str__()=='nameEntry':
            self.UnitpriceEntry.focus_set()

        elif self.focus_get().__str__()=='priceEntry':
            self.QtyEntry.focus_set()

        elif self.focus_get().__str__()=='qtyEntry':
            self.SubmitButton.focus_set()
        else:
            self.NAmeEntry.focus_set()

    ###########################################################

class GererProduit(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.configure(width=500, height=500)
        self.configure(bg='skyblue')

        self.buttons=[]
        self.prod=None
        sty = ttk.Style()
        sty.configure('Log.TButton', foreground='green', font=("Times", 20), background='skyblue')
        sty.configure('My.TButton', foreground='black', background='skyblue',font=('times',20),width=50)
        sty.configure('TLabelframe', background='skyblue',foreground='green')

        self.rowconfigure(0,weight=1)


        self.columnconfigure(0,weight=1)
        message=ttk.Label(self,text='Selectionez le produit que vous voulez gerer',style='D.TLabel' ,font=('Times',18))
        message.grid(row=0,column=0)
        threading._start_new_thread(self.refresh1,())




    def refresh1(self):


        for i in range(len(self.controller.productnames)):

            #This part makes sure that the buttons are not replaced by new ones at each turn of the loop

            try:
                if self.buttons[i]!='':
                    pass
            except IndexError:
                but = ttk.Button(self, text=self.controller.productnames[i], style='My.TButton' ,
                                                                command=lambda:self.showProd(i-1))
                self.buttons.insert(i, but)

            finally:
                pass

        #button product array


        i=0
        for button in self.buttons:

            self.grid_rowconfigure(i+1, weight=5)

            button.grid(row=i+1,column=0)
            i+=1


        #We make use of recursion to call the refresh method indefinitely(after every 500ms)
        self.after(1000,self.refresh1)

    def showProd(self,index):
        try:
            if self.controller.products[index]!=0:#We use this just to check if $index  is a valid index
                pass

        except IndexError:
            index=index-1 #if not we reduce it by one(=> an item was removed from products list just before it and its index reduced by one
        finally:
            #We modify the values of the variables of the produit class directly from here depending on the product chosen
            self.controller.frames[Produit].productname.set(self.controller.products[index].getproductname())

            self.controller.frames[Produit].initialStock.set(self.controller.products[index].getquantity())

            self.controller.frames[Produit].Price.set(self.controller.products[index].getunitprice())
            self.controller.frames[Produit].Price.set(self.controller.frames[Produit].Price.get()+' FCFA')

            self.controller.frames[Produit].grossStock.set(self.controller.products[index].bulkquantity)

            self.controller.frames[Produit].quantityLeft.set(self.controller.products[index].getquantityleft())
            self.controller.frames[Produit].itemnum.set(index)
            try:
                self.controller.frames[Produit].TodayFrame.grid_forget()
            except:
                pass

            self.controller.show_frame(Produit)

class Produit(tk.Frame):

    #@Now i have to design my interface
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller

        lab = tk.Label(self, text="Compte du {}".format(datetime.date.today()), font=('Comic Sans Ms', 15), fg='blue',
                       bg='violet')
        self.TodayFrame=ttk.Labelframe(self, text="Aujourd'hui", labelwidget=lab, labelanchor='n')

        mysty=ttk.Style()

        self.configure(bg='skyblue')



        self.productname=tk.StringVar(self)
        self.initialStock = tk.StringVar(self)
        self.quantityLeft=tk.StringVar(self)
        self.grossStock=tk.StringVar(self)
        self.Price=tk.StringVar(self)
        self.itemnum=tk.IntVar(self)
        self.checkVar = tk.IntVar()

        self.newquantityleft=tk.StringVar(self)
        self.quantitysold=tk.StringVar()
        self.amountsold=tk.StringVar()
        self.amountsold.set('0')



        self.columnconfigure(0,weight=1)


        #The former day text
        daynow=datetime.date.today()
        daynow=str(daynow)

        lab = tk.Label(self,text='Journée précédente', font=('Times', 15), fg='blue', bg='violet')
        formerdayFrame=ttk.Labelframe(self,text='Jour précédant',labelwidget=lab,labelanchor='n')


        name=ttk.Label(formerdayFrame,text='Nom : ',font=('Times',20),style='D.TLabel')
        price=ttk.Label(formerdayFrame,text="Prix d'unité :",font=('Times',20),style='D.TLabel')
        initstock=ttk.Label(formerdayFrame,text='Stock Initial : ',font=('Times',20),style='D.TLabel')
        quantity=ttk.Label(formerdayFrame,text='Reste : ',font=('Times',20),style='D.TLabel')
        #CFA = ttk.Label(formerdayFrame, text=' FCFA ', font=('Times', 20), style='D.TLabel')

        mysty.configure("DW.TLabel", anchor=tk.W)
        mysty.configure('TCheckbutton',background='aqua')

        productnameLabel=ttk.Label(formerdayFrame,textvariable=self.productname,font=('Times',20),style='D.TLabel')
        initstockLabel=ttk.Label(formerdayFrame,textvariable=self.initialStock,style='D.TLabel',font=('Times',20))
        #grossLabel = ttk.Label(formerdayFrame, textvariable=self.grossStock, style='D.TLabel',font=('Times',20))
        priceLabel=ttk.Label(formerdayFrame,textvariable=self.Price,style='D.TLabel',font=('Times',20))
        quantityleftLabel=ttk.Label(formerdayFrame,textvariable=self.quantityLeft,style='D.TLabel',font=('Times',20))

        compteDuJourBut=ttk.Button(self, text='Comptes du Jour',style='My.TButton',command=self.comptes)
        enleverProduitBut = ttk.Button(self, text='Suprimer le Produit', style='My.TButton', command=self.deleteproduct)
        GenererRapportBut = ttk.Button(self, text='Sauvegarder Rapport du Jour', style='My.TButton', command=self.generateR)
        ModifierBut = ttk.Button(self, text='Modifier le Produit', style='My.TButton', command=self.editprod)

        #stretching
        formerdayFrame.columnconfigure(0,weight=1)
        formerdayFrame.columnconfigure(1,weight=1)



        name.grid(row=0,column=0,sticky='e')
        price.grid(row=1,column=0,sticky='e')
        initstock.grid(row=2,column=0,sticky='e')
        quantity.grid(row=3,column=0,sticky='e')


        productnameLabel.grid(row=0,column=1,sticky='w')
        priceLabel.grid(row=1, column=1, sticky='w')
        initstockLabel.grid(row=2,column=1,sticky='w')
        quantityleftLabel.grid(row=3,column=1,sticky='w')
        #CFA.grid(row=1,column=2, sticky='w')#Label that displays currency





        enleverProduitBut.grid(row=2,column=0)
        ModifierBut.grid(row=3,column=0)
        GenererRapportBut.grid(row=4,column=0)
        formerdayFrame.grid(row=0,column=0,sticky='nsew',padx=20,pady=20)
        compteDuJourBut.grid(row=1,column=0)

        ###############################################################################################################
    def deleteproduct(self):
        response=askyesnocancel(title="Supprimer Produit?" ,message='Voulez vous vraiment supprimer ce produit?')
        if response==True:
            self.controller.show_frame(GererProduit)
            self.controller.removeproduct(self.productname.get())
            prodNumber=self.itemnum.get()
            self.controller.frames[GererProduit].buttons[prodNumber].destroy()#Removes the button of the current item from the screen
            self.controller.frames[GererProduit].buttons.__delitem__(prodNumber)#this part goes to the Gerer produit class
            # and deletes the button from the self.buttons list



            a=self.controller.frames[DayReport].grid_slaves(self.itemnum.get()+2,0)#We select all widgets found at that position
            b = self.controller.frames[DayReport].grid_slaves(self.itemnum.get() + 2, 1)

            #we then destroy all of them
            for item in a:
                item.destroy()
            for item2 in b:
                item2.destroy()


           

        else:
            pass

    def generateR(self):
        report=Report(datetime.date.today(),self.productname.get(),self.Price.get(),self.initialStock.get(),self.quantityLeft.get(),self.newquantityleft.get(),
                      self.quantitysold.get(),self.amountsold.get())
        
        #############################################
        #See this later
        name=asksaveasfilename(title="Sauvegarder votre session",initialfile='Rapport des {}_du _{}.html'.format(self.productname.get(),datetime.date.today()),filetypes=[("html page",".html")])
        
        name=[x for x in name.split("/")]
    
        name[len(name)-1]='Rapport des {}_du _{}.html'.format(self.productname.get(),datetime.date.today())
        name='/'.join(name)
        print(name)
        reportfile=open(name,'w+')
        reportfile.write(report.generateReport())
        reportfile.close()


    def comptes(self):

        def compteOday():




            name1 = ttk.Label(self.TodayFrame, text='Nom : ', font=('Times', 20), style='D.TLabel')
            price1 = ttk.Label(self.TodayFrame, text="Prix d'unité :", font=('Times', 20), style='D.TLabel')
            initstock1 = ttk.Label(self.TodayFrame, text='Stock Initial : ', font=('Times', 20), style='D.TLabel')
            quantity1 = ttk.Label(self.TodayFrame, text='Reste : ', font=('Times', 20), style='D.TLabel')
            qtsold1 = ttk.Label(self.TodayFrame, text='Quantité Vendu : ', font=('Times', 20), style='D.TLabel')
            amtsold1 = ttk.Label(self.TodayFrame, text='Somme Vendu : ', font=('Times', 20), style='D.TLabel')


            productnameLabel1 = ttk.Label(self.TodayFrame, textvariable=self.productname, font=('Times', 20),
                                          style='D.TLabel')
            initstockLabel1 = ttk.Label(self.TodayFrame, textvariable=self.initialStock, style='D.TLabel',
                                        font=('Times', 20))
            soldLabel = ttk.Label(self.TodayFrame, textvariable=self.quantitysold, style='D.TLabel', font=('Times', 20))
            amtsoldLabel = ttk.Label(self.TodayFrame, textvariable=self.amountsold, style='D.TLabel', font=('Times', 20))
            priceLabel1 = ttk.Label(self.TodayFrame, textvariable=self.Price, style='D.TLabel', font=('Times', 20))
            quantityleftLabel1 = ttk.Label(self.TodayFrame, textvariable=self.newquantityleft, style='D.TLabel',
                                           font=('Times', 20))

            # compteDuJourBut = ttk.Button(self, text='Comptes du Jour', style='My.TButton', command=self.comptes)

            # stretching
            self.TodayFrame.columnconfigure(0, weight=1)
            self.TodayFrame.columnconfigure(1, weight=1)

            name1.grid(row=0, column=0, sticky='e')
            price1.grid(row=1, column=0, sticky='e')
            initstock1.grid(row=2, column=0, sticky='e')
            quantity1.grid(row=3, column=0, sticky='e')
            qtsold1.grid(row=4,column=0,sticky='e')
            amtsold1.grid(row=5, column=0, sticky='e')


            productnameLabel1.grid(row=0, column=1, sticky='w')
            priceLabel1.grid(row=1, column=1, sticky='w')
            initstockLabel1.grid(row=2, column=1, sticky='w')
            quantityleftLabel1.grid(row=3, column=1, sticky='w')
            soldLabel.grid(row=4,column=1,sticky='w')
            amtsoldLabel.grid(row=5, column=1, sticky='w')

            self.TodayFrame.grid(row=5, column=0, sticky='nsew', padx=20, pady=20)


        def submit():
            try:
                rest=int(restEntry.get())
            except ValueError:
                showerror(title='Erreur',message='Valeur incorrecte')
            else:
                if addQtyEntry.cget('state')=='disabled':
                    if rest>int(self.quantityLeft.get()):
                        showerror(title="Erreur", message="la valeure du reste est incorrecte")
                    else:
                        newQty=rest
                        qtysold=int(self.quantityLeft.get())-newQty
    
                        temp=self.Price.get()
                        temp=[x for x in temp.split(' ')]#we separate the price and the CFA suffix
                        temp=temp[0]#this is the priice only e.g [100,'FCFA'] temp[0]=100
    
    
                        amtsold=qtysold*int(temp)
                        self.controller.products[self.itemnum.get()].setamt(amtsold)#Sets the amount sold variable of the product object to amtsold
    
                        self.newquantityleft.set(newQty)
                        self.quantitysold.set(str(qtysold))
                        self.amountsold.set(str(str(amtsold) + ' FCFA'))
                        self.controller.products[self.itemnum.get()].setquantity(newQty)
                        compteOday()
                else:
                    try:
                        if addQtyEntry.get()=='':
                            add=0
                        else:
                            add=int(addQtyEntry.get())
                    except ValueError:
                        showerror(title='Erreur',message='Valeur de la quantité ajouté incorrecte')

                    else:
                        
                        if rest>int(self.quantityLeft.get())+add:
                            showerror(title="Erreur", message="la valeure du reste est incorrecte")
                        
                        else:
                            
                            newQty=rest
                            left=str(newQty) + '(Vous avez ajouté {} {})'.format(add, self.productname.get())
                            self.newquantityleft.set(left)
    
                            qtysold = (int(self.quantityLeft.get())+add) - rest
    
    
                            temp = self.Price.get()
                            temp = [x for x in temp.split(' ')]
                            temp = temp[0]
                            amtsold = qtysold * int(temp)
                            self.controller.products[self.itemnum.get()].setamt(amtsold)##Again!!
    
                            #self.newquantityleft.set(newQty)
                            self.quantitysold.set(str(qtysold))
                            self.amountsold.set(str(str(amtsold) + ' FCFA'))
    
                            self.controller.products[self.itemnum.get()].setquantity(newQty)
                            compteOday()
            finally:
                compteWindow.destroy()





                        #self.controller.products[self.itemnum.get()].setquantity(newQty)

                        #Now we set the quantity left to the sum of the rest and the added quantity
        def check():
            if self.checkVar.get()==0:
                addQtyEntry.delete(0,tk.END)
                addQtyEntry.configure(state='disabled')
            else:
                addQtyEntry.configure(state='normal')

        compteWindow=tk.Toplevel(self)
        compteWindow.geometry('600x300')
        compteWindow.minsize(600,300)
        compteWindow.maxsize(800,300)
        compteWindow.title('Comptes des {} du Jour'.format(self.productname.get()))
        compteWindow.configure(bg='skyblue')



        restLabel=ttk.Label(compteWindow,text='Reste :', font=('Times',20),style='D.TLabel')
        restEntry=ttk.Entry(compteWindow,font=('Times',23))
        ttk.Label(compteWindow,text='Entrez les valeurs demandés',anchor=tk.E,style='D.TLabel',font=('Times',20)).grid(row=0,column=0,columnspan=2)
        addQty=ttk.Label(compteWindow,text='Ajouter Quantité : ',font=('Times',20),style='D.TLabel')
        addQtyEntry=ttk.Entry(compteWindow,font=('Times',23), state='disabled')
        add=ttk.Checkbutton(compteWindow,text='augmenter la quantité du produit?', variable=self.checkVar, command=check)
        finishBut=ttk.Button(compteWindow,text='Terminer', style='D.TButton',command=submit)

        compteWindow.rowconfigure(0,weight=1)
        compteWindow.rowconfigure(1, weight=1)
        compteWindow.rowconfigure(2, weight=1)
        compteWindow.rowconfigure(3, weight=1)

        compteWindow.columnconfigure(0,weight=1)
        compteWindow.columnconfigure(1, weight=15)


        restLabel.grid(row=1,column=0)
        restEntry.grid(row=1,column=1)
        addQty.grid(row=2,column=0, pady=20)
        addQtyEntry.grid(row=2,column=1)
        finishBut.grid(row=3,column=1,columnspan=1, pady=20)
        add.grid(row=3,column=0,sticky='nw')

        compteWindow.tkraise()
        compteWindow.focus_set()
        restEntry.focus_set()
    
    def editprod(self):
        
        def submit():
            
            if((nameEntry.get())!=""):
                name=nameEntry.get()
                self.controller.products[self.itemnum.get()].setproductname(name)
                self.controller.frames[GererProduit].buttons[self.itemnum.get()].configure(text=name)
                self.productname.set(name)
                
            if(UnitPriceEntry.get()!="" ):
                try:
                    price=int(UnitPriceEntry.get())
                except ValueError:
                    showerror(title="Erreur",message="La valeur du prix est incorrecte")
                    EditWindow.tkraise()
                    EditWindow.focus_set()
                self.controller.products[self.itemnum.get()].setunitprice(price)
                self.Price.set(str(price))
                
                
            if(qtyEntry.get()!=""):
                try:
                    qty=int(qtyEntry.get())
                except ValueError:
                    showerror(title="Erreur",message="La valeur de la quantité est incorrecte")
                    EditWindow.tkraise()
                    EditWindow.focus_set()
                
                self.controller.products[self.itemnum.get()].setquantity(qty)
                self.initialStock.set(str(qty))
            EditWindow.destroy()
                
        
        EditWindow=tk.Toplevel(self)
        EditWindow.geometry('600x300')
        EditWindow.minsize(600,300)
        EditWindow.maxsize(800,300)
        EditWindow.title(' Modifier {}'.format(self.productname.get()))
        EditWindow.configure(bg='skyblue')



        nameLabel=ttk.Label(EditWindow,text='Nom :', font=('Times',20),style='D.TLabel')
        nameEntry=ttk.Entry(EditWindow,font=('Times',23))
        
        ttk.Label(EditWindow,text='Entrez les valeurs que vous voulez changer',anchor=tk.E,style='D.TLabel',font=('Times',20)).grid(row=0,column=0,columnspan=2)
        
        UnitPrice=ttk.Label(EditWindow,text="Prix d'unité :" ,font=('Times',20),style='D.TLabel')
        UnitPriceEntry=ttk.Entry(EditWindow,font=('Times',23))
        
        qtyLabel=ttk.Label(EditWindow,text='quantité', font=('Times',20),style='D.TLabel')
        qtyEntry=ttk.Entry(EditWindow,font=('Times',23))
        
        finishBut=ttk.Button(EditWindow,text='Terminer', style='D.TButton', command=submit)

        EditWindow.rowconfigure(0,weight=1)
        EditWindow.rowconfigure(1, weight=1)
        EditWindow.rowconfigure(2, weight=1)
        EditWindow.rowconfigure(3, weight=1)
        EditWindow.rowconfigure(4, weight=1)

        EditWindow.columnconfigure(0,weight=1)
        EditWindow.columnconfigure(1, weight=15)


        nameLabel.grid(row=1,column=0)
        nameEntry.grid(row=1,column=1)
        UnitPrice.grid(row=2,column=0, pady=20)
        UnitPriceEntry.grid(row=2,column=1)
        qtyLabel.grid(row=3,column=0)
        qtyEntry.grid(row=3,column=1)
        finishBut.grid(row=4,column=1,columnspan=1, pady=20)
        

        EditWindow.tkraise()
        EditWindow.focus_set()
        


class DayReport(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.parent=parent



        
        mysty = ttk.Style()
        mysty.configure("Total.TLabel",background="blue", foreground='white')
        mysty.configure("Another.TLabel", background="skyblue", foreground='black',padding=20)
        mysty.configure("Anotherr.TLabel", background="red", foreground='black',  width=20)

        self.configure(bg='skyblue')

        self.controller=controller
        self.rowconfigure(0,weight=2)
        self.columnconfigure(0,weight=1)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=5)

        myimg=tk.PhotoImage(file='nm.gif')

        self.welcomeLabel=ttk.Label(self,text="Les Totaux du Jour",anchor=tk.CENTER, style='Total.TLabel', font=("Comic Sans Ms",30,'bold','italic'))
        
        self.totalbut=ttk.Button(self,text='Afficher total', style="D.TButton", command=self.showinfo)
        self.clearbut=ttk.Button(self,text='Effacer total', style="D.TButton", command=self.clearinfo)
        
        NomLabel=ttk.Label(self,text='Produit', name='', font=("Comic Sans Ms",20,'bold','underline'),style="Another.TLabel")
        QuantityLabel=ttk.Label(self,text='Quantité Vendu', font=("Comic Sans Ms",20,'bold','underline') ,style="Another.TLabel")

        NomLabel.grid(row=1, column=0)
        
        self.totalbut.grid(row=0,column=0,sticky='sw')
        self.clearbut.grid(row=0,column=1,sticky='se')
        
        QuantityLabel.grid(row=1, column=1)
        self.welcomeLabel.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.lab1 = ttk.Label(self, text='Total', font=('Comic Sans Ms', 19,'bold'), style='Anotherr.TLabel')
        self.lab2 = ttk.Label(self, text='', font=('Comic Sans Ms', 19,'bold'), style='Anotherr.TLabel')


        #threading._start_new_thread(self.showinfo, ())


    def showinfo(self):
        sum = 0
        try:

            self.lab1.grid_forget()
            self.lab2.grid_forget()
        except AttributeError as e:
            print(e)

        #We place the labels ( name and amount)
        for i in range ( len(self.controller.products)):
            name=self.controller.productnames[i]
            amount=self.controller.products[i].getamt()
            sum+=amount

            ttk.Label(self,text=name,anchor=tk.W, font=('Comic Sans Ms',19) ,style='Another.TLabel').grid(row=i+2,column=0)#We start griding from row 2
            ttk.Label(self, text='{} FCFA'.format(amount),anchor=tk.W, font=('Comic Sans Ms', 19), style='Another.TLabel').grid(row=i + 2, column=1)
            self.rowconfigure(i+2,weight=1)

        k=len(self.controller.products)
        self.lab2.configure(text=str(sum)+' FCFA')

        self.lab1.grid(row=k + 2, column=0)  # We start griding from row 2  To make sure it(the totals) is always positioned at the bottom
        self.lab2.grid(row=k + 2,column=1)
        
        
    
    def clearinfo(self):
        #This function clears all the totals on the totals display screen
        
        def clear(ro,col):
            #This function removes all widgets on row ro and column col on the totals screen
            items=self.grid_slaves(row=ro,column=col) #The grid slaves method 
                                                      #returns a list of all the widgets grided on the precised row and column of the frame 
            for item in items:
                item.grid_forget()
            
        
        for i in range ( len(self.controller.products)+1):#+1 because we want to include also the row that shows totals
            clear(i+2,0)#names and prices start from the second row on column 0 and 1
            clear(i+2,1)
        
            
        
      

if __name__ == '__main__':
    app=BusinessManager('Ndjock Market','Ndjock Philo')
    app.focus_set()
    app.mainloop()

    def newin(self):
        app2=BusinessManager('Ndjock Market','Ndjock Philo')
        app2.mainloop()

