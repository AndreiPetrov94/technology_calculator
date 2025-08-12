import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from num2words import num2words
from scrollable_frame import ScrollableFrame
from form_config_01 import data_applicant, data_connection_parameters, data_rate_power

def create_main_window():
    root = tk.Tk()
    root.title("Калькулятор расчета стоимости по ТП")
    root.geometry("1450x900")
    root.iconbitmap("resources/logo_VVEK.ico")
    return root

def replace_comma_with_dot(text: str) -> str:
    if text is None:
        return ""
    return text.replace(',', '.')

def replace_dot_with_comma(event):
    entry = event.widget
    text = entry.get()
    if '.' in text:
        new_text = text.replace('.', ',')
        entry.delete(0, tk.END)
        entry.insert(0, new_text)

def validate_and_format_float(event, min_val=0.0, max_val=32000.0):
    entry = event.widget
    text = entry.get()
    text = replace_comma_with_dot(text)
    try:
        value = float(text)
        if not (min_val <= value <= max_val):
            raise ValueError("Out of range")
        formatted = f"{value:.2f}".replace('.', ',')
        entry.delete(0, tk.END)
        entry.insert(0, formatted)
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, "")

def update_distance_options(form_values):
    applicant = form_values["applicant_type"].get()
    location = form_values["location"].get()
    distance_widget = form_values["distance"]
    new_values = []
    if applicant == "Физическое лицо":
        if location in ["Город", "Поселок городского типа"]:
            new_values = ["менее 300", "более 300"]
        elif location == "Сельская местность":
            new_values = ["менее 500", "более 500"]
    elif applicant in ["Юридическое лицо", "Индивидуальный предприниматель"]:
        if location in ["Город", "Поселок городского типа"]:
            new_values = ["менее 200", "более 200"]
        elif location == "Сельская местность":
            new_values = ["менее 300", "более 300"]
    if new_values:
        distance_widget["values"] = new_values
        distance_widget.set("")


def create_table(parent, title_text, data_dict, form_values, is_connection_section=False):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)
    title = tk.Label(section, text=title_text, font=("Arial", 12, "bold"), anchor="center")
    title.pack(anchor='center')
    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)
    font_style = ("Arial", 12)

    for row_index, (key, config) in enumerate(data_dict.items()):
        label = tk.Label(
            frame,
            text=config["label"],
            font=font_style,
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=3,
            width=60 if is_connection_section else 40,
            anchor='w'
        )
        label.grid(row=row_index, column=0, padx=5, pady=5, sticky='w')
        if config["type"] == "entry":
            entry = tk.Entry(frame, width=50, font=font_style, relief="solid", borderwidth=1)
            entry.grid(row=row_index, column=1, padx=5, pady=5, ipady=2, sticky='w')
            form_values[key] = entry
        elif config["type"] == "date":
            date_entry = DateEntry(
                frame,
                width=48,
                font=font_style,
                relief="solid",
                borderwidth=1,
                date_pattern='dd.mm.yyyy',
                locale='ru_RU'
            )
            date_entry.grid(row=row_index, column=1, padx=5, pady=5, ipady=2, sticky='w')
            form_values[key] = date_entry
        elif config["type"] == "combobox":
            combo = ttk.Combobox(
                frame,
                values=config["values"],
                width=28,
                font=font_style,
                state="readonly"
            )
            combo.grid(row=row_index, column=1, padx=5, pady=5, ipady=1, sticky='w')
            combo.bind("<MouseWheel>", lambda e: "break")
            form_values[key] = combo
        elif config["type"] == "float_entry":
            entry = tk.Entry(frame, width=30, font=font_style, relief="solid", borderwidth=1)
            entry.grid(row=row_index, column=1, padx=5, pady=5, ipady=3, sticky='w')
            entry.bind('<KeyRelease>', replace_dot_with_comma)
            entry.bind('<FocusOut>', validate_and_format_float)
            form_values[key] = entry
        elif config["type"] == "readonly":
            entry = tk.Entry(frame, width=30, font=font_style, relief="solid", borderwidth=1, state="readonly")
            entry.grid(row=row_index, column=1, padx=5, pady=5, ipady=3, sticky='w')
            form_values[key] = entry
        else:
            tk.Label(frame, text="Неподдерживаемый тип", font=font_style).grid(
                row=row_index, column=1, padx=5, pady=5, sticky='w'
            )
    if is_connection_section:
        def update_power_total(*args):
            try:
                prev = form_values["power_prev"].get()
                new = form_values["power_new"].get()
                power_total = float(replace_comma_with_dot(prev) or 0) + float(replace_comma_with_dot(new) or 0)

                total_field = form_values["power_total"]
                total_field.config(state="normal")
                total_field.delete(0, tk.END)
                total_field.insert(0, f"{power_total:.2f}".replace('.', ','))
                total_field.config(state="readonly")
                if power_total <= 15.00:
                    category = "до 15 кВт"
                elif power_total <= 150.00:
                    category = "от 15 до 150 кВт"
                else:
                    category = "свыше 150 кВт"
                category_field = form_values["category_result"]
                category_field.config(state="normal")
                category_field.delete(0, tk.END)
                category_field.insert(0, category)
                category_field.config(state="readonly")
            except Exception:
                pass
        form_values["power_prev"].bind("<FocusOut>", lambda e: (validate_and_format_float(e), update_power_total()))
        form_values["power_new"].bind("<FocusOut>", lambda e: (validate_and_format_float(e), update_power_total()))
        form_values["applicant_type"].bind("<<ComboboxSelected>>", lambda e: update_distance_options(form_values))
        form_values["location"].bind("<<ComboboxSelected>>", lambda e: update_distance_options(form_values))

def extract_form_values(form_values):
    def get_value(widget):
        if widget is None:
            return None
        if isinstance(widget, (ttk.Combobox, DateEntry, tk.Entry)):
            return widget.get()
        return None

    values = {}
    for key, widget in form_values.items():
        values[key] = get_value(widget)
    return values


def update_benefit_text(form_values, label=None):
    keys = [
        "applicant_type",
        "location",
        "voltage",
        "reliability_category",
        "distance",
        "category_result"
    ]
    # Извлекаем все значения (без передачи keys)
    values = extract_form_values(form_values)

    # Проверяем, что все ключи есть в values и их значения не пусты
    if any(values.get(k) is None or values.get(k) == "" for k in keys):
        result_text = "Для определения признака расчета по льготной ставке за 1 кВт заполните информацию"
        bg_color = "SystemButtonFace"
    else:
        condition_1 = (
            values["applicant_type"] == "Физическое лицо" and
            values["location"] in ["Город", "Поселок городского типа"] and
            values["voltage"] == "0,4 кВ и ниже" and
            values["reliability_category"] == "III" and
            values["distance"] == "менее 300" and
            values["category_result"] == "до 15 кВт"
        )
        condition_2 = (
            values["applicant_type"] == "Физическое лицо" and
            values["location"] == "Сельская местность" and
            values["voltage"] == "0,4 кВ и ниже" and
            values["reliability_category"] == "III" and
            values["distance"] == "менее 500" and
            values["category_result"] == "до 15 кВт"
        )
        condition_3 = (
            values["applicant_type"] in ["Юридическое лицо", "Индивидуальный предприниматель"] and
            values["location"] in ["Город", "Поселок городского типа"] and
            values["voltage"] == "0,4 кВ и ниже" and
            values["reliability_category"] == "III" and
            values["distance"] == "менее 200" and
            values["category_result"] in ["до 15 кВт", "от 15 до 150 кВт"]
        )
        condition_4 = (
            values["applicant_type"] in ["Юридическое лицо", "Индивидуальный предприниматель"] and
            values["location"] == "Сельская местность" and
            values["voltage"] == "0,4 кВ и ниже" and
            values["reliability_category"] == "III" and
            values["distance"] == "менее 300" and
            values["category_result"] in ["до 15 кВт", "от 15 до 150 кВт"]
        )
        general_condition_1 = not (condition_1 or condition_2)
        general_condition_2 = not (condition_3 or condition_4)
        if general_condition_1 and general_condition_2:
            result_text = "Заявитель не подходит по критериям для расчета по льготной ставке за 1 кВт"
            bg_color = "#ff8787"
        elif condition_1 or condition_2 or condition_3 or condition_4:
            result_text = "Заявитель подходит по критериям для расчета по льготной ставке за 1 кВт"
            bg_color = "#69f78a"
        else:
            result_text = "Данные не полные или не соответствуют условиям"
            bg_color = "SystemButtonFace"

    if label:
        label.config(text=result_text, background=bg_color)


# ==== Таблица льготная ставка 1 кВт ====
def create_benefit_table(parent, form_values_connection):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)
    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)
    font_style = ("Arial", 12, "bold")
    label_example = tk.Label(
        frame,
        text="",
        font=font_style,
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=5,
        width=83,
        anchor='c',
        justify="left",
        wraplength=1200
    )
    label_example.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    update_benefit_text(form_values_connection, label_example)
    return label_example

def bind_update_benefit_label(form_values, label):
    keys_to_bind = [
        "applicant_type", "location", "voltage",
        "reliability_category", "distance", "category_result"
    ]
    for key in keys_to_bind:
        widget = form_values.get(key)
        if widget:
            if isinstance(widget, ttk.Combobox):
                widget.bind("<<ComboboxSelected>>", lambda e: update_benefit_text(form_values, label))
            elif isinstance(widget, tk.Entry):
                widget.bind("<FocusOut>", lambda e: update_benefit_text(form_values, label))

# ==== Таблица для расчета ставок ====
def create_dynamic_table_with_headers(parent, data_rate_config, data_rate_all_dict):
    pass

def number_to_words_rub_kop(value_str):
    try:
        value_str = replace_comma_with_dot(value_str)
        value = float(value_str)
    except ValueError:
        return ""
    rub = int(value)
    kop = int(round((value - rub) * 100))

    rub_text = num2words(rub, lang='ru')
    kop_text = num2words(kop, lang='ru')
    if rub % 10 == 1 and rub % 100 != 11:
        rub_word = "рубль"
    elif 2 <= rub % 10 <= 4 and (rub % 100 < 10 or rub % 100 >= 20):
        rub_word = "рубля"
    else:
        rub_word = "рублей"
    if kop % 10 == 1 and kop % 100 != 11:
        kop_word = "копейка"
    elif 2 <= kop % 10 <= 4 and (kop % 100 < 10 or kop % 100 >= 20):
        kop_word = "копейки"
    else:
        kop_word = "копеек"
    return f"{rub_text} {rub_word} {kop_text} {kop_word}"

# ==== Таблица для расчета итоговой стоимости и сравнения ставок ====
TABLE_HEADERS = [
    "Ставка",
    "Стоимость без НДС, руб",
    "Сумма НДС, руб",
    "Стоимость с НДС, руб"
]

BLOCKS_DATA = {
    1: "Стоимость мероприятий по ТП,\n"
       "рассчитанная с применением\n"
       "льготной ставки за 1 кВт",
    3: "Стоимость мероприятий по ТП,\n"
       "рассчитанная с применением\n"
       "стандартизированных\nтарифных ставок"
}

PLACEHOLDER_TEXT = "Значение рассчитывается автоматически"


def create_result_table(parent, placeholder):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)

    title = tk.Label(section, text='Расчет по льготной ставке за 1 кВт и СТС',
                     font=("Arial", 12, "bold"), anchor="center")
    title.pack(anchor='center')

    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)

    font_style_header = ("Arial", 12, "bold")
    font_style_cells = ("Arial", 12)

    # Заголовки таблицы
    for col, header in enumerate(TABLE_HEADERS):
        lbl = tk.Label(frame, text=header, font=font_style_header,
                       borderwidth=1, relief="solid", width=25, anchor="center")
        lbl.grid(row=0, column=col, padx=5, pady=5, ipady=2, sticky="nsew")

    # Валидация и перевод в слова
    def validate_and_copy_words(event, linked_var):
        entry = event.widget
        text = entry.get().replace(',', '.')
        try:
            value = float(text)
            if not (0.0 <= value <= 1000000000.0):
                raise ValueError("Out of range")
            formatted = f"{value:.2f}".replace('.', ',')
            entry.delete(0, tk.END)
            entry.insert(0, formatted)
            linked_var.set(number_to_words_rub_kop(formatted))
        except ValueError:
            entry.delete(0, tk.END)
            linked_var.set("")

    # Копирование в буфер
    def copy_to_clipboard(text):
        parent.clipboard_clear()
        parent.clipboard_append(text)

    # Создание блока строк
    def create_big_cell_block(start_row, text):
        lbl = tk.Label(frame, text=text, font=font_style_cells, borderwidth=1,
                       relief="solid", anchor="w", justify="left", width=25)
        lbl.grid(row=start_row, column=0, rowspan=2, padx=5, pady=5, ipady=10, sticky="nsew")

        for col in range(1, 4):
            display_var = tk.StringVar()

            # Первая строка: Entry + кнопка копирования
            entry_container = tk.Frame(frame)
            entry_container.grid(row=start_row, column=col, padx=5, pady=5, sticky="nsew")

            entry = tk.Entry(entry_container, font=font_style_cells, borderwidth=1,
                             relief="solid", width=30, justify='center')
            entry.insert(0, placeholder)  # Заглушка
            entry.pack(side="left", fill="x", expand=True)
            entry.bind("<FocusOut>", lambda e, var=display_var: validate_and_copy_words(e, var))

            btn_copy_entry = tk.Button(entry_container, text="❐", font=("Arial", 12),
                                       command=lambda e=entry: copy_to_clipboard(e.get()))
            btn_copy_entry.pack(side="left", padx=(5, 0), ipady=5)

            # Вторая строка: Text + кнопка копирования
            text_container = tk.Frame(frame)
            text_container.grid(row=start_row + 1, column=col, padx=5, pady=(0, 0), sticky="nsew")

            display = tk.Text(text_container, font=font_style_cells, borderwidth=1,
                              relief="solid", width=30, height=2, wrap="word")
            display.pack(side="left", fill="both", expand=True)
            display.insert("1.0", display_var.get())
            display.config(state="disabled")

            def update_text(*args, disp=display, var=display_var):
                disp.config(state="normal")
                disp.delete("1.0", tk.END)
                disp.insert("1.0", var.get())
                disp.config(state="disabled")

            display_var.trace_add("write", update_text)

            btn_copy_text = tk.Button(text_container, text="❐", font=("Arial", 12),
                                      command=lambda var=display_var: copy_to_clipboard(var.get()))
            btn_copy_text.pack(side="left", padx=(5, 0), ipady=5)

    # Генерация блоков через цикл
    for row, description in BLOCKS_DATA.items():
        create_big_cell_block(row, description)

    return frame

def setup_interface(root):
    tk.Label(
        root,
        text="Калькулятор расчета стоимости по ТП",
        font=("Arial", 20, "bold"),
        bg="#b7e4c7",
        padx=10,
        pady=10,
        anchor='center'
    ).pack(fill='x')
    scrollable = ScrollableFrame(root)
    scrollable.pack(fill='both', expand=True)
    value_applicant = {}
    value_connection_parameters = {}
    create_table(
        scrollable.scrollable_frame,
        "Данные Заявителя",
        data_applicant,
        value_applicant
    )
    create_table(
        scrollable.scrollable_frame,
        "Информация для расчета стоимости по ТП",
        data_connection_parameters,
        value_connection_parameters,
        is_connection_section=True
    )
    benefit_label = create_benefit_table(
        scrollable.scrollable_frame,
        value_connection_parameters
    )
    def unified_update(event=None):
        update_distance_options(value_connection_parameters)
        update_benefit_text(value_connection_parameters, benefit_label)
    value_connection_parameters["applicant_type"].bind("<<ComboboxSelected>>", unified_update)
    value_connection_parameters["location"].bind("<<ComboboxSelected>>", unified_update)
    value_connection_parameters["voltage"].bind("<<ComboboxSelected>>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))
    value_connection_parameters["reliability_category"].bind("<<ComboboxSelected>>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))
    value_connection_parameters["distance"].bind("<<ComboboxSelected>>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))
    value_connection_parameters["category_result"].bind("<FocusOut>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))




    current_text = benefit_label.cget("text")
    print(current_text)

    create_result_table(scrollable.scrollable_frame, current_text)

    return benefit_label

def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
