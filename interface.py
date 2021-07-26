def get_data_in_table():
    value1 = url.get()
    value2 = cost_price.get()
    value3 = money.get()
    value4 = description.get()

    if value1 and value2 and value3 and value4:
        add_new_product(value1, value2, value3, value4)
    elif value1 and value2 and value3:
        add_new_product(value1, value2, value3, 'Нет описания ')
    else:
        print('Нужные поля не заполнены. Заполните все поля')

def start():
    open_data_base()

#удалять url будет
def del_data_in_table():
    value_del = del_url.get()
    valid = 'https://www.wildberries.ru'
    if valid in value_del:
        delete_product(value_del)
        print('Товар удалён')
    else:
        print('Поле заполнено неправильно')
    
def show_data_base_gui():
    show_data_base()


from main_script import *
import tkinter as tk
import threading

win = tk.Tk()
win.title('Ma&eR')
win.geometry('550x550')
win.resizable(False, False)


######### 
url_label = tk.Label(text='Ссылка на товар: ')
cost_price_label = tk.Label(text='Цена покупки (от и ниже): ')
money_label = tk.Label(text='Сумма: ')
description_label = tk.Label(text='Описание товара: ')

url_label.grid(row=0, column=0, sticky='w')
cost_price_label.grid(row=1, column=0, sticky='w')
money_label.grid(row=2, column=0, sticky='w')
description_label.grid(row=3, column=0, sticky='w')

url = tk.Entry(win)
cost_price = tk.Entry(win)
money = tk.Entry(win)
description = tk.Entry(win)
########



url.grid(row=0, column=1)
cost_price.grid(row=1, column=1)
money.grid(row=2, column=1)
description.grid(row=3, column=1)

del_url = tk.Entry(win)
Label_del_url = tk.Label(text='Удалить товар: ')

Label_del_url.grid(row=0, column=4)
del_url.grid(row = 0, column=5)
tk.Button(win, text='Удалить товар', command=del_data_in_table).grid(row=1, column=5)

Label_version = tk.Label(text = 'version: Beta')
Label_version.grid(row=100, column=0)


tk.Button(win, text='Показать базу данных', command = show_data_base).grid(row=5, column=5)
path = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'server.db')
path2 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'cockies')
path3 = Path(pathlib.Path.home(), 'Рабочий стол','бот 1.1', 'MaeR_.ico')

debug = r'G:\python_progs\бот wildberries\icon.ico'


win.iconbitmap(path3)
tk.Button(win, text='Добавить', command=get_data_in_table).grid(row=4, column=0)
start_program = tk.Button(win, text = 'Запуск', command=lambda: threading.Thread(target=start, daemon=True).start())
start_program.grid(row=7, column=0)
win.mainloop()

