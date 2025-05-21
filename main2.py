import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calculate_cost():
    try:
        connection_type = connection_type_var.get()
        distance = float(distance_entry.get())
        
        base_price = 1000
        
        if connection_type == "Стандарт":
            multiplier = 1.0
        elif connection_type == "Премиум":
            multiplier = 1.5
        else:
            multiplier = 1.0  # значение по умолчанию

        cost = base_price + (distance * 20 * multiplier)
        result_label.config(text=f"Итоговая стоимость: {cost:.2f} руб.")
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректное число в поле 'Расстояние'.")

# Создание окна
root = tk.Tk()
root.title("Калькулятор стоимости подключения")
root.geometry("400x250")
root.resizable(False, False)

# Тип подключения
tk.Label(root, text="Тип подключения:").pack(pady=5)
connection_type_var = tk.StringVar()
connection_type_combobox = ttk.Combobox(root, textvariable=connection_type_var)
connection_type_combobox['values'] = ("Стандарт", "Премиум")
connection_type_combobox.current(0)
connection_type_combobox.pack(pady=5)

# Расстояние
tk.Label(root, text="Расстояние до точки подключения (м):").pack(pady=5)
distance_entry = tk.Entry(root)
distance_entry.pack(pady=5)

# Кнопка расчета
calc_button = tk.Button(root, text="Рассчитать", command=calculate_cost)
calc_button.pack(pady=10)

# Вывод результата
result_label = tk.Label(root, text="Итоговая стоимость: ...")
result_label.pack(pady=10)

# Запуск приложения
root.mainloop()
