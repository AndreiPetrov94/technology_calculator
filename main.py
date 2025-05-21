import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Калькулятор расчета стоимости по ТП")
root.geometry("950x700")
root.resizable(True, True)

# Заголовок
tk.Label(
    root,
    text="Калькулятор расчета стоимости по ТП",
    font=("Arial", 16),
    bg="#d8f3dc",
    padx=10,
    pady=10
).pack(fill='x')

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill='both', expand=True)

# Ввод названия заявки и ТП
# tk.Label(main_frame, text="Наименование заявки:", font=("Arial", 12)).grid(row=0, column=0, sticky='w')
# tk.Entry(main_frame, width=30, font=("Arial", 12)).grid(row=0, column=1, pady=5, sticky='w')

# tk.Label(main_frame, text="Заявка ТП:", font=("Arial", 12)).grid(row=1, column=0, sticky='w')
# tk.Entry(main_frame, width=30, font=("Arial", 12)).grid(row=1, column=1, pady=5, sticky='w')


top_fields = [
    ("Наименование заявителя:", tk.StringVar()),
    ("Номер заявки ТП:", tk.StringVar()),
    ("Дата заявки ТП:", tk.StringVar())
]

# Хранилище переменных для верхних полей
top_field_vars = {}

# Создание меток и полей ввода в цикле
for i, (label_text, var) in enumerate(top_fields):
    tk.Label(main_frame, text=label_text, font=("Arial", 12)).grid(row=i, column=0, sticky='w')
    tk.Entry(main_frame, textvariable=var, width=30, font=("Arial", 12)).grid(row=i, column=1, pady=5, sticky='w')
    top_field_vars[i] = var

tk.Label(main_frame, text="Информация для расчета стоимости по ТП", font=("Arial", 14)).grid(row=3, column=0, columnspan=2, sticky='s', pady=10)

# Описание полей
field_config = {
    0: {"label": "Тип Заявителя", "type": "combobox", "values": ["Физическое лицо", "Юридическое лицо", "Индивидуальный предприниматель"]},
    1: {"label": "Расположение", "type": "combobox", "values": ["Город", "Поселок городского типа", "Сельская местность"]},
    2: {"label": "Ранее присоединенная мощность, кВт", "type": "float_entry"},
    3: {"label": "Присоединяемая мощность, кВт", "type": "float_entry"},
    4: {"label": "Максимальная мощность, кВт", "type": "readonly"},
    5: {"label": "Категория присоединения", "type": "readonly"},
    6: {"label": "Напряжение", "type": "combobox", "values": ["0,4 кВ и ниже", "1-20 кВ"]},
    7: {"label": "Категория надежности", "type": "combobox", "values": ["I", "II", "III"]},
    8: {"label": "Расстояние от границ участка заявителя до ближайшего объекта СО", "type": "combobox", "values": ["менее 300", "более 300"]},
    9: {"label": "Льготная группа заявителей (861 постановление п.17 абзацы 11-19)", "type": "combobox", "values": ["да", "нет"]},
    10: {"label": "Выбор ставки C1.2.1 - выдача уведомления / C1.2.2 - проверку выполнения ТУ", "type": "combobox", "values": ["C1.2.1 - выдача уведомления", "C1.2.2 - проверку выполнения ТУ"]}
}

# Хранилище переменных
field_vars = {}

# Валидация float
def validate_float(P):
    if P == "":
        return True
    try:
        val = float(P)
        return 0 <= val <= 32000
    except:
        return False

vcmd = (root.register(validate_float), "%P")

# Переменные с формулами
power_prev = tk.StringVar()
power_new = tk.StringVar()
power_total = tk.StringVar(value="0.00")
category_result = tk.StringVar(value="")

# Автоматическое обновление полей
def update_calculations(*args):
    try:
        prev = float(power_prev.get())
    except:
        prev = 0
    try:
        new = float(power_new.get())
    except:
        new = 0
    total = prev + new
    power_total.set(f"{total:.2f}")

    if total <= 15:
        category_result.set("до 15 кВт")
    elif total <= 150:
        category_result.set("от 15 до 150 кВт")
    else:
        category_result.set("свыше 150 кВт")

power_prev.trace_add("write", update_calculations)
power_new.trace_add("write", update_calculations)

# Создание полей на форме
for i, config in field_config.items():
    tk.Label(
        main_frame,
        text=f"{i+1}. {config['label']}",
        font=("Arial", 12),
        anchor='w',
        width=70
        ).grid(
            row=i+4,
            column=0,
            sticky='w',
            pady=5
        )

    if config["type"] == "combobox":
        var = tk.StringVar()
        cb = ttk.Combobox(
            main_frame,
            font=("Arial", 12),
            width=30,
            values=config["values"],
            textvariable=var
        )
        cb.grid(row=i+4, column=1, sticky='w')
        field_vars[i] = var

    elif config["type"] == "float_entry":
        var = power_prev if i == 2 else power_new
        entry = tk.Entry(
            main_frame,
            font=("Arial", 12),
            width=30,
            textvariable=var,
            validate="key",
            validatecommand=vcmd
        )
        entry.grid(row=i+4, column=1, sticky='w')
        field_vars[i] = var

    elif config["type"] == "readonly":
        var = power_total if i == 4 else category_result
        entry = tk.Entry(
            main_frame,
            font=("Arial", 12),
            width=30,
            textvariable=var,
            state='readonly'
        )
        entry.grid(row=i+4, column=1, sticky='w')
        field_vars[i] = var

root.mainloop()
