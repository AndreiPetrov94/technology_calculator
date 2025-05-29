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


# ==== Таблица 1: Заявитель ====
def create_applicant_table(parent, data_dict):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)

    # Заголовок секции
    title = tk.Label(
        section,
        text="Данные Заявителя",
        font=("Arial", 12, "bold"),
        anchor="center"
    )
    title.pack(anchor='center')

    # Основной фрейм с полями
    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)

    font_style = ("Arial", 12)
    value_applicant = {}

    for row_index, (key, config) in enumerate(data_dict.items()):

        # Метка
        label = tk.Label(
            frame,
            text=config["label"],
            font=font_style,
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=3,
            width=40,
            anchor='w'
        )
        label.grid(
            row=row_index,
            column=0,
            padx=5,
            pady=5,
            sticky='w'
        )

        # Поле ввода
        if config["type"] == "entry":
            entry = tk.Entry(
                frame,
                width=50,
                font=font_style,
                relief="solid",
                borderwidth=1
            )
            entry.grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                ipady=3,
                sticky='w'
            )
            value_applicant[key] = entry

        elif config["type"] == "date":
            date_entry = DateEntry(
                frame,
                width=48,  # ширина по твоему усмотрению
                font=font_style,
                relief="solid",
                borderwidth=1,
                date_pattern='dd.mm.yyyy',
                locale='ru_RU'
            )
            date_entry.grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                ipady=3,
                sticky='w'
            )
            value_applicant[key] = date_entry

        else:
            tk.Label(
                frame,
                text="Неподдерживаемый тип",
                font=font_style,
                relief="solid",
                borderwidth=1
            ).grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                sticky='w'
            )


def configure_float_entry(entry_widget, min_value=0, max_value=32000):
    def validate(P):
        if P == "":
            return True
        # Заменяем запятую на точку для преобразования
        try:
            value = float(P.replace(",", "."))
            # Проверка диапазона
            if not (min_value <= value <= max_value):
                return False
            # Проверка количества знаков после запятой
            parts = P.split(",")
            if len(parts) == 2 and len(parts[1]) > 2:
                return False
            return True
        except ValueError:
            return False

    def replace_dot(event):
        text = entry_widget.get().replace(".", ",")
        try:
            value = float(text.replace(",", "."))
            formatted = f"{value:.2f}".replace(".", ",")
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, formatted)
        except ValueError:
            pass  # Оставим поле без изменений, если невалидно

    vcmd = (entry_widget.register(validate), "%P")
    entry_widget.config(validate="key", validatecommand=vcmd)
    entry_widget.bind("<FocusOut>", replace_dot)


# ==== Таблица 2: Информация для расчета стоимости по ТП ====
def create_connection_parameters_table(parent, data_dict):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=0)

    # Заголовок секции
    title = tk.Label(
        section,
        text="Информация для расчета стоимости по ТП",
        font=("Arial", 12, "bold"),
        anchor="center"
    )
    title.pack(anchor='center')

    # Основной фрейм с полями
    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)

    font_style = ("Arial", 12)
    value_connection_parameters = {}
    # vcmd = (frame.register(validate_float_input), '%P')

    for row_index, (key, config) in enumerate(data_dict.items()):

        # Метка
        label = tk.Label(
            frame,
            text=config["label"],
            font=font_style,
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=3,
            width=60,
            anchor='w'
        )
        label.grid(
            row=row_index,
            column=0,
            padx=5,
            pady=5,
            sticky='w'
        )

        # Поле ввода
        if config["type"] == "combobox":
            entry = ttk.Combobox(
                frame,
                values=config["values"],
                width=28,
                font=font_style,
                state="readonly"
            )
            entry.grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                ipady=3,
                sticky='w'
            )
            entry.bind("<MouseWheel>", lambda e: "break")
            value_connection_parameters[key] = entry

        elif config["type"] == "float_entry":
            entry = tk.Entry(
                frame,
                width=30,
                font=font_style,
                relief="solid",
                borderwidth=1,
                validate="key"
            )
            entry.grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                ipady=3,
                sticky='w'
            )
            configure_float_entry(entry)
            value_connection_parameters[key] = entry

        elif config["type"] == "readonly":
            entry = tk.Entry(
                frame,
                width=30,
                font=font_style,
                relief="solid",
                borderwidth=1,
                state="readonly"
            )
            entry.grid(row=row_index, column=1, padx=5, pady=5, ipady=3, sticky='w')
            value_connection_parameters[key] = entry


        else:
            tk.Label(
                frame,
                width=30,
                text="Неподдерживаемый тип",
                font=font_style,
                relief="solid",
                borderwidth=1
            ).grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                sticky='w'
            )


# ==== UI ====
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

    create_applicant_table(scrollable.scrollable_frame, data_applicant)
    create_connection_parameters_table(scrollable.scrollable_frame, data_connection_parameters)


def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
