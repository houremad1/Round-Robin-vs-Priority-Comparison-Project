import tkinter as tk
import customtkinter as ctk

from src.util.constants import *
from src.util.helpers import _pid_idx

class GanttCell(ctk.CTkFrame):
    def __init__(self, parent, label="Gantt Chart", **kw):
        super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)

        ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont("Consolas", 12, "bold"),
            text_color=ACCENT
        ).pack(anchor="w", padx=14, pady=(8,4))

        # Frame holds canvas + scrollbar
        canvas_frame = ctk.CTkFrame(self, fg_color="transparent")
        canvas_frame.pack(fill="x", padx=14, pady=(0,8))

        # Canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            bg=BG3,
            height=76,
            highlightthickness=0
        )
        self.canvas.pack(side="top", fill="x", expand=True)

        self.scroll_x = tk.Scrollbar(
            canvas_frame,
            orient="horizontal",
            command=self.canvas.xview
        )
        self.scroll_x.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scroll_x.set)

    def draw(self, timeline):
        self.canvas.delete("all")

        if not timeline:
            return

        total = timeline[-1]["end"]
        if total == 0:
            return

        y1, y2 = 8, 50
        chart_width = max(total * 60, 900)

        for seg in timeline:
            col = PROC_COLORS[_pid_idx(seg["pid"]) % len(PROC_COLORS)]

            x1 = int(seg["start"] / total * chart_width)
            x2 = int(seg["end"]   / total * chart_width)

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=col,
                outline=BG3,
                width=1
            )

            if x2 - x1 > 18:
                self.canvas.create_text(
                    (x1+x2)//2,
                    (y1+y2)//2,
                    text=seg["pid"],
                    fill="white",
                    font=("Consolas",9,"bold")
                )

        shown = set()

        for seg in timeline:
            for t in [seg["start"], seg["end"]]:
                if t not in shown:
                    x = int(t / total * chart_width)

                    self.canvas.create_line(x, y2, x, y2+5, fill=FG2)

                    self.canvas.create_text(
                        x,
                        70,
                        text=str(t),
                        fill=FG2,
                        font=("Consolas",8)
                    )

                    shown.add(t)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear(self):
        self.canvas.delete("all")
