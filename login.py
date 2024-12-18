import customtkinter as cstk
import pypyodbc as pyodbc 
import tkinter

# Параметры подключения
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'VITSIRYK-LAPTOP'
DATABSE_NAME = 'TestDb'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABSE_NAME};
    Trust_Connection=yes;
"""

# Настройка CustomTkinter
cstk.set_appearance_mode("system")
cstk.set_default_color_theme("blue")

app = cstk.CTk()
app.geometry("500x500")
app.title("Create Table")

# Поля ввода
entry_table_name = cstk.CTkEntry(app, placeholder_text="Table name", width=190)
entry_table_name.place(relx=0.1, rely=0.1)

entry_column1_name = cstk.CTkEntry(app, placeholder_text="Column_1", width=190)
entry_column1_name.place(relx=0.1, rely=0.2)

entry_column2_name = cstk.CTkEntry(app, placeholder_text="Column_2", width=190)
entry_column2_name.place(relx=0.1, rely=0.3)

entry_column3_name = cstk.CTkEntry(app, placeholder_text="Column_3", width=190)
entry_column3_name.place(relx=0.1, rely=0.4)

# Переменные для выбора типа данных
radio_var_coll1 = tkinter.StringVar(value="varchar(50)")
radio_var_coll2 = tkinter.StringVar(value="varchar(50)")
radio_var_coll3 = tkinter.StringVar(value="varchar(50)")

# Функция создания таблицы
def create():
    connection = None
    try:
        connection = pyodbc.connect(connection_string)
        sql_stmt = f"""
        CREATE TABLE {entry_table_name.get()} (
            {entry_column1_name.get()} {radio_var_coll1.get()},
            {entry_column2_name.get()} {radio_var_coll2.get()},
            {entry_column3_name.get()} {radio_var_coll3.get()}
        )
        """
        cursor = connection.cursor()
        cursor.execute(sql_stmt)
        connection.commit()  # Явное завершение транзакции
        info_label.configure(text="Table created successfully")
    except pyodbc.Error as ex:
        print('Connection failed', ex)
        info_label.configure(text=f"Error: {ex}")
    finally:
        if connection:
            try:
                connection.close()  # Закрытие соединения
            except pyodbc.Error as close_ex:
                print("Error closing connection:", close_ex)


# Кнопка создания таблицы
create_button = cstk.CTkButton(app, text="Create", command=create)
create_button.place(relx=0.1, rely=0.5)

# Радиокнопки для Column 1
cstk.CTkLabel(app, text="Column 1 Type:").place(relx=0.5, rely=0.15)
cstk.CTkRadioButton(app, text="varchar(50)", variable=radio_var_coll1, value="varchar(50)").place(relx=0.5, rely=0.2)
cstk.CTkRadioButton(app, text="integer", variable=radio_var_coll1, value="integer").place(relx=0.7, rely=0.2)

# Радиокнопки для Column 2
cstk.CTkLabel(app, text="Column 2 Type:").place(relx=0.5, rely=0.25)
cstk.CTkRadioButton(app, text="varchar(50)", variable=radio_var_coll2, value="varchar(50)").place(relx=0.5, rely=0.3)
cstk.CTkRadioButton(app, text="integer", variable=radio_var_coll2, value="integer").place(relx=0.7, rely=0.3)

# Радиокнопки для Column 3
cstk.CTkLabel(app, text="Column 3 Type:").place(relx=0.5, rely=0.35)
cstk.CTkRadioButton(app, text="varchar(50)", variable=radio_var_coll3, value="varchar(50)").place(relx=0.5, rely=0.4)
cstk.CTkRadioButton(app, text="integer", variable=radio_var_coll3, value="integer").place(relx=0.7, rely=0.4)

# Метка для логов
info_label = cstk.CTkLabel(app, text="Log output")
info_label.place(relx=0.1, rely=0.6)

app.mainloop()