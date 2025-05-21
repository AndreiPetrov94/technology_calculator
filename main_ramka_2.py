import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Калькулятор расчета стоимости по ТП")
root.geometry("950x700")

# --- Создаем контейнер для canvas и вертикального скроллбара ---
container = tk.Frame(root)
container.pack(fill='both', expand=True)

canvas = tk.Canvas(container)
canvas.pack(side='left', fill='both', expand=True)

v_scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
v_scrollbar.pack(side='right', fill='y')

# Горизонтальный скроллбар внизу окна
h_scrollbar = tk.Scrollbar(root, orient='horizontal', command=canvas.xview)
h_scrollbar.pack(side='bottom', fill='x')

canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Создаем frame, в котором будет весь интерфейс
main_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=main_frame, anchor='nw')

# Обновляем scrollregion при изменении размера main_frame
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

main_frame.bind("<Configure>", on_frame_configure)

# --- Здесь начинается твой исходный интерфейс, только теперь в main_frame ---

# Заголовок
tk.Label(
    main_frame,
    text="Калькулятор расчета стоимости по ТП",
    font=("Arial", 16, "bold"),
    bg="#d8f3dc",
    padx=10,
    pady=10,
    anchor='center'
).pack(fill='x')


# Используем отдельный фрейм для содержимого под заголовком
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
    entry = create_cell(content_frame, tk.Entry, i, 1, textvariable=var, font=("Arial", 12), width=30)
    top_field_vars[i] = var

# Заголовок таблицы с расчетом стоимости
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

# --- Таблица: С3 Кабельные линии электропередачи ---

table_title = tk.Label(
    content_frame,
    text="С3 Кабельные линии электропередачи",
    font=("Arial", 14, "bold")
)
table_title.grid(row=100, column=0, columnspan=8, pady=(20, 10), sticky='nsew')

columns = [
    "№ п/п", "Напряжение, кВ", "Сечение, мм²", "Изоляция", "Количество КЛ в траншее/блоках/каналах",
    "Наименование мероприятия", "Стоимость ставки, руб./км",
    "Длина, км", "Стоимость без НДС, руб", "Стоимость с НДС, руб"
]

for col, name in enumerate(columns):
    header = tk.Label(content_frame, text=name, font=("Arial", 10, "bold"),
                      borderwidth=1, relief="solid")
    header.grid(row=101, column=col, sticky='nsew', padx=1, pady=1)

table_rows = []

def add_table_row():
    row_index = 102 + len(table_rows)
    row_widgets = []

    for col in range(len(columns)):
        entry = tk.Entry(content_frame, font=("Arial", 10),
                         relief="solid", borderwidth=1)
        entry.grid(row=row_index, column=col, sticky='nsew', padx=1, pady=1)
        row_widgets.append(entry)

    table_rows.append(row_widgets)
    draw_totals()

def draw_totals():
    total_row = 102 + len(table_rows)
    tk.Label(content_frame, text="ИТОГО", font=("Arial", 10, "bold"),
             borderwidth=1, relief="solid").grid(row=total_row, column=0, columnspan=5, sticky='nsew', padx=1, pady=1)

    for col in range(5, 8):
        entry = tk.Entry(content_frame, font=("Arial", 10, "bold"),
                         relief="solid", borderwidth=1)
        entry.insert(0, "0,00")
        entry.grid(row=total_row, column=col, sticky='nsew', padx=1, pady=1)

add_row_button = tk.Button(content_frame, text="+", font=("Arial", 12, "bold"),
                           command=add_table_row)
add_row_button.grid(row=105, column=0, pady=(10, 0), sticky='w')

for _ in range(2):
    add_table_row()

root.mainloop()
