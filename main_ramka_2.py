import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

root = tk.Tk()
root.title("Калькулятор расчета стоимости по ТП")
root.geometry("950x900")

tk.Label(
    root,
    text="Калькулятор расчета стоимости по ТП",
    font=("Arial", 16, "bold"),
    bg="#d8f3dc",
    padx=10,
    pady=10,
    anchor='center'
).pack(fill='x')

# --- Создаем контейнер для canvas и вертикального скроллбара ---
container = tk.Frame(root)
container.pack(fill='both', expand=True)

canvas = tk.Canvas(container)
canvas.pack(side='left', fill='both', expand=True)

v_scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
v_scrollbar.pack(side='right', fill='y')

h_scrollbar = tk.Scrollbar(root, orient='horizontal', command=canvas.xview)
h_scrollbar.pack(side='bottom', fill='x')

canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

main_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=main_frame, anchor='nw')

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

main_frame.bind("<Configure>", on_frame_configure)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

content_frame = tk.Frame(main_frame, padx=10, pady=10)
content_frame.pack(fill='both', expand=True)

top_fields = [
    ("Наименование заявителя:", tk.StringVar()),
    ("Номер заявки ТП:", tk.StringVar()),
    ("Дата заявки ТП:", tk.StringVar())
]

top_field_vars = {}

def create_cell(parent, widget_class, row, column, **kwargs):
    frame = tk.Frame(parent, highlightbackground="black", highlightthickness=1)
    frame.grid(row=row, column=column, sticky='nsew', padx=3, pady=3)
    widget = widget_class(frame, **kwargs)
    widget.pack(fill='both', expand=True)
    return widget

# Верхние поля
for i, (label_text, var) in enumerate(top_fields):
    create_cell(content_frame, tk.Label, i, 0, text=label_text, font=("Arial", 12), anchor='w')

    if label_text == "Дата заявки ТП:":
        entry = create_cell(
            content_frame, DateEntry, i, 1,
            textvariable=var,
            font=("Arial", 12),
            width=28,
            date_pattern='dd.mm.yyyy',
            locale='ru_RU'
        )
    else:
        entry = create_cell(content_frame, tk.Entry, i, 1, textvariable=var, font=("Arial", 12), width=30)

    top_field_vars[i] = var

tk.Label(content_frame, text="Информация для расчета стоимости по ТП", font=("Arial", 14, "bold")).grid(
    row=3, column=0, columnspan=2, sticky='s', pady=10
)

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

field_vars = {}
power_prev = tk.StringVar()
power_new = tk.StringVar()
power_total = tk.StringVar(value="0.00")
category_result = tk.StringVar(value="")

def validate_float(P):
    if P == "":
        return True
    try:
        val = float(P)
        return 0 <= val <= 32000
    except:
        return False

vcmd = (root.register(validate_float), "%P")

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

for i, config in field_config.items():
    row = i + 4
    create_cell(content_frame, tk.Label, row, 0, text=f"{i+1}. {config['label']}", font=("Arial", 12), anchor='w')

    if config["type"] == "combobox":
        var = tk.StringVar()
        cb = create_cell(content_frame, ttk.Combobox, row, 1, font=("Arial", 12), width=30, values=config["values"], textvariable=var)
        field_vars[i] = var

    elif config["type"] == "float_entry":
        var = power_prev if i == 2 else power_new
        entry = create_cell(content_frame, tk.Entry, row, 1, font=("Arial", 12), width=30, textvariable=var, validate="key", validatecommand=vcmd)
        field_vars[i] = var

    elif config["type"] == "readonly":
        var = power_total if i == 4 else category_result
        entry = create_cell(content_frame, tk.Entry, row, 1, font=("Arial", 12), width=30, textvariable=var, state='readonly')
        field_vars[i] = var

# Добавляем таблицу для расчета стоимости по КЛ
kl_label = tk.Label(content_frame, text="Расчет стоимости по КЛ", font=("Arial", 14, "bold"))
kl_label.grid(row=15, column=0, columnspan=2, pady=20)

kl_frame = tk.Frame(content_frame)
kl_frame.grid(row=16, column=0, columnspan=2, sticky='nsew')

kl_headers = [
    "№ п/п", "Напряжение, кВ", "Сечение, мм²", "Изоляция",
    "Кол-во КЛ в тр-не/блоках/каналах", "Наименование мероприятия",
    "Ставка, руб/км", "Длина, км", "Стоимость без НДС, руб", "Стоимость с НДС, руб"
]

for col, header in enumerate(kl_headers):
    tk.Label(kl_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padx=5, pady=2).grid(row=0, column=col, sticky='nsew')

kl_entry_vars = []

for row in range(1, 6):
    row_vars = []
    for col in range(len(kl_headers)):
        if col == 0:
            tk.Label(kl_frame, text=str(row), borderwidth=1, relief="solid", width=5).grid(row=row, column=col, sticky='nsew')
        else:
            var = tk.StringVar()
            entry = tk.Entry(kl_frame, textvariable=var, width=18, borderwidth=1, relief="solid")
            entry.grid(row=row, column=col, sticky='nsew')
            row_vars.append(var)
    kl_entry_vars.append(row_vars)

for col in range(len(kl_headers)):
    if col == 0:
        tk.Label(kl_frame, text="", borderwidth=1, relief="solid").grid(row=6, column=col, sticky='nsew')
    elif col == 5:
        tk.Label(kl_frame, text="ИТОГО", font=("Arial", 10, "bold"), borderwidth=1, relief="solid").grid(row=6, column=col, sticky='nsew')
    elif col == 7:
        length_total = tk.StringVar(value="0.000")
        tk.Entry(kl_frame, textvariable=length_total, state='readonly', borderwidth=1, relief="solid").grid(row=6, column=col, sticky='nsew')
    elif col == 8:
        sum_wo_vat = tk.StringVar(value="0.00")
        tk.Entry(kl_frame, textvariable=sum_wo_vat, state='readonly', borderwidth=1, relief="solid").grid(row=6, column=col, sticky='nsew')
    elif col == 9:
        sum_with_vat = tk.StringVar(value="0.00")
        tk.Entry(kl_frame, textvariable=sum_with_vat, state='readonly', borderwidth=1, relief="solid").grid(row=6, column=col, sticky='nsew')
    else:
        tk.Label(kl_frame, text="", borderwidth=1, relief="solid").grid(row=6, column=col, sticky='nsew')

root.mainloop()
