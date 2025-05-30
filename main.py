import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from scrollable_frame import ScrollableFrame
from form_config import data_applicant, data_connection_parameters


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

        def update_distance_options(*args):
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

        form_values["applicant_type"].bind("<<ComboboxSelected>>", lambda e: update_distance_options())
        form_values["location"].bind("<<ComboboxSelected>>", lambda e: update_distance_options())


# ==== Таблица 1: Заявитель ====
def create_benefit_table(parent):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)

    # Основной фрейм с полями
    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)

    font_style = ("Arial", 12)
    value_benefit = {}

    # Добавляем ячейку с текстом "пример", занимающую две колонки
    label_example = tk.Label(
        frame,
        text="пример",
        font=font_style,
        borderwidth=1,
        relief="solid",
        padx=5,
        pady=5,
        width=92,
        anchor='w'
    )
    label_example.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    return value_benefit


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

    create_benefit_table(scrollable.scrollable_frame)


def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
