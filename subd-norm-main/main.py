from tkinter import *
from tkinter import ttk
import backend as back
from sqlite3 import *

#  Главное окно
window = Tk()
window.title('subd')
window.minsize(700, 450)

frame_change = Frame(window, width=150, height=150, bg='white')  # блок для функционала субд
frame_view = Frame(window, width=150, height=150, bg='white')  # блок для просмотра базы данных
frame_change.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_view.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)



# порядок элементов
heads = ['id', 'name', 'expenses']
table = ttk.Treeview(frame_view, show='headings')  # дерево выполняющее свойство таблицы
table['columns'] = heads  # длина таблицы

# заголовки столбцов и их расположение
for header in heads:
    table.heading(header, text=header, anchor='center')
    table.column(header, anchor='center')

# добавление из бд в таблицу приложения
for row in back.information():
    table.insert('', END, values=row)
table.pack(expand=YES, fill=BOTH, side=LEFT)

# функция добавления новых записей
def form_submit():
    name = f_name.get()
    expenses = f_expenses.get()
    insert_inf = (name, expenses)
    with connect('database.db') as db:
        cursor = db.cursor()
        query = """ INSERT INTO table1(name, expenses) VALUES (?, ?)"""
        cursor.execute(query, insert_inf)
        db.commit()
        refresh()

# функция обновления таблицы
def refresh():
    with connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(''' SELECT * FROM table1 ''')
        [table.delete(i) for i in
        table.get_children()]
        [table.insert('', 'end', values=row) for row in cursor.fetchall()]
# кнопка удалить и её функционал
f_delete = ttk.Entry(frame_change)
f_delete.grid(row=2, column=1, sticky='w', padx=10, pady=10)

def delete_user():
    with connect('database.db') as db:
        cursor = db.cursor()
        id = id_sel
        cursor.execute('''DELETE FROM table1 WHERE id = ?''', (id,))
        db.commit()
        refresh()

btn_delete = ttk.Button(frame_change, text="Удалить", command=delete_user)
btn_delete.grid(row=2, column=3, columnspan=2, sticky='w', padx=10, pady=10)



def on_select(event):
    global id_sel
    global set_col
    id_sel = table.item(table.focus())
    id_sel = id_sel.get('values')[0]
    col = table.identify_column(event.x)
    set_col = table.column(col)
    set_col = set_col.get('id')

table.bind('<ButtonRelease-1>', on_select)

def changeDB():
    with connect('database.db') as db:
        cursor = db.cursor()
        id = id_sel
        whatchange = f_change.get()
        if set_col != 'id':
            cursor.execute("""Update table1 set""" + ' ' + set_col + """ = ? where id = ? """, (whatchange, id))
            db.commit()
            refresh()

# функция создания таблицы

def create_table():
    with connect('database.db') as db:
        def add_table():
            global heads
            def add():
                global heads
                heads += E_newcreate.get()
                print(len(heads))
                if len(heads) >= n:
                    red.destroy()
                    table = ttk.Treeview(frame_view, show='headings')  # дерево выполняющее свойство таблицы
                    table['columns'] = heads
                    for header in heads:
                            table.heading(header, text=header, anchor='center')
                            table.column(header, anchor='center')
                    for row in back.information():
                        table.insert('', END, values=row)
                        table.pack(expand=YES, fill=BOTH, side=LEFT)
                    cursor = db.cursor()
                    cursor.execute(""" CREATE TABLE IF NOT EXISTS name(heads)""")
            n=int(E_create.get())
            name=N_create.get()
            menu.destroy()
            New = Tk()
            New.title(name)
            New.minsize(700, 450)
            frame_new_change = Frame(New, width=150, height=150, bg='white')  # блок для функционала субд
            frame_new_view = Frame(New, width=150, height=150, bg='white')  # блок для просмотра базы данных
            frame_new_change.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame_new_view.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)
            red=Tk()
            red.title('red')
            red.minsize(300, 300)
            f_r = Frame(red, width=100, height=100, bg='white')
            f_r.place(relx=0, rely=0, relwidth=1, relheight=1)
            l_newcreate = ttk.Label(f_r, text="Название столбца")
            l_newcreate.grid(row=0, column=0, sticky='w', padx=10, pady=10)
            E_newcreate=ttk.Entry(f_r)  
            E_newcreate.grid(row=0, column=1, sticky='w', padx=10, pady=10)
            Add = ttk.Button(f_r, text="Добавить", command=add)
            Add.grid(row=2, column=0,columnspan = 2, sticky='w', padx=10, pady=10)
            heads = []
            
            
        menu=Tk()
        menu.title('create')
        menu.minsize(300, 300)
        frame_create = Frame(menu, width=100, height=100, bg='white')
        frame_create.place(relx=0, rely=0, relwidth=1, relheight=1)
        l_create = ttk.Label(frame_create, text="Сколько столбцов?")
        l_create.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        E_create=ttk.Entry(frame_create)  
        E_create.grid(row=0, column=1, sticky='w', padx=10, pady=10)
        l_namecreate = ttk.Label(frame_create, text="Название таблицы")
        l_namecreate.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        N_create = ttk.Entry(frame_create)
        N_create.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        Add = ttk.Button(frame_create, text="Добавить", command=add_table)
        Add.grid(row=2, column=0,columnspan = 2, sticky='w', padx=10, pady=10)
                

# кнопки и label добавления новых записей
l_name = ttk.Label(frame_change, text="Имя")
f_name = ttk.Entry(frame_change)
l_index = ttk.Label(frame_change, text="Индекс")
#здесь по идее должен быть f_index но вместо него мы используем f_delete
l_change = ttk.Label(frame_change, text="Заменить на:")
f_change = ttk.Entry(frame_change) #entry на что меняем прошлое имя в бд
l_expenses = ttk.Label(frame_change, text="Платеж")
f_expenses = ttk.Entry(frame_change)
btn_submit = ttk.Button(frame_change, text="Добавить", command=form_submit)

but_change = ttk.Button(frame_change, text='Изменить', command=changeDB)
btn_reference = ttk.Button(frame_change, text="Справка", command=back.show_info)
# расположение кнопок и label добавления новых записей
l_name.grid(row=0, column=0, sticky='w', padx=10, pady=10)
f_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)
l_expenses.grid(row=1, column=0, sticky='w', padx=10, pady=10)
f_expenses.grid(row=1, column=1, sticky='w', padx=10, pady=10)
l_index.grid(row=2, column=0, sticky='w', padx=10, pady=10)
l_change.grid(row=3, column=0, sticky='w', padx=10, pady=10)
f_change.grid(row=3, column=1, sticky='w', padx=10, pady=10)
#здесь по идее должен быть entry index но вместо него используем f_delete
btn_submit.grid(row=0, column=3, columnspan=2, sticky='w', padx=10, pady=10)
but_change.grid(row=3, column=3, columnspan=2, sticky='w', padx=10, pady=10)
btn_reference.grid(row=4, column=0, sticky='w', padx=10, pady=10)
#Кнопка созданиятаблицы
create_new_table=ttk.Button(frame_change, text='Создать таблицу', command=create_table)
create_new_table.grid(row=1, column = 2, columnspan=2,sticky='w', padx=10, pady=10)
#скроллбар
scrollpanel = ttk.Scrollbar(frame_view, command=table.yview)
table.configure(yscrollcommand=scrollpanel.set)
scrollpanel.pack(side=RIGHT, fill=Y)
table.pack(expand=YES, fill=BOTH)





window.mainloop()
