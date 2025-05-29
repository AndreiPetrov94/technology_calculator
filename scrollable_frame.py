import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Канвас + скроллбары
        self.canvas = tk.Canvas(
            self,
            bg="#f1f1f1"
        )
        self.v_scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )
        self.h_scrollbar = tk.Scrollbar(
            self,
            orient="horizontal",
            command=self.canvas.xview
        )

        self.canvas.configure(
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )

        self.v_scrollbar.pack(
            side="right",
            fill="y"
        )
        self.h_scrollbar.pack(
            side="bottom",
            fill="x"
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Внутренний фрейм
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        # Обновление области прокрутки при изменении размеров
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Поддержка прокрутки колесиком мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
