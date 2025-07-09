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
    headers = [col["header"] for col in columns_cfg]

    price_rate_col = value_col = cost_without_vat_col = cost_with_vat_col = index_col = None
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

    for col, header in enumerate(headers):
        label = tk.Label(frame, text=header, font=font_style, borderwidth=1, relief="solid",
                         padx=5, pady=5, width=column_widths[col])
        label.grid(row=0, column=col, sticky="nsew", padx=3, pady=3)

    form_values = {}
    current_row = 1

    totals_labels = {}

    def update_indices():
        for row_num in range(1, current_row):
            if index_col is not None and row_num in form_values:
                widget = form_values[row_num][index_col]
                if isinstance(widget, tk.Label):
                    widget.config(text=str(row_num))

    def get_nested_dict_by_path(d, path):
        cur = d
        try:
            for p in path:
                cur = cur[p]
            return cur
        except (KeyError, TypeError):
            return None

    def get_options_for_combobox(row_num, col_idx):
        selections = []
        for ci in range(1, col_idx):
            widget = form_values[row_num].get(ci)
            val = None
            if isinstance(widget, ttk.Combobox):
                val = widget.get()
            elif isinstance(widget, tuple):
                var = widget[0]
                val = var.get()
            else:
                continue
            if val == "":
                break
            selections.append(val)
        nested = get_nested_dict_by_path(data_rate_all_dict, selections)
        return list(nested.keys()) if isinstance(nested, dict) else []

    def update_optionmenu(widget_tuple, new_options):
        var, optionmenu_widget = widget_tuple
        menu = optionmenu_widget["menu"]
        menu.delete(0, "end")
        for option in new_options:
            menu.add_command(label=option, command=lambda v=option: var.set(v))
        if var.get() not in new_options:
            var.set('')

    def update_price_rate(row_num):
        selections = []
        for ci in range(1, price_rate_col):
            widget = form_values[row_num].get(ci)
            val = None
            if isinstance(widget, ttk.Combobox):
                val = widget.get()
            elif isinstance(widget, tuple):
                var = widget[0]
                val = var.get()
            else:
                continue
            if val == "":
                break
            selections.append(val)

        price = get_nested_dict_by_path(data_rate_all_dict, selections)
        price_widget = form_values[row_num].get(price_rate_col)
        if isinstance(price_widget, tk.Entry):
            price_widget.config(state='normal')
            price_widget.delete(0, tk.END)
            if isinstance(price, (int, float)):
                price_widget.insert(0, f"{price:.2f}".replace('.', ','))
            price_widget.config(state='readonly')

    def on_combobox_select(event, row_num, col_idx):
        next_col = col_idx + 1
        if next_col < price_rate_col:
            widget_next = form_values[row_num].get(next_col)
            if widget_next:
                opts = get_options_for_combobox(row_num, next_col)
                if isinstance(widget_next, ttk.Combobox):
                    widget_next['values'] = opts
                    if widget_next.get() not in opts:
                        widget_next.set('')
                    for c in range(next_col + 1, price_rate_col):
                        w = form_values[row_num].get(c)
                        if isinstance(w, ttk.Combobox):
                            w.set('')
                            w['values'] = []
                        elif isinstance(w, tuple):
                            update_optionmenu(w, [])
                            w[0].set('')
                elif isinstance(widget_next, tuple):
                    update_optionmenu(widget_next, opts)
                    for c in range(next_col + 1, price_rate_col):
                        w = form_values[row_num].get(c)
                        if isinstance(w, tuple):
                            update_optionmenu(w, [])
                            w[0].set('')
        update_price_rate(row_num)
        update_totals()

    def on_validate_float(event, row_num):
        widget = form_values[row_num].get(value_col)
        if isinstance(widget, tk.Entry):
            validate_and_format_float(event)
        update_totals()

    def update_totals():
        total_cost_without_vat = 0.0
        total_cost_with_vat = 0.0
        for row_num, row_entries in form_values.items():
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

                total_cost_without_vat += cost_without_vat_val
                total_cost_with_vat += cost_with_vat
            except Exception:
                pass

        # Обновляем строку "Итого"
        if totals_labels:
            totals_labels[cost_without_vat_col].config(text=f"{total_cost_without_vat:.2f}".replace('.', ','))
            totals_labels[cost_with_vat_col].config(text=f"{total_cost_with_vat:.2f}".replace('.', ','))

    def create_totals_row():
        # Если строка "Итого" уже есть, удаляем её
        if totals_labels:
            for widget in totals_labels.values():
                widget.grid_forget()
                widget.destroy()
            totals_labels.clear()

        total_row = current_row
        for col_idx, col_cfg in enumerate(columns_cfg):
            width = column_widths[col_idx]
            if col_cfg["type"] == "index":
                lbl = tk.Label(frame, text="", font=font_style, borderwidth=1, relief="solid",
                               width=width, padx=5, pady=5)
                lbl.grid(row=total_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                totals_labels[col_idx] = lbl
            elif col_cfg.get("key") == "price_rate":
                lbl = tk.Label(frame, text="Итого:", font=font_style, borderwidth=1, relief="solid",
                               width=width, padx=5, pady=5, anchor="e")
                lbl.grid(row=total_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                totals_labels[col_idx] = lbl
            elif col_cfg.get("key") in ("cost_without_vat", "cost_with_vat"):
                lbl = tk.Label(frame, text="0,00", font=font_style, borderwidth=1, relief="solid",
                               width=width, padx=5, pady=5, anchor="e")
                lbl.grid(row=total_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                totals_labels[col_idx] = lbl
            else:
                lbl = tk.Label(frame, text="", font=font_style, borderwidth=1, relief="solid",
                               width=width, padx=5, pady=5)
                lbl.grid(row=total_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                totals_labels[col_idx] = lbl

    def add_row():
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
                if col_idx == 1:
                    cb['values'] = list(data_rate_all_dict.keys())
                cb.bind("<<ComboboxSelected>>", lambda e, r=current_row, c=col_idx: on_combobox_select(e, r, c))
                form_values[current_row][col_idx] = cb

            elif col_type == "optionmenu":
                var = tk.StringVar()
                var.set('')
                om = tk.OptionMenu(frame, var, '')
                om.config(font=font_style, width=width)
                om.grid(row=current_row, column=col_idx, sticky="nsew", padx=3, pady=3)
                def callback(*args, r=current_row, c=col_idx):
                    on_combobox_select(None, r, c)
                var.trace_add("write", callback)
                form_values[current_row][col_idx] = (var, om)

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

        current_row += 1
        create_totals_row()
        update_indices()
        update_totals()

    def remove_last_row():
        nonlocal current_row
        if current_row <= 1:
            return
        # Удаляем строку "Итого" перед удалением строки данных
        if totals_labels:
            for widget in totals_labels.values():
                widget.grid_forget()
                widget.destroy()
            totals_labels.clear()

        # Удаляем последнюю строку данных
        for widget in form_values[current_row - 1].values():
            if isinstance(widget, tk.Widget):
                widget.grid_forget()
                widget.destroy()
            elif isinstance(widget, tuple):
                widget[1].grid_forget()
                widget[1].destroy()
        form_values.pop(current_row - 1)
        current_row -= 1
        create_totals_row()
        update_indices()
        update_totals()

    btn_frame = tk.Frame(parent)
    btn_frame.pack(anchor='w', padx=10, pady=5)
    add_btn = tk.Button(btn_frame, text="Добавить строку", font=font_style, bg="#69f78a", width=20, command=add_row)
    add_btn.pack(side="left", padx=10)
    remove_btn = tk.Button(btn_frame, text="Удалить строку", font=font_style, bg="#ff8787", width=20, command=remove_last_row)
    remove_btn.pack(side="left", padx=5)

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
