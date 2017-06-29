from tkinter import *
from tkinter import ttk
import sys
class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.pack()
        self.t=master
        self.createWidgets()
        self.lock1=0
        self.lock2=0
    def createWidgets(self):
        self.tb=ttk.Notebook(self,height=200,width=300)
        self.tree = ttk.Treeview(self)
        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Path', anchor='w')
        path=['首页','注册']
        root_node = self.tree.insert('', 'end', text='功能', open=True)
        self.process_directory(root_node, path)
        #构建一个grid
        self.tree.grid(row=0, column=0,sticky='n')
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        self.tb.grid(row=0,column=2)
        self.grid()
        self.tree.bind('<<TreeviewSelect>>',self.func)
    def process_directory(self, parent, path):
        #遍历路径下的子目录
        for p in path:
            oid = self.tree.insert(parent, 'end', text=p, open=False)
    def func(self,event):
        #返回对象为Tuple
        select=self.tree.selection()
        select=select[0]
        if select=='I002' and self.lock1==0:
            lable=Label(text='欢迎登陆！',fg='black')
            self.tb.add(lable,text='首页')
            self.lock1=1
        if select=='I003' and self.lock2==0:
            self.child=Frame(self.t)
            self.name=StringVar()
            self.name.set('必填')
            self.psw=StringVar()
            self.psw.set('必填')
            lb=Label(self.child,text='用户名',fg='black')
            lb.grid(row=0,column=0,pady=15,padx=10,sticky='se')
            name=Entry(self.child)
            name['textvariable']=self.name
            name.grid(row=0,column=1)
            la=Label(self.child,text='密码',fg='black')
            la.grid(row=1,column=0,padx=10,sticky='se')
            psw=Entry(self.child)
            psw['textvariable']=self.psw
            psw.grid(row=1,column=1)
            style=ttk.Style()
            style.map("C.TButton",foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'), ('active', 'white')])
            btn1=ttk.Button(self.child,text='提交',style='C.TButton',command=self.submit)
            btn2=ttk.Button(self.child,text='重置',style='C.TButton',command=self.reset)
            btn1.grid(row=2,column=0,pady=10,padx=10,sticky='e')
            btn2.grid(row=2,column=1)
            self.tb.add(self.child,text='修改密码')
            self.lock2=1
    def submit(self):
        fp=open('1.txt','w')
        if self.name.get()!='':
            fp.writelines(self.name.get()+'\n')
        if self.psw.get()!='':
            fp.writelines(self.psw.get())
        fp.close()
    def reset(self):
        self.name.set('')
        self.psw.set('')
root=Tk()
app=Application(root)
app.mainloop()