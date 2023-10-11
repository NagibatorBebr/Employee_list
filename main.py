#Импорт нужных библиотек
import tkinter as tk
from tkinter import ttk
import sqlite3

#Класс главного окна
class Main(tk.Frame):

    def __init__(self,root):#инициализация
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
       

    def init_main(self):# инициализация всех элементов окна
        
        toolbar = tk.Frame(bg='#ffd88a',bd=2) # Панель инструментов
        toolbar.pack(side=tk.LEFT,fill=tk.Y)
        
        
        self.add_img = tk.PhotoImage(file = './img/add.png')#создание и размещение кнопки добавить  с фотографией
        btn_open_dialog = tk.Button(toolbar,bg='#ffd88a',bd= 0,
                                    image= self.add_img,
                                    command=self.open_other
        )
        btn_open_dialog.pack(side=tk.TOP)


        self.delete_img = tk.PhotoImage(file = './img/delete.png')#создание и размещение кнопки удалить с фотографией
        btn_delete = tk.Button(toolbar,bg='#ffd88a',bd=0, 
                                    image= self.delete_img,
                                    command=self.delete_records)
        btn_delete.pack(side=tk.TOP)


        self.edit_img = tk.PhotoImage(file ='./img/edit.png')#создание и размещение кнопки редактировать  с фотографией
        btn_edit = tk.Button(toolbar,bg='#ffd88a', bd=0,
                                    image= self.edit_img,
                                    command=self.open_edit)
        btn_edit.pack(side=tk.TOP)

        self.search_img = tk.PhotoImage(file='./img/search.png')#создание и размещение кнопки поиск  с фотографией
        btn_search = tk.Button(toolbar,bg='#ffd88a',bd =0,
                                    image= self.search_img)
        btn_search.bind('<Button-1>',lambda event:self.search_records(entry.entry_var.get()))
        btn_search.pack(side=tk.TOP)

        btn_show_all = tk.Button(root,text='Показать всё',command=self.view_records)#создание и размещение кнопки показать всё
        btn_show_all.place(x=150,y=430)

        #создание таблицы для размещения сотрудниклв
        self.tree = ttk.Treeview(
            self,
            columns=('ID','name','phone','email','wages'),
            height=20,show='headings')
        
        #расположение столбцов
        self.tree.column('ID',width=30,anchor=tk.CENTER)
        self.tree.column('name',width=240,anchor=tk.CENTER)
        self.tree.column('phone',width=130,anchor=tk.CENTER)
        self.tree.column('email',width=130,anchor=tk.CENTER)
        self.tree.column('wages',width=130,anchor=tk.CENTER)

        #установка удобных заголовков
        self.tree.heading('ID',text='ID')
        self.tree.heading('name',text='ФИО')
        self.tree.heading('phone',text='Номер телефона')
        self.tree.heading('email',text='E-mail')
        self.tree.heading('wages',text='Зарплата')
        self.tree.pack(side=tk.LEFT)

        
        
        

    
    def open_other(self): #функция для открытия дочернего другого окна
        Other()

    def records(self,name,phone,email,wages): #функция для отображения записей
        self.db.insert_data(name,phone,email,wages)
        self.view_records()

    def view_records(self): #функция для обновления показа записей
        self.db.cur.execute('SELECT * FROM Employee')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()]

    def delete_records(self): #функция для удаления записей
        for i in self.tree.selection():
            self.db.cur.execute(
                'DELETE FROM Employee WHERE id=?',(self.tree.set(i,'#1'))
            )

        self.db.conn.commit()
        self.view_records()


    def open_edit(self): # функция для открытия окна редактирования
        Edit()
    
    def edit_records(self,name,phone,email,wages): # функция для редактирования записей
        self.db.cur.execute('UPDATE Employee SET name = ?,phone = ?, email = ?, wages = ? WHERE id = ?',(name,phone,email,wages, self.tree.set(self.tree.selection() [0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def search_records(self,name): # функиця для поиска записей
        name = "%" + name + "%"
        self.db.cur.execute("SELECT * FROM Employee WHERE name LIKE ?", (name,)) 

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()]

#класс дочернего окна
class Other(tk.Toplevel):
    def __init__(self): #инициализация
        super().__init__(root)
        self.init_other()
        self.view = app

    def init_other(self): #инициализация окна и его элементов
        self.title('Добавить')
        self.geometry('440x300')
        self.resizable(False,False)
        self.focus_set()
        self.grab_set()

        #создание наименований и полей для ввода данных
        label_name = tk.Label(self,text='ФИО:')
        label_name.place(x=50,y=40)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200,y=40)

        label_phone = tk.Label(self,text='Номер телефона:')
        label_phone.place(x=50,y=70)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200,y=70)
        
        label_email = tk.Label(self,text='Email:')
        label_email.place(x=50,y=100)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200,y=100)

        label_wages = tk.Label(self,text='Заработная плата:')
        label_wages.place(x=50,y=130)
        self.entry_wages = ttk.Entry(self)
        self.entry_wages.place(x=200,y=130)

        #размещение кнопки отменить
        self.btn_cancel = ttk.Button(self,text='Закрыть',command=self.destroy)
        self.btn_cancel.place(x=50,y=250)

        #размещение кнопки добавить
        self.btn_ok = ttk.Button(self,text='Добавить')
        self.btn_ok.place(x=140,y=250)

        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.records(
                             self.entry_name.get(),self.entry_phone.get(),self.entry_email.get(),self.entry_wages.get()
                         ))
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.destroy(),add='+')

#класс окна Редактировать
class Edit(Other):
    def __init__(self): # инициализация
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.view_def_data()

    
    def init_edit(self): #инициализация окна и элементов
        self.title('Редактировать сотрудника')
        self.btn_ok.destroy()
        
        #размещение кнокпи Редактировать
        btn_edit = ttk.Button(self,text='Редактировать')
        btn_edit.place(x=140,y=250)
        btn_edit.bind('<Button-1>', lambda event:self.view.edit_records(self.entry_name.get(),self.entry_phone.get(),self.entry_email.get(),self.entry_wages.get()))
        btn_edit.bind('<Button-1>', lambda event:self.destroy(),add='+')
        
    def view_def_data(self):#функция для заполнения изначальных данных в поля ввода
        self.db.cur.execute('SELECT * FROM Employee WHERE id = ?',
                            self.view.tree.set(self.view.tree.selection() [0], '#1'))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_phone.insert(0,row[2])
        self.entry_email.insert(0,row[3])
        self.entry_wages.insert(0,row[4])

#класс строки поиска
class EntrySearch(tk.Entry):
    def __init__(self, master=None, placeholder=None): # инициализцаия
        self.entry_var = tk.StringVar()
        super().__init__(master, textvariable=self.entry_var)
        self.view = app

        #реализация подсказки в строке поиска
        if placeholder is not None:
            self.placeholder = placeholder
            self.placeholder_color = 'grey'
            self.default_fg_color = self['fg']
            self.placeholder_on = False
            self.put_placeholder()

            self.entry_var.trace("w", self.entry_change)

            # При всех перечисленных событиях, если placeholder отображается, ставить курсор на 0 позицию
            self.bind("<FocusIn>", self.reset_cursor)
            self.bind("<KeyRelease>", self.reset_cursor)
            self.bind("<ButtonRelease>", self.reset_cursor)

    def entry_change(self, *args):
        if not self.get():
            self.put_placeholder()
        elif self.placeholder_on:
            self.remove_placeholder()
            self.entry_change()  # На случай, если после удаления placeholder остается пустое поле

    def put_placeholder(self): # вставка подсказки
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.icursor(0)
        self.placeholder_on = True

    def remove_placeholder(self):
        # Если был вставлен какой-то символ в начало, удаляем не весь текст, а только placeholder:
        text = self.get()[:-len(self.placeholder)]
        self.delete('0', 'end')
        self['fg'] = self.default_fg_color
        self.insert(0, text)
        self.placeholder_on = False

    def reset_cursor(self, *args): #сброс курсора
        if self.placeholder_on:
            self.icursor(0)

#класс базы данных
class DB():
    def __init__(self): # инициализация и создание бд
        self.conn = sqlite3.connect('Employee.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS Employee (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT,
            wages TEXT
            )"""
        )
        self.conn.commit()

    
    def insert_data(self,name,phone,email,wages): # звставка значений
        self.cur.execute("""INSERT INTO Employee(name,phone,email,wages) VALUES(?,?,?,?)""",
                         (name,phone,email,wages))
        self.conn.commit()
    
#Запуск
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников')
    root.geometry('700x460')
    root.resizable(False,False)
    entry = EntrySearch(root, 'Введите ФИО и нажмите на \U0001F50D')
    entry.place(x=250,y=430,width=200)
    root.mainloop()