import tkinter as tk
from tkinter import ttk
from scrollable_frame import ScrollableFrame
from form_config_05 import data_rate, data_rate_all

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

def create_dynamic_table_with_headers(parent, data_rate_config, data_rate_all_dict):

    # name_rate = data["name_rate"]
    # headers = data["headers"]
    # column_widths = data.get("column_widths", [15] * len(headers))
    # section = tk.Frame(parent)
    # section.pack(anchor='w', padx=10, pady=5)
    # title = tk.Label(section, text=name_rate, font=("Arial", 12, "bold"), anchor="center")
    # title.pack(anchor='center')
    # frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    # frame.pack(anchor="w", padx=10, pady=5)
    # font_style = ("Arial", 12)
    # form_values = {}









    name_rate = data_rate_config["name_rate"]
    columns_cfg = data_rate_config["columns"]
    column_widths = data_rate_config.get("column_widths", [15] * len(columns_cfg))


    section = tk.Frame(parent)
    section.pack(anchor='w', padx=10, pady=5)
    title = tk.Label(section, text=name_rate, font=("Arial", 12, "bold"), anchor="center")
    title.pack(anchor='center')
    frame = tk.Frame(section, padx=10, pady=10, relief="ridge", bd=5)
    frame.pack(anchor="w", padx=10, pady=5)
    font_style = ("Arial", 12)


    # font_style = ("Arial", 12)
    # frame = tk.Frame(parent, padx=10, pady=10, relief="ridge", bd=5)
    # frame.pack(anchor="w", padx=10, pady=5)

    headers = [col["header"] for col in columns_cfg]

    # Находим индексы ключевых столбцов
    price_rate_col = None
    value_col = None
    cost_without_vat_col = None
    cost_with_vat_col = None
    index_col = None

    for i, col_cfg in enumerate(columns_cfg):
        if col_cfg["type"] == "index":
            index_col = i
        if col_cfg.get("key") == "price_rate":
            price_rate_col = i
        if col_cfg.get("key") == "value":
            value_col = i
        if col_cfg.get("key") == "cost_without_vat":
            cost_without_vat_col = i
        if col_cfg.get("key") == "cost_with_vat":
            cost_with_vat_col = i

    # Отрисовка заголовков
    for col, header in enumerate(headers):
        label = tk.Label(frame, text=header, font=font_style, borderwidth=1, relief="solid",
                         padx=5, pady=5, width=column_widths[col])
        label.grid(row=0, column=col, sticky="nsew", padx=3, pady=3)

    # Словарь для хранения виджетов в формате: {номер_строки: {индекс_столбца: виджет}}
    form_values = {}
    current_row = 1

    def update_indices():
        # Обновляем нумерацию строк
        for row_num in range(1, current_row):
            if index_col is not None and row_num in form_values:
                widget = form_values[row_num][index_col]
                if isinstance(widget, tk.Label):
                    widget.config(text=str(row_num))

    def replace_comma_with_dot(s):
        return s.replace(',', '.') if isinstance(s, str) else s

    def get_nested_dict_by_path(d, path):
        """
        Проходит по словарю d по ключам из path.
        Возвращает None, если ключ отсутствует.
        """
        cur = d
        try:
            for p in path:
                cur = cur[p]
            return cur
        except (KeyError, TypeError):
            return None

    def get_options_for_combobox(row_num, col_idx):
        """
        Получает список вариантов для combobox на основе выбранных значений в предыдущих combobox
        (от 1-го столбца до col_idx - 1), по словарю data_rate_all_dict.
        """
        # Сбор выбранных значений предыдущих combobox до col_idx
        selections = []
        for ci in range(1, col_idx):
            widget = form_values[row_num].get(ci)
            if widget is None:
                break
            val = widget.get()
            if val == "":
                break
            selections.append(val)

        # Извлечь словарь с нужным уровнем вложенности
        nested = get_nested_dict_by_path(data_rate_all_dict, selections)

        # Если это словарь, вернуть ключи, иначе пустой список
        if isinstance(nested, dict):
            # Важно: если значение словаря — это числовая ставка, то вариантов нет
            # Поэтому отфильтруем только те ключи, у которых значение - dict или str (опции)
            # Но обычно значения в словаре options - ключи
            # Тут просто возвращаем все ключи словаря
            return list(nested.keys())
        else:
            return []

    def update_price_rate(row_num):
        """
        Обновляет поле 'price_rate' для строки, исходя из выбранных значений combobox
        """
        # Собираем выбранные значения до price_rate_col (не включая price_rate_col)
        selections = []
        for ci in range(1, price_rate_col):
            widget = form_values[row_num].get(ci)
            if widget is None:
                break
            val = widget.get()
            if val == "":
                break
            selections.append(val)

        price = get_nested_dict_by_path(data_rate_all_dict, selections)
        price_widget = form_values[row_num].get(price_rate_col)
        if price_widget is None:
            return

        if isinstance(price, (int, float)):
            price_widget.config(state='normal')
            price_widget.delete(0, tk.END)
            # Записываем цену с заменой '.' на ','
            price_widget.insert(0, f"{price:.2f}".replace('.', ','))
            price_widget.config(state='readonly')
        else:
            # Если цена не найдена или не число — очистить поле
            price_widget.config(state='normal')
            price_widget.delete(0, tk.END)
            price_widget.config(state='readonly')

    def on_combobox_select(event, row_num, col_idx):
        """
        Обработчик выбора значения в combobox:
        - обновляет варианты в следующем combobox, если он есть и до price_rate_col
        - обновляет цену в price_rate
        - пересчитывает итоговые стоимости
        """
        next_col = col_idx + 1
        if next_col < price_rate_col:
            widget_next = form_values[row_num].get(next_col)
            if widget_next:
                opts = get_options_for_combobox(row_num, next_col)
                widget_next['values'] = opts
                # Сбросим значение, если текущего нет в новых опциях
                if widget_next.get() not in opts:
                    widget_next.set('')
                # Очистим значения в дальнейших combobox
                for c in range(next_col + 1, price_rate_col):
                    w = form_values[row_num].get(c)
                    if w:
                        w.set('')

        update_price_rate(row_num)
        update_totals()

    def on_validate_float(event, row_num):
        """
        Валидация поля ввода для float_entry с ограничениями
        """
        widget = form_values[row_num].get(value_col)
        if widget is None:
            return

        val = widget.get()
        try:
            v = float(val.replace(',', '.'))
            if v < 0 or v > 32000:
                raise ValueError()
        except Exception:
            widget.delete(0, tk.END)
            widget.insert(0, '0')
        update_totals()

    def update_totals():
        """
        Обновляет расчёты стоимости по всем строкам
        """
        try:
            for row_entries in form_values.values():
                try:
                    cost_rate_val = float(replace_comma_with_dot(row_entries[price_rate_col].get()))
                    length_val = float(replace_comma_with_dot(row_entries[value_col].get()))
                    cost_without_vat = cost_rate_val * length_val
                    row_entries[cost_without_vat_col].config(state='normal')
                    row_entries[cost_without_vat_col].delete(0, tk.END)
                    row_entries[cost_without_vat_col].insert(0, f"{cost_without_vat:.2f}".replace('.', ','))
                    row_entries[cost_without_vat_col].config(state='readonly')
                except Exception:
                    pass
                try:
                    cost_without_vat_val = float(replace_comma_with_dot(row_entries[cost_without_vat_col].get()))
                    cost_with_vat = cost_without_vat_val * 1.20
                    row_entries[cost_with_vat_col].config(state='normal')
                    row_entries[cost_with_vat_col].delete(0, tk.END)
                    row_entries[cost_with_vat_col].insert(0, f"{cost_with_vat:.2f}".replace('.', ','))
                    row_entries[cost_with_vat_col].config(state='readonly')
                except Exception:
                    pass
        except Exception:
            pass

    def add_row():
        """
        Добавляет новую строку в таблицу
        """
        nonlocal current_row
        form_values[current_row] = {}

        for col_idx, col_cfg in enumerate(columns_cfg):
            col_type = col_cfg["type"]
            width = column_widths[col_idx]

            if col_type == "index":
                lbl = tk.Label(frame, text=str(current_row), font=font_style, borderwidth=1,
                               relief="solid", width=width, padx=5, pady=5)
                lbl.grid(row=current_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                form_values[current_row][col_idx] = lbl

            elif col_type == "combobox":
                cb = ttk.Combobox(frame, font=font_style, width=width - 1, state="readonly")
                cb.grid(row=current_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                # Для первого combobox - берем ключи верхнего уровня из data_rate_all_dict
                if col_idx == 1:
                    cb['values'] = list(data_rate_all_dict.keys())
                else:
                    # Остальные из функции get_options_for_combobox (пока пусто)
                    cb['values'] = []
                cb.bind("<<ComboboxSelected>>", lambda e, r=current_row, c=col_idx: on_combobox_select(e, r, c))
                form_values[current_row][col_idx] = cb

            elif col_type == "optionmenu":
                # optionmenu заменяем на combobox readonly (для удобства)
                var = tk.StringVar()
                om = ttk.Combobox(frame, font=font_style, width=width - 1, state="readonly", textvariable=var)
                om.grid(row=current_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                om.bind("<<ComboboxSelected>>", lambda e, r=current_row, c=col_idx: on_combobox_select(e, r, c))
                form_values[current_row][col_idx] = om

            elif col_type == "readonly":
                ent = tk.Entry(frame, font=font_style, width=width, state='readonly', justify='right')
                ent.grid(row=current_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                form_values[current_row][col_idx] = ent

            elif col_type == "float_entry":
                ent = tk.Entry(frame, font=font_style, width=width, justify='right')
                ent.grid(row=current_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                ent.insert(0, '0')
                ent.bind("<FocusOut>", lambda e, r=current_row: on_validate_float(e, r))
                form_values[current_row][col_idx] = ent

        update_indices()
        current_row += 1

    def remove_last_row():
        """
        Удаляет последнюю строку из таблицы (если их > 1)
        """
        nonlocal current_row
        if current_row <= 2:
            return  # не удаляем заголовок и последнюю строку

        for widget in form_values[current_row - 1].values():
            widget.grid_forget()
            widget.destroy()
        form_values.pop(current_row - 1)
        current_row -= 1
        update_indices()
        update_totals()

    # Кнопки управления
    btn_frame = tk.Frame(parent)
    btn_frame.pack(anchor='w', padx=10, pady=5)

    add_btn = tk.Button(btn_frame, text="Добавить строку", font=font_style, bg="#69f78a", width=20, command=add_row)
    add_btn.pack(side="left", padx=10)

    remove_btn = tk.Button(btn_frame, text="Удалить строку", font=font_style, bg="#ff8787", width=20, command=remove_last_row)
    remove_btn.pack(side="left", padx=5)

    # Добавляем первую строку сразу
    add_row()

    return frame, add_row, remove_last_row

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
    table_frame_C2 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C2"],
        data_rate_all["C2"]
    )
    table_frame_C3_1 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C3_1"],
        data_rate_all["C3_1"]
    )
    return

def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
