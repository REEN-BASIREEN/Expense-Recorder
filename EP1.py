
from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import datetime

# main program
GUI = Tk() #Tk() คือหน้าจอหลักโปรแกรม
GUI.title('โปรแกรมบันทึก')
GUI.geometry('700x700')



menubar = Menu(GUI)
GUI.config(menu=menubar)


filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')


helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About')

def Donate():
    messagebox.showinfo('Donate','KTC App:0212542255')

donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='Donate',command=Donate)




Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

icon_t1 = PhotoImage(file = 't1_expense.png')
icon_t2 = PhotoImage(file = 't2_expense.png')
        

Tab.add(T1,text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound ='top')
Tab.add(T2,text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')



F1=Frame(T1)
F1.place(x=100,y=50)

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(even=None):
    expense=v_expense.get()
    price=v_price.get()
    quantity=v_quantity.get()

    if expense == '' or price == '' or quantity == '' :
        print('No Data')
        messagebox.showerror('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '' : 
        messagebox.showerror('Error','กรุณากรอกราคา')   
        return
    elif quantity == '' : 
        messagebox.showerror('Error','กรุณากรอกจำนวน')   
        return
    

    try:
        total=int(price)*int(quantity)
        
        print('รายการ:{} ราคาชิ้นละ:{} บาท'.format(expense,price))
        print('จำนวน:{} ชิ้น ค่าใช้จ่ายทั้งหมด:{} บาท'.format(quantity,total))
        text = 'รายการ:{} ราคาชิ้นละ:{} บาท\n'.format(expense,price)
        text = text + 'จำนวน:{} ชิ้น ค่าใช้จ่ายทั้งหมด:{} บาท'.format(quantity,total)
        v_result.set(text)
        
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        today = datetime.now().strftime('%a')
        dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        dt = (days[today]) +'-' + dt

        with open('savedata.csv','a',encoding='utf-8',newline='') as file:
            
            fw = csv.writer(file)
            data = [dt,expense,price,quantity,total]
            fw.writerow(data)
        E1.focus() 
        update_table()

    except:
        print('ERROR')
        messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

GUI.bind('<Return>',Save)


FONT1 = ('Arial Rounded MT Bold',18)

L=ttk.Label(F1,text='รายการ',font=FONT1).pack()
v_expense=StringVar()

E1=ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack(pady=10)

L=ttk.Label(F1,text='ราคา',font=FONT1).pack()
v_price=StringVar()

E2=ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack(pady=10)

L=ttk.Label(F1,text='จำนวน',font=FONT1).pack()
v_quantity=StringVar()

E3=ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack(pady=10)


icon_b1 = PhotoImage(file='b_save.png')

B1=ttk.Button(F1,text='Save',image=icon_b1,compound='left',command=Save)
B1.pack(ipadx=50,ipady=20)

v_result = StringVar()
v_result.set('------ผลลัพธ์-----')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='red')
result.pack(pady=20)



def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8')as f:
        fr = csv.reader(f)
        data = list(fr)
    return data    

L=ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10)   
resulttable.pack()

for h in header:    
    resulttable.heading(h,text=h)

headerwith = [150,200,80,80,80]
for h,w in zip(header,headerwith):
    resulttable.column(h,width=w)


def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()
print('GET CHILD:',resulttable.get_children())

GUI.mainloop()
