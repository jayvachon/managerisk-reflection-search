import Tkinter as tk

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.activeVar = tk.StringVar()
        self.activeVar.set(1)

        self.canvas = tk.Canvas(self,
                                background="red",
                                borderwidth=0,
                                highlightthickness=0)
        self.vsb = tk.Scrollbar(self, orient="vertical",
command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y", expand=False)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self, background="blue")
        self.canvas.create_window(0,0,
                                  anchor="nw",
                                  window=self.inner_frame,
                                  tags=("frame",))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self._add_widgets(20)

    def _on_canvas_resize(self, event=None):
        width = self.canvas.winfo_width()
        self.canvas.itemconfigure("frame", width=width)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _add_widgets(self, count):
        bg = self.inner_frame.cget('background')
        self.inner_frame.grid_columnconfigure(2, weight=1)

        for row in xrange(1, count):
            lrb = tk.Radiobutton(self.inner_frame, text="",
                                 variable = self.activeVar,
                                 value=str(row),
                                 background=bg)
            lent1 = tk.Entry(self.inner_frame,  bg = "white")
            lent2 = tk.Entry(self.inner_frame,  bg = "white")
            lent3 = tk.Entry(self.inner_frame,  bg = "white")

            lrb.grid(row=row, column=0, pady=2)
            lent1.grid(row=row, column=1, sticky='ew', pady=2)
            lent2.grid(row=row, column=2, sticky='ew', pady=2)
            lent3.grid(row=row, column=3, sticky='ew', pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()