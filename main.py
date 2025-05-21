import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Калькулятор расчета стоимости по ТП")
root.geometry("950x700")
root.resizable(True, True)

# ---------- Переменные ----------
power_prev_var = tk.StringVar()
power_new_var = tk.StringVar()
max_power_var = tk.StringVar(value="0.00")
category_var = tk.StringVar(value="")  # Поле 5 (Категория присоединения)

# ---------- Валидация float от 0 до 32000 ----------
def validate_float(value):
    if value == "":
        return True
    try:
        val = float(value)
        return 0 <= val <= 32000
    except ValueError:
        return False

vcmd = (root.register(validate_float), '%P')

# ---------- Автообновление поля 4 и поля 5 ----------
def update_formula_and_category(*args):
    try:
        val1 = float(power_prev_var.get())
    except ValueError:
        val1 = 0
    try:
        val2 = float(power_new_var.get())
    except ValueError:
        val2 = 0
    total = val1 + val2
    max_power_var.set(f"{total:.2f}")

    # Логика для поля 5
    if total <= 15:
        category_var.set("до 15 кВт")
    elif total <= 150:
        category_var.set("от 15 до 150 кВт")
    else:
        category_var.set("свыше 150 кВт")

power_prev_var.trace_add("write", update_formula_and_category)
power_new_var.trace_add("write", update_formula_and_category)

# ---------- Заголовок ----------
tk.Label(root, text="Калькулятор расчета стоимости по ТП",
         font=("Arial", 16), bg="#d8f3dc", padx=10, pady=10).pack(fill='x')

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill='both', expand=True)

# ---------- Поля ввода сверху ----------
tk.Label(main_frame, text="Наименование заявки:", font=("Arial", 12)).grid(row=0, column=0, sticky='w')
tk.Entry(main_frame, width=30, font=("Arial", 12)).grid(row=0, column=1, columnspan=3, sticky='w', pady=5)

tk.Label(main_frame, text="Заявка ТП:", font=("Arial", 12)).grid(row=1, column=0, sticky='w')
tk.Entry(main_frame, width=30, font=("Arial", 12)).grid(row=1, column=1, columnspan=3, sticky='w', pady=5)

tk.Label(main_frame, text="Информация для расчета стоимости по ТП", font=("Arial", 12)).grid(row=2, column=0, sticky='n')

# ---------- Таблица ----------
fields = [
    "Заявитель",
    "Расположение",
    "Ранее присоединенная максимальная мощность, кВт",
    "Присоединяемая мощность, кВт",
    "Максимальная мощность, кВт",
    "Категория присоединения",
    "Напряжение",
    "Категория надежности",
    "Расстояние от границ участка заявителя до ближайшего объекта СО",
    "Льготная группа заявителей (861 постановление п.17 абзацы 11-19)",
    "Выбор ставки C1.2.1 - выдача уведомления / C1.2.2 - проверку выполнения ТУ"
]

input_widgets = []

for i, label in enumerate(fields):
    tk.Label(main_frame, width=70, text=f"{i+1}. {label}", anchor='w', font=("Arial", 12)).grid(row=i + 3, column=0, sticky='w', pady=5)

    if i == 0:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["Физическое лицо", "Юридическое лицо", "Индивидуальный предприниматель"])
    elif i == 1:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["Город", "Поселок городского типа", "Сельская местность"])
    elif i == 2:
        widget = tk.Entry(main_frame, width=30, font=("Arial", 12), textvariable=power_prev_var,
                          validate="key", validatecommand=vcmd)
    elif i == 3:
        widget = tk.Entry(main_frame, width=30, font=("Arial", 12), textvariable=power_new_var,
                          validate="key", validatecommand=vcmd)
    elif i == 4:
        widget = tk.Entry(main_frame, width=30, font=("Arial", 12), state="readonly", textvariable=max_power_var)
    elif i == 5:
        widget = tk.Entry(main_frame, width=30, font=("Arial", 12), state="readonly", textvariable=category_var)
    elif i == 6:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["0,4 кВ и ниже", "1-20 кВ"])
    elif i == 7:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["I", "II", "III"])
    elif i == 8:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["менее 300", "более 300"])
    elif i == 9:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["да", "нет"])
    elif i == 10:
        widget = ttk.Combobox(main_frame, width=30, font=("Arial", 12),
                              values=["C1.2.1 - выдача уведомления", "C1.2.2 - проверку выполнения ТУ"])
    else:
        widget = tk.Entry(main_frame, width=30, font=("Arial", 12), validate="key", validatecommand=vcmd)

    widget.grid(row=i + 3, column=1, sticky='w', pady=5)
    input_widgets.append(widget)

# ---------- Запуск ----------
root.mainloop()
