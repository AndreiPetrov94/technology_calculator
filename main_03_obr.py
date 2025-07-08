import tkinter as tk
from scrollable_frame import ScrollableFrame
from form_config_03 import data_rate, data_rate_all

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
            try:
                cost_rate_val = float(replace_comma_with_dot(row_entries[cost_rate_col].get()))
                length_val = float(replace_comma_with_dot(row_entries[length_col].get()))
                cost_without_vat = cost_rate_val * length_val
                row_entries[cost_without_vat_col].delete(0, tk.END)
                row_entries[cost_without_vat_col].insert(0, f"{cost_without_vat:.2f}".replace('.', ','))
            except Exception:
                pass
            try:
                cost_without_vat_val = float(replace_comma_with_dot(row_entries[cost_without_vat_col].get()))
                cost_with_vat = cost_without_vat_val * 1.20
                row_entries[cost_with_vat_col].delete(0, tk.END)
                row_entries[cost_with_vat_col].insert(0, f"{cost_with_vat:.2f}".replace('.', ','))
            except Exception:
                pass
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
    table_frame_C2 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C2"]
    )
    table_frame_C3_1 = create_dynamic_table_with_headers(
        scrollable.scrollable_frame,
        data_rate["C3_1"]
    )
    return

def main():
    root = create_main_window()
    setup_interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
