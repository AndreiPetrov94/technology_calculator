import tkinter as tk
from tkcalendar import DateEntry

from scrollable_frame import ScrollableFrame
from form_config import data_applicant, data_parameter


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

    for row_index, (field_key, field_info) in enumerate(data_dict.items()):
        label_text = field_info.get("label", field_key)
        field_type = field_info.get("type", "entry")

        # Метка
        label = tk.Label(
            frame,
            text=label_text,
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
        if field_type == "entry":
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
            value_applicant[field_key] = entry

        elif field_type == "date":
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
            value_applicant[field_key] = date_entry

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


# ==== Таблица 2: Информация для расчета стоимости по ТП ====
def create_paramet_table(parent, data_dict):
    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)

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
    value_paramet = {}

    for row_index, (field_key, field_info) in enumerate(data_dict.items()):
        label_text = field_info.get("label", field_key)
        field_type = field_info.get("type", "entry")

        # Метка
        label = tk.Label(
            frame,
            text=label_text,
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
        if field_type == "entry":
            entry = tk.Entry(
                frame,
                width=30,
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
            value_paramet[field_key] = entry

        elif field_type == "date":
            date_entry = DateEntry(
                frame,
                width=30,  # ширина по твоему усмотрению
                font=font_style,
                relief="solid",
                borderwidth=1,
                date_pattern='dd.mm.yyyy'  # формат даты
            )
            date_entry.grid(
                row=row_index,
                column=1,
                padx=5,
                pady=5,
                ipady=3,
                sticky='w'
            )
            value_paramet[field_key] = date_entry

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
    create_paramet_table(scrollable.scrollable_frame, data_parameter)


def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
