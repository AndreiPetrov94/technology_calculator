import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from constants import SCREEN_SIZE
from form_config_02 import (
    application_data,
    calculation_data,
    headers_dict,
    rates_dict
)
from scrollable_frame_2 import ScrollableFrame
from validators import validate_float, to_float, to_str


root = tk.Tk()
root.title("Калькулятор расчета стоимости по ТП")
root.geometry(SCREEN_SIZE)
root.iconbitmap("resources/logo_VVEK.ico")

tk.Label(
    root,
    text="Калькулятор расчета стоимости по ТП",
    font=("Arial", 20, "bold"),
    bg="#b7e4c7",
    padx=10,
    pady=10,
    anchor='center'
).pack(fill='x')

# Инициализация прокручиваемой области
scrollable = ScrollableFrame(root)
# Растянуть на всю доступную площадь
scrollable.pack(fill='both', expand=True)

# Внутренний фрейм для размещения контента
main_frame = scrollable.main_frame

# Контейнер с отступами для содержимого
content_frame = tk.Frame(main_frame, padx=10, pady=10)
content_frame.pack(fill='both', expand=True)
content_frame.grid_columnconfigure(0, weight=0)


# Универсальная функция для создания ячеек с рамкой
def create_cell(parent, widget_class, row, column, **kwargs):
    """
    Универсальная функция для создания ячейки с виджетом.
    Автоматически отключает прокрутку колесиком мыши у Combobox.
    """
    frame = tk.Frame(parent, highlightbackground="black", highlightthickness=1)
    frame.grid(row=row, column=column, sticky='w', padx=4, pady=4)
    widget = widget_class(frame, **kwargs)
    widget.pack(fill='x')

    # Отключаем прокрутку у Combobox (чтобы не переключались случайно)
    if isinstance(widget, ttk.Combobox):
        widget.bind("<MouseWheel>", lambda e: "break")

    return widget


# данные заявки
application_data_vars = {}

# Создаем верхние поля с соответствующими виджетами
for i, (key, config) in enumerate(application_data.items()):
    var = tk.StringVar()
    application_data_vars[key] = var

    create_cell(
        content_frame,
        tk.Label,
        i, 0,
        text=config["label"],
        font=("Arial", 12),
        width=60,
        anchor='w'
    )

    if config["type"] == "date":
        entry = create_cell(
            content_frame, DateEntry, i, 1,
            textvariable=var,
            font=("Arial", 12),
            width=28,
            date_pattern='dd.mm.yyyy',
            locale='ru_RU'
        )
    else:
        entry = create_cell(
            content_frame,
            tk.Entry,
            i, 1,
            textvariable=var,
            font=("Arial", 12),
            width=30
        )

# Заголовок Информация для расчета стоимости по ТП
tk.Label(
    content_frame,
    text="Информация для расчета стоимости по ТП",
    font=("Arial", 14, "bold")
).grid(
    row=4,
    column=0,
    columnspan=2,
    sticky='s',
    pady=5
)

calculation_data_vars = {}

power_prev = tk.StringVar()
power_new = tk.StringVar()
power_total = tk.StringVar(value="0,00")
category_result = tk.StringVar(value="")

vcmd = (root.register(validate_float), "%P")


# Автоматический пересчет суммарной мощности и категории
def update_calculations(*args):
    prev = to_float(power_prev.get())
    new = to_float(power_new.get())

    total = prev + new
    power_total.set(f"{total:.2f}".replace('.', ','))

    if total <= 15:
        category_result.set("до 15 кВт")
    elif total <= 150:
        category_result.set("от 15 до 150 кВт")
    else:
        category_result.set("свыше 150 кВт")


power_prev.trace_add("write", update_calculations)
power_new.trace_add("write", update_calculations)


# Создаем поля формы на основе конфигурации
for i, (key, config) in enumerate(calculation_data.items()):
    row = i + 5
    create_cell(
        content_frame,
        tk.Label,
        row, 0,
        text=f"{i+1}. {config['label']}",
        font=("Arial", 12),
        width=60,
        anchor='w'
    )

    # Определяем переменную
    if key == "power_prev":
        var = power_prev
    elif key == "power_new":
        var = power_new
    elif key == "power_total":
        var = power_total
    elif key == "category_result":
        var = category_result
    else:
        var = tk.StringVar()

    calculation_data_vars[key] = var  # сохраняем переменную

    # Создание виджета
    if config["type"] == "combobox":
        create_cell(
            content_frame,
            ttk.Combobox,
            row, 1,
            font=("Arial", 12),
            width=28,
            values=config["values"],
            textvariable=var, state="readonly"
        )

    elif config["type"] == "float_entry":
        create_cell(
            content_frame,
            tk.Entry,
            row, 1,
            font=("Arial", 12),
            width=30,
            textvariable=var, validate="key",
            validatecommand=vcmd
        )

    elif config["type"] == "readonly":
        create_cell(
            content_frame,
            tk.Entry,
            row, 1,
            font=("Arial", 12),
            width=30,
            textvariable=var,
            state='readonly'
        )

# ===========================
# Таблица С2 Воздушные линии электропередачи
# ===========================

# Заголовок таблицы
tk.Label(
    content_frame,
    text="С2 Воздушные линии электропередачи",
    font=("Arial", 14, "bold")
).grid(
    row=16,
    column=0,
    columnspan=2,
    pady=5
)

# Основной фрейм для таблицы
C2_frame = tk.Frame(content_frame)
C2_frame.grid(row=17, column=0, columnspan=2, sticky='nsew')

# Создаем заголовки таблицы
for col, header in enumerate(headers_dict["C2"]):
    tk.Label(
        C2_frame,
        text=header,
        font=("Arial", 10, "bold"),
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=2,
        justify='center'
    ).grid(
        row=0,
        column=col,
        sticky='nsew'
    )

vl_entry_vars = []  # список словарей с переменными строк
vl_total_widgets = []  # виджеты итоговой строки
next_vl_row = 1  # счетчик строк таблицы

# Переменные для итоговых значений (связываются с виджетами итоговой строки)
length_total_vl = tk.StringVar(value="0,00")
sum_wo_vat_vl = tk.StringVar(value="0,00")
sum_with_vat_vl = tk.StringVar(value="0,00")


def update_vl_totals():
    """
    Пересчитывает итоги по столбцам: длина, стоимость без НДС, стоимость с НДС.
    Обновляет переменные итоговой строки в таблице С2.
    """
    total_length = 0.0
    total_cost_wo_vat = 0.0
    total_cost_with_vat = 0.0

    for row_vars in vl_entry_vars:
        length = to_float(row_vars["length"].get())
        cost_wo_vat = to_float(row_vars["cost_wo_vat"].get())
        cost_with_vat = to_float(row_vars["cost_with_vat"].get())

        total_length += length
        total_cost_wo_vat += cost_wo_vat
        total_cost_with_vat += cost_with_vat

    length_total_vl.set(to_str(total_length, precision=2))
    sum_wo_vat_vl.set(to_str(total_cost_wo_vat, precision=2, grouping=True))
    sum_with_vat_vl.set(to_str(total_cost_with_vat, precision=2, grouping=True))


def draw_vl_totals():
    """
    Рисует итоговую строку в таблице, используя переменные итогов.
    Если итоговые виджеты уже созданы — удаляет их и рисует заново.
    """
    global vl_total_widgets
    for widget in vl_total_widgets:
        widget.destroy()
    vl_total_widgets.clear()

    total_row = next_vl_row  # строка под итог

    for col in range(len(headers_dict["C2"])):
        if col == 0:
            w = tk.Label(C2_frame, text="", borderwidth=1, relief="solid")
        elif col == 3:  # В столбце "Наименование мероприятия" пишем "ИТОГО"
            w = tk.Label(C2_frame, text="ИТОГО", font=("Arial", 10, "bold"), borderwidth=1, relief="solid")
        elif col == 5:
            w = tk.Entry(C2_frame, textvariable=length_total_vl, state='readonly', borderwidth=1, relief="solid", justify='center')
        elif col == 6:
            w = tk.Entry(C2_frame, textvariable=sum_wo_vat_vl, state='readonly', borderwidth=1, relief="solid", justify='center')
        elif col == 7:
            w = tk.Entry(C2_frame, textvariable=sum_with_vat_vl, state='readonly', borderwidth=1, relief="solid", justify='center')
        else:
            w = tk.Label(C2_frame, text="", borderwidth=1, relief="solid")
        w.grid(row=total_row, column=col, sticky='nsew')
        vl_total_widgets.append(w)

def add_vl_row():
    """
    Добавляет новую строку в таблицу.
    Создает виджеты и переменные для каждого столбца.
    Привязывает обработчики изменений для динамического пересчета стоимости и итогов.
    """
    global next_vl_row
    row = next_vl_row

    # Создаем переменные для ячеек строки
    row_vars = {
        "voltage": tk.StringVar(),
        "section": tk.StringVar(),
        "event": tk.StringVar(),
        "rate": tk.StringVar(),
        "length": tk.StringVar(),
        "cost_wo_vat": tk.StringVar(),
        "cost_with_vat": tk.StringVar()
    }

    # № п/п — просто метка с номером
    tk.Label(C2_frame, text=str(row), borderwidth=1, relief="solid", width=5).grid(row=row, column=0, sticky='nsew')

    # Напряжение — Combobox с выбором из ключей rates_dict["C2"]
    voltage_cb = ttk.Combobox(C2_frame, textvariable=row_vars["voltage"], state="readonly", width=15, justify='center')
    voltage_cb['values'] = list(rates_dict["C2"].keys())
    voltage_cb.grid(row=row, column=1, sticky='nsew')

    # Сечение — Combobox (будет заполняться в зависимости от напряжения)
    section_cb = ttk.Combobox(C2_frame, textvariable=row_vars["section"], state="readonly", width=20, justify='center')
    section_cb.grid(row=row, column=2, sticky='nsew')

    # Наименование мероприятия — OptionMenu, изначально пустое
    event_var = row_vars["event"]
    event_var.set('')  # по умолчанию пусто

    event_menu = tk.OptionMenu(C2_frame, event_var, '')
    event_menu.config(width=50, font=("Arial", 10), anchor='w')  # фиксируем ширину и шрифт
    event_menu.grid(row=row, column=3, sticky='nsew')

    # Ставка — Entry, только для чтения
    rate_entry = tk.Entry(C2_frame, textvariable=row_vars["rate"], state='readonly', justify='center', borderwidth=1, relief="solid")
    rate_entry.grid(row=row, column=4, sticky='nsew')

    # Длина — Entry, пользователь вводит
    length_entry = tk.Entry(
        C2_frame,
        textvariable=row_vars["length"],
        width=18,
        borderwidth=1,
        relief="solid",
        justify='center',
        validate='key',
        validatecommand=vcmd
    )
    length_entry.grid(row=row, column=5, sticky='nsew')

    # Стоимость без НДС — Entry, только для чтения
    cost_wo_vat_entry = tk.Entry(C2_frame, textvariable=row_vars["cost_wo_vat"], state='readonly', justify='center', borderwidth=1, relief="solid")
    cost_wo_vat_entry.grid(row=row, column=6, sticky='nsew')

    # Стоимость с НДС — Entry, только для чтения
    cost_with_vat_entry = tk.Entry(C2_frame, textvariable=row_vars["cost_with_vat"], state='readonly', justify='center', borderwidth=1, relief="solid")
    cost_with_vat_entry.grid(row=row, column=7, sticky='nsew')

    def on_voltage_change(event=None):
        voltage = row_vars["voltage"].get()
        # Обновляем список сечений в зависимости от напряжения
        sections = list(rates_dict["C2"].get(voltage, {}).keys())
        section_cb['values'] = sections
        row_vars["section"].set('')
        # Очистить мероприятия и ставки
        row_vars["event"].set('')
        row_vars["rate"].set('')
        row_vars["cost_wo_vat"].set('')
        row_vars["cost_with_vat"].set('')
        # Обновить меню мероприятий пустым
        event_menu['menu'].delete(0, 'end')

        update_vl_totals()

    def on_section_change(event=None):
        voltage = row_vars["voltage"].get()
        section = row_vars["section"].get()
        # Обновляем мероприятия в зависимости от напряжения и сечения
        events = list(rates_dict["C2"].get(voltage, {}).get(section, {}).keys())
        # Обновляем меню событий (OptionMenu)
        event_menu['menu'].delete(0, 'end')
        for ev in events:
            event_menu['menu'].add_command(label=ev, command=tk._setit(row_vars["event"], ev, on_event_selected))
        row_vars["event"].set('')
        row_vars["rate"].set('')
        row_vars["cost_wo_vat"].set('')
        row_vars["cost_with_vat"].set('')

        update_vl_totals()

    def on_event_selected(*args):
        """
        Вызывается при выборе наименования мероприятия.
        Устанавливает ставку, рассчитывает стоимость без НДС и с НДС.
        """
        voltage = row_vars["voltage"].get()
        section = row_vars["section"].get()
        event_name = row_vars["event"].get()

        if voltage and section and event_name:
            rate = rates_dict["C2"].get(voltage, {}).get(section, {}).get(event_name, 0)
            row_vars["rate"].set(to_str(rate, precision=2, grouping=True))

            length = to_float(row_vars["length"].get())
            cost_wo_vat = round(length * rate, 2)
            cost_with_vat = round(cost_wo_vat * 1.2, 2)

            row_vars["cost_wo_vat"].set(to_str(cost_wo_vat, precision=2, grouping=True))
            row_vars["cost_with_vat"].set(to_str(cost_with_vat, precision=2, grouping=True))
        else:
            row_vars["rate"].set('')
            row_vars["cost_wo_vat"].set('')
            row_vars["cost_with_vat"].set('')

        update_vl_totals()

    def on_length_change(*args):
        """
        Перерасчитывает стоимость при изменении длины.
        """
        length = to_float(row_vars["length"].get())
        rate = to_float(row_vars["rate"].get())

        cost_wo_vat = round(rate * length, 2)
        cost_with_vat = round(cost_wo_vat * 1.2, 2)

        row_vars["cost_wo_vat"].set(to_str(cost_wo_vat, precision=2, grouping=True))
        row_vars["cost_with_vat"].set(to_str(cost_with_vat, precision=2, grouping=True))

        update_vl_totals()

    # Привязываем обработчики
    voltage_cb.bind("<<ComboboxSelected>>", on_voltage_change)
    section_cb.bind("<<ComboboxSelected>>", on_section_change)
    row_vars["event"].trace_add("write", on_event_selected)
    row_vars["length"].trace_add("write", on_length_change)

    # Добавляем переменные текущей строки в общий список
    vl_entry_vars.append(row_vars)

    next_vl_row += 1
    draw_vl_totals()
    update_vl_totals()

def remove_vl_row():
    """
    Удаляет последнюю добавленную строку из таблицы и обновляет итоги.
    """
    global next_vl_row
    if next_vl_row > 1:
        next_vl_row -= 1
        # Удаляем виджеты строки из grid
        row_widgets = C2_frame.grid_slaves(row=next_vl_row)
        for widget in row_widgets:
            widget.destroy()
        # Удаляем переменные строки
        vl_entry_vars.pop()
        draw_vl_totals()
        update_vl_totals()

# Добавим две строки для примера
add_vl_row()

# Создадим кнопки для добавления и удаления строк
buttons_frame_vl = tk.Frame(content_frame)
buttons_frame_vl.grid(row=18, column=0, columnspan=2, sticky='w', pady=10)

add_btn_vl = tk.Button(buttons_frame_vl, text="Добавить воздушную линию", font=("Arial", 12, "bold"), command=add_vl_row, bg="#b7e4c7", width=30)
add_btn_vl.pack(side='left', padx=(0, 10))

remove_btn_vl = tk.Button(buttons_frame_vl, text="Удалить воздушную линию", font=("Arial", 12, "bold"), command=remove_vl_row, bg="#f8d7da", width=30)
remove_btn_vl.pack(side='left')


# ===========================
# Таблица С3_1 Кабельные линии в траншее
# ===========================
tk.Label(
    content_frame,
    text="С3_1 Кабельные линии в траншее",
    font=("Arial", 14, "bold")
).grid(
    row=19,
    column=0,
    columnspan=2,
    pady=5
)

C3_1_frame = tk.Frame(content_frame)
C3_1_frame.grid(row=20, column=0, columnspan=2, sticky='nsew')

for col, header in enumerate(headers_dict["C3_1"]):
    tk.Label(
        C3_1_frame,
        text=header,
        font=("Arial", 10, "bold"),
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=2,
        justify='center'
    ).grid(
        row=0,
        column=col,
        sticky='nsew'
    )

c31_entry_vars = []
c31_total_widgets = []
next_c31_row = 1

length_total_c31 = tk.StringVar(value="0,00")
sum_wo_vat_c31 = tk.StringVar(value="0,00")
sum_with_vat_c31 = tk.StringVar(value="0,00")

def update_c31_totals():
    total_length = 0.0
    total_cost_wo_vat = 0.0
    total_cost_with_vat = 0.0
    for row_vars in c31_entry_vars:
        length = to_float(row_vars["length"].get())
        cost_wo_vat = to_float(row_vars["cost_wo_vat"].get())
        cost_with_vat = to_float(row_vars["cost_with_vat"].get())
        total_length += length
        total_cost_wo_vat += cost_wo_vat
        total_cost_with_vat += cost_with_vat
    length_total_c31.set(to_str(total_length, precision=2))
    sum_wo_vat_c31.set(to_str(total_cost_wo_vat, precision=2, grouping=True))
    sum_with_vat_c31.set(to_str(total_cost_with_vat, precision=2, grouping=True))

def draw_c31_totals():
    global c31_total_widgets
    for widget in c31_total_widgets:
        widget.destroy()
    c31_total_widgets.clear()
    total_row = next_c31_row
    for col in range(len(headers_dict["C3_1"])):
        if col == 0:
            w = tk.Label(C3_1_frame, text="", borderwidth=1, relief="solid")
        elif col == 5:
            w = tk.Label(C3_1_frame, text="ИТОГО", font=("Arial", 10, "bold"), borderwidth=1, relief="solid")
        elif col == 7:
            w = tk.Entry(C3_1_frame, textvariable=length_total_c31, state='readonly', borderwidth=1, relief="solid", justify='center')
        elif col == 8:
            w = tk.Entry(C3_1_frame, textvariable=sum_wo_vat_c31, state='readonly', borderwidth=1, relief="solid", justify='center')
        elif col == 9:
            w = tk.Entry(C3_1_frame, textvariable=sum_with_vat_c31, state='readonly', borderwidth=1, relief="solid", justify='center')
        else:
            w = tk.Label(C3_1_frame, text="", borderwidth=1, relief="solid")
        w.grid(row=total_row, column=col, sticky='nsew')
        c31_total_widgets.append(w)

def add_c31_row():
    global next_c31_row
    row = next_c31_row
    row_vars = {
        "voltage": tk.StringVar(),
        "section": tk.StringVar(),
        "insulation": tk.StringVar(),
        "quantity": tk.StringVar(),
        "event": tk.StringVar(),
        "rate": tk.StringVar(),
        "length": tk.StringVar(),
        "cost_wo_vat": tk.StringVar(),
        "cost_with_vat": tk.StringVar()
    }

    tk.Label(C3_1_frame, text=str(row), borderwidth=1, relief="solid", width=5).grid(row=row, column=0, sticky='nsew')

    voltage_cb = ttk.Combobox(C3_1_frame, textvariable=row_vars["voltage"], state="readonly", width=15, justify='center')
    voltage_cb['values'] = list(rates_dict["C3_1"].keys())
    voltage_cb.grid(row=row, column=1, sticky='nsew')

    section_cb = ttk.Combobox(C3_1_frame, textvariable=row_vars["section"], state="readonly", width=20, justify='center')
    section_cb.grid(row=row, column=2, sticky='nsew')

    insulation_cb = ttk.Combobox(C3_1_frame, textvariable=row_vars["insulation"], state="readonly", width=20, justify='center')
    insulation_cb.grid(row=row, column=3, sticky='nsew')

    quantity_cb = ttk.Combobox(C3_1_frame, textvariable=row_vars["quantity"], state="readonly", width=20, justify='center')
    quantity_cb.grid(row=row, column=4, sticky='nsew')

    event_var = row_vars["event"]
    event_menu = tk.OptionMenu(C3_1_frame, event_var, '')
    event_menu.config(width=50, font=("Arial", 10), anchor='w')
    event_menu.grid(row=row, column=5, sticky='nsew')

    rate_entry = tk.Entry(C3_1_frame, textvariable=row_vars["rate"], state='readonly', justify='center', borderwidth=1, relief="solid")
    rate_entry.grid(row=row, column=6, sticky='nsew')

    length_entry = tk.Entry(
        C3_1_frame,
        textvariable=row_vars["length"],
        width=18,
        borderwidth=1,
        relief="solid",
        justify='center',
        validate='key',
        validatecommand=vcmd
    )
    length_entry.grid(row=row, column=7, sticky='nsew')

    cost_wo_vat_entry = tk.Entry(C3_1_frame, textvariable=row_vars["cost_wo_vat"], state='readonly', justify='center', borderwidth=1, relief="solid")
    cost_wo_vat_entry.grid(row=row, column=8, sticky='nsew')

    cost_with_vat_entry = tk.Entry(C3_1_frame, textvariable=row_vars["cost_with_vat"], state='readonly', justify='center', borderwidth=1, relief="solid")
    cost_with_vat_entry.grid(row=row, column=9, sticky='nsew')

    def on_voltage_change(event=None):
        voltage = row_vars["voltage"].get()
        sections = list(rates_dict["C3_1"].get(voltage, {}).keys())
        section_cb['values'] = sections
        row_vars["section"].set('')
        row_vars["insulation"].set('')
        row_vars["quantity"].set('')
        row_vars["event"].set('')
        row_vars["rate"].set('')
        row_vars["cost_wo_vat"].set('')
        row_vars["cost_with_vat"].set('')
        insulation_cb['values'] = []
        quantity_cb['values'] = []
        event_menu['menu'].delete(0, 'end')
        update_c31_totals()

    def on_section_change(event=None):
        voltage = row_vars["voltage"].get()
        section = row_vars["section"].get()
        insulations = list(rates_dict["C3_1"].get(voltage, {}).get(section, {}).keys())
        insulation_cb['values'] = insulations
        row_vars["insulation"].set('')
        row_vars["quantity"].set('')
        row_vars["event"].set('')
        row_vars["rate"].set('')
        row_vars["cost_wo_vat"].set('')
        row_vars["cost_with_vat"].set('')
        quantity_cb['values'] = []
        event_menu['menu'].delete(0, 'end')
        update_c31_totals()

    def on_insulation_change(event=None):
        voltage = row_vars["voltage"].get()
        section = row_vars["section"].get()
        insulation = row_vars["insulation"].get()
        quantities = list(rates_dict["C3_1"].get(voltage, {}).get(section, {}).get(insulation, {}).keys())
        quantity_cb['values'] = quantities
        row_vars["quantity"].set('')
        row_vars["event"].set('')
        row_vars["rate"].set('')
        row_vars["cost_wo_vat"].set('')
        row_vars["cost_with_vat"].set('')
        event_menu['menu'].delete(0, 'end')
        update_c31_totals()

    def on_quantity_change(event=None):
        voltage = row_vars["voltage"].get()
        section = row_vars["section"].get()
        insulation = row_vars["insulation"].get()
        quantity = row_vars["quantity"].get()
        events = list(rates_dict["C3_1"].get(voltage, {}).get(section, {}).get(insulation, {}).get(quantity, {}).keys())
        event_menu['menu'].delete(0, 'end')
        for ev in events:
            event_menu['menu'].add_command(label=ev, command=tk._setit(row_vars["event"], ev, on_event_selected))
        row_vars["event"].set('')
        row_vars["rate"].set('')
        row_vars["cost_wo_vat"].set('')
        row_vars["cost_with_vat"].set('')
        update_c31_totals()

    def on_event_selected(*args):
        voltage = row_vars["voltage"].get()
        section = row_vars["section"].get()
        insulation = row_vars["insulation"].get()
        quantity = row_vars["quantity"].get()
        event_name = row_vars["event"].get()
        if voltage and section and insulation and quantity and event_name:
            rate = rates_dict["C3_1"].get(voltage, {}).get(section, {}).get(insulation, {}).get(quantity, {}).get(event_name, 0)
            row_vars["rate"].set(to_str(rate, precision=2, grouping=True))
            length = to_float(row_vars["length"].get())
            cost_wo_vat = round(length * rate, 2)
            cost_with_vat = round(cost_wo_vat * 1.2, 2)
            row_vars["cost_wo_vat"].set(to_str(cost_wo_vat, precision=2, grouping=True))
            row_vars["cost_with_vat"].set(to_str(cost_with_vat, precision=2, grouping=True))
        else:
            row_vars["rate"].set('')
            row_vars["cost_wo_vat"].set('')
            row_vars["cost_with_vat"].set('')
        update_c31_totals()

    def on_length_change(*args):
        length = to_float(row_vars["length"].get())
        rate = to_float(row_vars["rate"].get())
        cost_wo_vat = round(rate * length, 2)
        cost_with_vat = round(cost_wo_vat * 1.2, 2)
        row_vars["cost_wo_vat"].set(to_str(cost_wo_vat, precision=2, grouping=True))
        row_vars["cost_with_vat"].set(to_str(cost_with_vat, precision=2, grouping=True))
        update_c31_totals()

    voltage_cb.bind("<<ComboboxSelected>>", on_voltage_change)
    section_cb.bind("<<ComboboxSelected>>", on_section_change)
    insulation_cb.bind("<<ComboboxSelected>>", on_insulation_change)
    quantity_cb.bind("<<ComboboxSelected>>", on_quantity_change)
    row_vars["event"].trace_add("write", on_event_selected)
    row_vars["length"].trace_add("write", on_length_change)

    c31_entry_vars.append(row_vars)
    next_c31_row += 1
    draw_c31_totals()
    update_c31_totals()

def remove_c31_row():
    global next_c31_row
    if next_c31_row > 1:
        next_c31_row -= 1
        row_widgets = C3_1_frame.grid_slaves(row=next_c31_row)
        for widget in row_widgets:
            widget.destroy()
        c31_entry_vars.pop()
        draw_c31_totals()
        update_c31_totals()

add_c31_row()

buttons_frame_c31 = tk.Frame(content_frame)
buttons_frame_c31.grid(row=21, column=0, columnspan=2, sticky='w', pady=10)
add_btn_c31 = tk.Button(buttons_frame_c31, text="Добавить кабельную линию", font=("Arial", 12, "bold"), command=add_c31_row, bg="#b7e4c7", width=30)
add_btn_c31.pack(side='left', padx=(0, 10))
remove_btn_c31 = tk.Button(buttons_frame_c31, text="Удалить кабельную линию", font=("Arial", 12, "bold"), command=remove_c31_row, bg="#f8d7da", width=30)
remove_btn_c31.pack(side='left')




root.mainloop()
