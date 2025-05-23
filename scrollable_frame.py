import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Обертка
        container = tk.Frame(self)
        container.pack(
            fill='both',
            expand=True
        )

        # Канвас
        self.canvas = tk.Canvas(container)
        self.canvas.pack(
            side='left',
            fill='both',
            expand=True
        )

        # Скроллбары
        v_scrollbar = tk.Scrollbar(
            container,
            orient='vertical',
            command=self.canvas.yview
        )
        v_scrollbar.pack(
            side='right',
            fill='y'
        )

        h_scrollbar = tk.Scrollbar(
            self,
            orient='horizontal',
            command=self.canvas.xview
        )
        h_scrollbar.pack(
            side='bottom',
            fill='x'
        )

        # Настройка канваса
        self.canvas.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )

        # Вложенный фрейм
        self.main_frame = tk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor='nw'
        )

        # Прокрутка колесиком
        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

        self.main_frame.bind(
            "<Configure>",
            self._on_frame_configure
        )

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
