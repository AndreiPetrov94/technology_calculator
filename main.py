import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from collections import defaultdict

from scrollable_frame import ScrollableFrame
from form_config import data_applicant, data_connection_parameters, data_rate


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


def update_benefit_text(form_values, label=None):
    def get_value(key):
        widget = form_values.get(key)
        if widget is None:
            return None
        if isinstance(widget, ttk.Combobox) or isinstance(widget, DateEntry):
            return widget.get()
        elif isinstance(widget, tk.Entry):
            return widget.get()
        return None

    applicant_type = get_value("applicant_type")
    location = get_value("location")
    voltage = get_value("voltage")
    reliability_category = get_value("reliability_category")
    distance = get_value("distance")
    category = get_value("category_result")

    required_fields = [applicant_type, location, voltage, reliability_category, distance, category]
    if any(field is None or field == "" for field in required_fields):
        result_text = "Для определения признака расчета по льготной ставке за 1 кВт заполните информацию"
        bg_color = "SystemButtonFace"  # стандартный цвет фона (без выделения)
    else:
        condition_1 = (
            applicant_type == "Физическое лицо" and
            location in ["Город", "Поселок городского типа"] and
            voltage == "0,4 кВ и ниже" and
            reliability_category == "III" and
            distance == "менее 300" and
            category == "до 15 кВт"
        )

        condition_2 = (
            applicant_type == "Физическое лицо" and
            location == "Сельская местность" and
            voltage == "0,4 кВ и ниже" and
            reliability_category == "III" and
            distance == "менее 500" and
            category == "до 15 кВт"
        )

        condition_3 = (
            applicant_type in ["Юридическое лицо", "Индивидуальный предприниматель"] and
            location in ["Город", "Поселок городского типа"] and
            voltage == "0,4 кВ и ниже" and
            reliability_category == "III" and
            distance == "менее 200" and
            category in ["до 15 кВт", "от 15 до 150 кВт"]
        )

        condition_4 = (
            applicant_type in ["Юридическое лицо", "Индивидуальный предприниматель"] and
            location == "Сельская местность" and
            voltage == "0,4 кВ и ниже" and
            reliability_category == "III" and
            distance == "менее 300" and
            category in ["до 15 кВт", "от 15 до 150 кВт"]
        )

        general_condition_1 = not (condition_1 or condition_2)
        general_condition_2 = not (condition_3 or condition_4)

        if general_condition_1 and general_condition_2:
            result_text = "Заявитель не подходит по критериям для расчета по льготной ставке за 1 кВт"
            bg_color = "#ff8787"  # светло-красный (красный фон)
        elif condition_1 or condition_2 or condition_3 or condition_4:
            result_text = "Заявитель подходит по критериям для расчета по льготной ставке за 1 кВт"
            bg_color = "#69f78a"  # светло-зеленый (зелёный фон)
        else:
            result_text = "Данные не полные или не соответствуют условиям"
            bg_color = "SystemButtonFace"  # стандартный цвет фона

    if label:
        label.config(text=result_text, background=bg_color)


# ==== Таблица льготная ставка 1 кВт ====
def create_benefit_table(parent, form_values_connection):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)

    # Основной фрейм с полями
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

    # Обновляем текст при инициализации
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







def create_dynamic_table_with_headers(parent, data):
    name_rate = data["name_rate"]
    headers = data["headers"]
    column_widths = data.get("column_widths", [15] * len(headers))

    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)

    title = tk.Label(section, text=name_rate, font=("Arial", 12, "bold"), anchor="center")
    title.pack(anchor='center')

    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)

    font_style = ("Arial", 12)
    form_values = {}

    for col, header in enumerate(headers):
        label = tk.Label(frame, text=header, font=font_style, borderwidth=1, relief="solid",
                         padx=5, pady=5, width=column_widths[col])
        label.grid(row=0, column=col, sticky="nsew", padx=3, pady=3)

    current_row = 1
    total_labels = {}
    total_label_widget = None
    buttons_widgets = []
    merge_end_col = 0
    for i, header in enumerate(headers):
        if "Стоимость ставки" in header:
            merge_end_col = i
            break

    def update_totals(*args):
        try:
            cost_without_vat_col = headers.index("Стоимость без НДС, руб")
            cost_with_vat_col = headers.index("Стоимость с НДС, руб")
            cost_rate_col = len(headers) - 4  # 4-й столбец с конца
            length_col = len(headers) - 3     # 3-й столбец с конца
        except ValueError:
            return

        totals = {col: 0.0 for col in total_labels}
        for row_entries in form_values.values():
            # Автоматический расчет "Стоимость без НДС, руб" = (стоимость ставки) * (длина)
            try:
                cost_rate_val = float(replace_comma_with_dot(row_entries[cost_rate_col].get()))
                length_val = float(replace_comma_with_dot(row_entries[length_col].get()))
                cost_without_vat = cost_rate_val * length_val
                row_entries[cost_without_vat_col].delete(0, tk.END)
                row_entries[cost_without_vat_col].insert(0, f"{cost_without_vat:.2f}".replace('.', ','))
            except Exception:
                pass

            # Автоматический расчет "Стоимость с НДС, руб" = "Стоимость без НДС, руб" * 1.20
            try:
                cost_without_vat_val = float(replace_comma_with_dot(row_entries[cost_without_vat_col].get()))
                cost_with_vat = cost_without_vat_val * 1.20
                row_entries[cost_with_vat_col].delete(0, tk.END)
                row_entries[cost_with_vat_col].insert(0, f"{cost_with_vat:.2f}".replace('.', ','))
            except Exception:
                pass

            # Подсчет итогов по суммируемым столбцам
            for col in totals:
                try:
                    val = float(replace_comma_with_dot(row_entries[col].get()))
                    totals[col] += val
                except Exception:
                    pass

        for col, total in totals.items():
            total_labels[col].config(text=f"{total:.2f}".replace('.', ','))

    def draw_total_row():
        nonlocal total_label_widget

        if total_label_widget:
            total_label_widget.destroy()
        for lbl in total_labels.values():
            lbl.destroy()
        total_labels.clear()

        for btn in buttons_widgets:
            btn.grid_forget()

        total_row = current_row

        total_label_widget = tk.Label(frame, text="ИТОГО", font=font_style, borderwidth=1, relief="solid",
                                      padx=5, pady=5)
        total_label_widget.grid(row=total_row, column=0, columnspan=merge_end_col + 1,
                                sticky="nsew", padx=3, pady=3)

        for col in range(merge_end_col + 1, len(headers)):
            lbl = tk.Label(frame, text="0", font=font_style, borderwidth=1, relief="solid",
                           padx=5, pady=5, width=column_widths[col])
            lbl.grid(row=total_row, column=col, sticky="nsew", padx=3, pady=3)
            total_labels[col] = lbl

        btn_row = total_row + 1
        buttons_widgets[0].grid(row=btn_row, column=0, sticky="w", padx=5, pady=10)
        buttons_widgets[1].grid(row=btn_row, column=1, sticky="w", padx=5, pady=10)
        update_totals()

    def add_row():
        nonlocal current_row
        form_values[current_row] = {}
        for col in range(len(headers)):
            entry = tk.Entry(frame, font=font_style, width=column_widths[col])
            entry.grid(row=current_row, column=col, sticky="nsew", padx=3, pady=3)

            # Привязка событий
            entry.bind("<KeyRelease>", update_totals)
            entry.bind("<FocusOut>", validate_and_format_float)
            entry.bind("<FocusOut>", replace_dot_with_comma, add='+')

            form_values[current_row][col] = entry
        current_row += 1
        draw_total_row()

    def remove_row():
        nonlocal current_row
        if current_row > 1:
            for widget in form_values[current_row - 1].values():
                widget.destroy()
            del form_values[current_row - 1]
            current_row -= 1
            draw_total_row()

    btn_add = tk.Button(frame, text="Добавить строку", font=font_style, bg="#69f78a", width=20, command=add_row)
    btn_remove = tk.Button(frame, text="Удалить строку", font=font_style, bg="#ff8787", width=20, command=remove_row)
    buttons_widgets = [btn_add, btn_remove]

    add_row()

    return form_values




















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

    # Создаем метку льготы
    benefit_label = create_benefit_table(scrollable.scrollable_frame, value_connection_parameters)

    def unified_update(event=None):
        update_distance_options(value_connection_parameters)
        update_benefit_text(value_connection_parameters, benefit_label)

    # Привязка событий для автообновления
    value_connection_parameters["applicant_type"].bind("<<ComboboxSelected>>", unified_update)
    value_connection_parameters["location"].bind("<<ComboboxSelected>>", unified_update)
    value_connection_parameters["voltage"].bind("<<ComboboxSelected>>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))
    value_connection_parameters["reliability_category"].bind("<<ComboboxSelected>>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))
    value_connection_parameters["distance"].bind("<<ComboboxSelected>>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))
    value_connection_parameters["category_result"].bind("<FocusOut>", lambda e: update_benefit_text(value_connection_parameters, benefit_label))

    table_frame_C2 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C2"]
    )
    table_frame_C3_1 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C3_1"]
    )
    table_frame_C3_2 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C3_2"]
    )
    table_frame_C4 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C4"]
    )
    table_frame_C5 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C5"]
    )
    table_frame_C8 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C8"]
    )

    return benefit_label

def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
