import customtkinter as cstk
import pypyodbc as pyodbc
import tkinter
from datetime import datetime

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

# Функция регистрации
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        info_label.configure(text="Введіть ім'я користувача")
        return
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Проверка существования пользователя
        cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            info_label.configure(text="Користувач з таким ім'ям вже існує")
            return

        # Добавление пользователя
        registration_date = datetime.now().date()
        registration_time = datetime.now()
        cursor.execute(
            """
            INSERT INTO Users (username, password, registration_date, registration_time)
            VALUES (?, ?, ?, ?)
            """,
            (username, password, registration_date, registration_time)
        )
        connection.commit()
        info_label.configure(text="Реєстрація успішна")
    except pyodbc.Error as ex:
        info_label.configure(text=f"Помилка: {ex}")
    finally:
        if 'connection' in locals():
            connection.close()


# Функция авторизации
def login_user():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        info_label.configure(text="Введіть ім'я користувача та пароль")
        return
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Проверка имени пользователя и пароля
        cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ? AND password = ?", (username, password))
        if cursor.fetchone()[0] == 1:
            info_label.configure(text="Ви увійшли в систему")
        else:
            info_label.configure(text="Невірно вказані дані")
    except pyodbc.Error as ex:
        info_label.configure(text=f"Помилка: {ex}")
    finally:
        if 'connection' in locals():
            connection.close()


# Настройка интерфейса
cstk.set_appearance_mode("system")
cstk.set_default_color_theme("blue")

app = cstk.CTk()
app.geometry("400x300")
app.title("Login/Register")

# Поля ввода
entry_username = cstk.CTkEntry(app, placeholder_text="Ім'я користувача", width=200)
entry_username.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

entry_password = cstk.CTkEntry(app, placeholder_text="Пароль", width=200, show="*")
entry_password.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

# Кнопки
register_button = cstk.CTkButton(app, text="Реєстрація", command=register_user)
register_button.place(relx=0.3, rely=0.6, anchor=tkinter.CENTER)

login_button = cstk.CTkButton(app, text="Вхід", command=login_user)
login_button.place(relx=0.7, rely=0.6, anchor=tkinter.CENTER)

# Лог информации
info_label = cstk.CTkLabel(app, text="Введіть дані")
info_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

app.mainloop()
