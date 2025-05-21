import tkinter as tk
from tkinter import messagebox

BASE_COST = 1000
COST_PER_KM = 100

class ConnectionCostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор стоимости подключения")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Заголовки таблицы
        # tk.Label(root, text="Расстояние до точки подключения (м):").pack(pady=5)
        tk.Label(root, text="Название точки").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Расстояние (км)").grid(row=0, column=1, padx=10, pady=5)

        # Таблица ввода (по умолчанию 3 строки)
        self.entries = []
        for i in range(3):
            name_entry = tk.Entry(root)
            name_entry.grid(row=i + 1, column=0, padx=10, pady=5)

            distance_entry = tk.Entry(root)
            distance_entry.grid(row=i + 1, column=1, padx=10, pady=5)

            self.entries.append((name_entry, distance_entry))

        # Кнопка добавить строку
        self.add_row_button = tk.Button(root, text="Добавить строку", command=self.add_row)
        self.add_row_button.grid(row=4, column=0, pady=10)

        # Кнопка рассчитать
        self.calc_button = tk.Button(root, text="Рассчитать стоимость", command=self.calculate_cost)
        self.calc_button.grid(row=4, column=1, pady=10)

        # Метка результата
        self.result_label = tk.Label(root, text="Итоговая стоимость: ...", font=("Arial", 12))
        self.result_label.grid(row=5, column=0, columnspan=2, pady=15)

    def add_row(self):
        row = len(self.entries) + 1
        name_entry = tk.Entry(self.root)
        name_entry.grid(row=row, column=0, padx=10, pady=5)

        distance_entry = tk.Entry(self.root)
        distance_entry.grid(row=row, column=1, padx=10, pady=5)

        self.entries.append((name_entry, distance_entry))

    def calculate_cost(self):
        total_distance = 0.0
        for name_entry, dist_entry in self.entries:
            if dist_entry.get().strip():
                try:
                    km = float(dist_entry.get())
                    total_distance += km
                except ValueError:
                    messagebox.showerror("Ошибка ввода", f"Некорректное значение расстояния: {dist_entry.get()}")
                    return

        total_cost = BASE_COST + (total_distance * COST_PER_KM)
        self.result_label.config(text=f"Итоговая стоимость: {total_cost:.2f} руб.")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectionCostApp(root)
    root.mainloop()
