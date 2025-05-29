import tkinter as tk

from scrollable_frame import ScrollableFrame
from form_config_2 import application_data


def create_main_window():
    root = tk.Tk()
    root.title("Калькулятор расчета стоимости по ТП")
    root.geometry("1450x900")

    return root


# ==== Таблица 1: Заявитель ====
def create_applicant_table(parent, data_dict):
    # Контейнер всей секции
    section = tk.Frame(parent)
    section.pack(fill='x', pady=10)

    # Центрированный заголовок
    title = tk.Label(
        section,
        text="Данные Заявителя",
        font=("Arial", 12, "bold"),
        anchor="center"
    )
    title.pack(fill='x')

    # Основной фрейм с содержимым
    frame = tk.Frame(section, padx=10, pady=10, relief="groove", bd=2)
    frame.pack(pady=5)

    for row_index, (field_key, field_info) in enumerate(data_dict.items()):
        label_text = field_info.get("label", field_key)
        field_type = field_info.get("type", "entry")

        # Метка
        tk.Label(frame, text=label_text).grid(row=row_index, column=0, sticky='e', padx=5, pady=5)

        # Виджет ввода
        if field_type == "entry":
            entry = tk.Entry(frame, width=50)
            entry.grid(row=row_index, column=1, padx=5, pady=5, sticky='w')
        elif field_type == "date":
            entry = tk.Entry(frame, width=50)
            entry.insert(0, "дд.мм.гггг")  # можно позже заменить на datepicker
            entry.grid(row=row_index, column=1, padx=5, pady=5, sticky='w')
        else:
            tk.Label(frame, text="Неподдерживаемый тип").grid(row=row_index, column=1)


# ==== Таблица 1: Заявитель ====
def create_applicant_table_2(parent, data_dict):
    # Контейнер всей секции
    section = tk.Frame(parent)
    section.pack(fill='x', pady=10)

    # Центрированный заголовок
    title = tk.Label(
        section,
        text="Данные Заявителя",
        font=("Arial", 12, "bold"),
        anchor="center"
    )
    title.pack(fill='x')

    # Основной фрейм с содержимым
    frame = tk.Frame(section, padx=10, pady=10, relief="groove", bd=2)
    frame.pack(fill='x', pady=5)

    for row_index, (field_key, field_info) in enumerate(data_dict.items()):
        label_text = field_info.get("label", field_key)
        field_type = field_info.get("type", "entry")

        # Метка
        tk.Label(frame, text=label_text).grid(row=row_index, column=0, sticky='e', padx=5, pady=5)

        # Виджет ввода
        if field_type == "entry":
            entry = tk.Entry(frame, width=100)
            entry.grid(row=row_index, column=1, padx=5, pady=5, sticky='w')
        elif field_type == "date":
            entry = tk.Entry(frame, width=100)
            entry.insert(0, "дд.мм.гггг")  # можно позже заменить на datepicker
            entry.grid(row=row_index, column=1, padx=5, pady=5, sticky='w')
        else:
            tk.Label(frame, text="Неподдерживаемый тип").grid(row=row_index, column=1)





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

    create_applicant_table(scrollable.scrollable_frame, application_data)
    create_applicant_table_2(scrollable.scrollable_frame, application_data)


def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
