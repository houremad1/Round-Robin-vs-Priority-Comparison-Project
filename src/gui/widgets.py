import tkinter as tk
import customtkinter as ctk

from src.util.constants import *
from src.util.helpers import _pid_idx , _section_label

# class ResultsMiniTable(ctk.CTkFrame):
#     def __init__(self, parent, **kw):
#         super().__init__(parent, fg_color="transparent", **kw)
#         hf = ctk.CTkFrame(self, fg_color=BG3, corner_radius=6)
#         hf.pack(fill="x", padx=10, pady=(4,0))
#         for h, w in zip(RHEADS, RWIDTHS):
#             ctk.CTkLabel(hf, text=h, font=ctk.CTkFont("Consolas",9,"bold"),
#                          text_color=ACCENT2, width=w).pack(side="left", padx=3, pady=5)
#         self.rows = ctk.CTkScrollableFrame(self, fg_color="transparent", height=95)
#         self.rows.pack(fill="x", padx=10, pady=(2,6))
#
#     def fill(self, results):
#         for w in self.rows.winfo_children(): w.destroy()
#         for r in results:
#             row = ctk.CTkFrame(self.rows, fg_color=BG3, corner_radius=5)
#             row.pack(fill="x", pady=1)
#             for key, w in zip(RCOLS, RWIDTHS):
#                 ctk.CTkLabel(row, text=str(r.get(key,"—")), width=w,
#                              font=ctk.CTkFont("Consolas",9),
#                              text_color=RCMAP.get(key, FG)).pack(side="left", padx=3, pady=4)
#
#     def clear(self):
#         for w in self.rows.winfo_children(): w.destroy()
# class ProcessTableCell(ctk.CTkFrame):
#     def __init__(self, parent, app, **kw):
#         super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
#         self.app = app; self._build()
#
#     def _build(self):
#         hrow = ctk.CTkFrame(self, fg_color="transparent")
#         hrow.pack(fill="x", padx=14, pady=8)
#         ctk.CTkLabel(hrow, text="Process Table",
#                      font=ctk.CTkFont("Consolas",13,"bold"), text_color=FG).pack(side="left")
#         for txt, cmd, col in [("+ Add", self.app._add_process, ACCENT2),
#                                ("✕ Clear All", self.app._clear_all, ACCENT)]:
#             ctk.CTkButton(hrow, text=txt, width=80, height=26, fg_color=col,
#                           hover_color="#1e3a4f" if col==ACCENT2 else BG,
#                           font=ctk.CTkFont("Consolas",9), corner_radius=6,
#                           command=cmd).pack(side="right", padx=3)
#         hf = ctk.CTkFrame(self, fg_color=BG3, corner_radius=0)
#         hf.pack(fill="x", padx=14)
#         for c in ["Process ID","Arrival Time","Burst Time","Priority"]:
#             ctk.CTkLabel(hf, text=c, font=ctk.CTkFont("Consolas",10,"bold"),
#                          text_color=ACCENT2, width=100).pack(side="left", padx=6, pady=5)
#         self.table_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=140)
#         self.table_frame.pack(fill="x", padx=14, pady=(0,8))
#
#     def refresh(self):
#         for w in self.table_frame.winfo_children(): w.destroy()
#         for p in self.app.processes:
#             row = ctk.CTkFrame(self.table_frame, fg_color=BG3, corner_radius=6)
#             row.pack(fill="x", pady=2)
#             idx = _pid_idx(p["pid"])
#             d = tk.Canvas(row, width=10, height=10, bg=BG3, highlightthickness=0)
#             d.create_oval(1,1,9,9, fill=PROC_COLORS[idx % len(PROC_COLORS)], outline="")
#             d.pack(side="left", padx=(10,4), pady=7)
#             for val in [p["pid"], p["arrival"], p["burst"], p["priority"]]:
#                 ctk.CTkLabel(row, text=str(val), width=90,
#                              font=ctk.CTkFont("Consolas",10), text_color=FG).pack(side="left", padx=6)
#             pp = p
#             ctk.CTkButton(row, text="✎", width=28, height=22, fg_color="transparent",
#                           hover_color=BG, font=ctk.CTkFont("Consolas",11), text_color=ACCENT2,
#                           command=lambda x=pp: self.app._edit_process(x)).pack(side="right", padx=4)
#             ctk.CTkButton(row, text="✕", width=28, height=22, fg_color="transparent",
#                           hover_color=BG, font=ctk.CTkFont("Consolas",11), text_color=ACCENT,
#                           command=lambda x=pp: self.app._del_process(x)).pack(side="right", padx=2)
# class GanttCell(ctk.CTkFrame):
#     def __init__(self, parent, label="Gantt Chart", **kw):
#         super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
#
#         ctk.CTkLabel(
#             self,
#             text=label,
#             font=ctk.CTkFont("Consolas", 12, "bold"),
#             text_color=ACCENT
#         ).pack(anchor="w", padx=14, pady=(8,4))
#
#         # Frame holds canvas + scrollbar
#         canvas_frame = ctk.CTkFrame(self, fg_color="transparent")
#         canvas_frame.pack(fill="x", padx=14, pady=(0,8))
#
#         # Canvas
#         self.canvas = tk.Canvas(
#             canvas_frame,
#             bg=BG3,
#             height=76,
#             highlightthickness=0
#         )
#         self.canvas.pack(side="top", fill="x", expand=True)
#
#         self.scroll_x = tk.Scrollbar(
#             canvas_frame,
#             orient="horizontal",
#             command=self.canvas.xview
#         )
#         self.scroll_x.pack(side="bottom", fill="x")
#
#         self.canvas.configure(xscrollcommand=self.scroll_x.set)
#
#     def draw(self, timeline):
#         self.canvas.delete("all")
#
#         if not timeline:
#             return
#
#         total = timeline[-1]["end"]
#         if total == 0:
#             return
#
#         y1, y2 = 8, 50
#         chart_width = max(total * 60, 900)
#
#         for seg in timeline:
#             col = PROC_COLORS[_pid_idx(seg["pid"]) % len(PROC_COLORS)]
#
#             x1 = int(seg["start"] / total * chart_width)
#             x2 = int(seg["end"]   / total * chart_width)
#
#             self.canvas.create_rectangle(
#                 x1, y1, x2, y2,
#                 fill=col,
#                 outline=BG3,
#                 width=1
#             )
#
#             if x2 - x1 > 18:
#                 self.canvas.create_text(
#                     (x1+x2)//2,
#                     (y1+y2)//2,
#                     text=seg["pid"],
#                     fill="white",
#                     font=("Consolas",9,"bold")
#                 )
#
#         shown = set()
#
#         for seg in timeline:
#             for t in [seg["start"], seg["end"]]:
#                 if t not in shown:
#                     x = int(t / total * chart_width)
#
#                     self.canvas.create_line(x, y2, x, y2+5, fill=FG2)
#
#                     self.canvas.create_text(
#                         x,
#                         70,
#                         text=str(t),
#                         fill=FG2,
#                         font=("Consolas",8)
#                     )
#
#                     shown.add(t)
#
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
#     def clear(self):
#         self.canvas.delete("all")
# class ResultsCell(ctk.CTkFrame):
#     def __init__(self, parent, **kw):
#         super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
#         hf = ctk.CTkFrame(self, fg_color=BG3, corner_radius=8)
#         hf.pack(fill="x", padx=14, pady=(10,0))
#         for h, w in zip(RHEADS, RWIDTHS):
#             ctk.CTkLabel(hf, text=h, font=ctk.CTkFont("Consolas",9,"bold"),
#                          text_color=ACCENT2, width=w).pack(side="left", padx=4, pady=6)
#         self.res_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
#         self.res_frame.pack(fill="both", expand=True, padx=14, pady=(2,8))
#
#     def fill(self, results):
#         for w in self.res_frame.winfo_children(): w.destroy()
#         for r in results:
#             row = ctk.CTkFrame(self.res_frame, fg_color=BG3, corner_radius=6)
#             row.pack(fill="x", pady=2)
#             for key, w in zip(RCOLS, RWIDTHS):
#                 ctk.CTkLabel(row, text=str(r.get(key,"—")), width=w,
#                              font=ctk.CTkFont("Consolas",10),
#                              text_color=RCMAP.get(key, FG)).pack(side="left", padx=4, pady=5)
#
#     def clear(self):
#         for w in self.res_frame.winfo_children(): w.destroy()
# class SidebarCell(ctk.CTkScrollableFrame):



class GanttCanvas(ctk.CTkFrame):
    def __init__(self, parent, label, **kw):
        super().__init__(parent, fg_color=BG2, corner_radius=10, **kw)
        ctk.CTkLabel(self, text=label,
                     font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=12, pady=(8,2))
        self.canvas = tk.Canvas(self, bg=BG3, height=74, highlightthickness=0)
        self.canvas.pack(fill="x", padx=12, pady=(0,8))

    def draw(self, timeline):
        self.canvas.delete("all")
        if not timeline: return
        self.canvas.update_idletasks()
        W = self.canvas.winfo_width() or 600
        total = timeline[-1]["end"]
        if total == 0: return
        y1, y2 = 8, 50
        for seg in timeline:
            col = PROC_COLORS[_pid_idx(seg["pid"]) % len(PROC_COLORS)]
            x1 = int(seg["start"] / total * W)
            x2 = int(seg["end"] / total * W)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=col, outline=BG3, width=1)
            if x2 - x1 > 18:
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                        text=seg["pid"], fill="white",
                                        font=("Consolas",9,"bold"))
        shown = set()
        for seg in timeline:
            for t in [seg["start"], seg["end"]]:
                if t not in shown:
                    x = int(t / total * W)
                    self.canvas.create_line(x, y2, x, y2+5, fill=FG2)
                    self.canvas.create_text(x, 68, text=str(t), fill=FG2, font=("Consolas",8))
                    shown.add(t)

    def clear(self): self.canvas.delete("all")


class ResultsMiniTable(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        hf = ctk.CTkFrame(self, fg_color=BG3, corner_radius=6)
        hf.pack(fill="x", padx=10, pady=(4,0))
        for h, w in zip(RHEADS, RWIDTHS):
            ctk.CTkLabel(hf, text=h, font=ctk.CTkFont("Consolas",9,"bold"),
                         text_color=ACCENT2, width=w).pack(side="left", padx=3, pady=5)
        self.rows = ctk.CTkScrollableFrame(self, fg_color="transparent", height=95)
        self.rows.pack(fill="x", padx=10, pady=(2,6))

    def fill(self, results):
        for w in self.rows.winfo_children(): w.destroy()
        for r in results:
            row = ctk.CTkFrame(self.rows, fg_color=BG3, corner_radius=5)
            row.pack(fill="x", pady=1)
            for key, w in zip(RCOLS, RWIDTHS):
                ctk.CTkLabel(row, text=str(r.get(key,"—")), width=w,
                             font=ctk.CTkFont("Consolas",9),
                             text_color=RCMAP.get(key, FG)).pack(side="left", padx=3, pady=4)

    def clear(self):
        for w in self.rows.winfo_children(): w.destroy()


class ProcessTableCell(ctk.CTkFrame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
        self.app = app
        self._build()

    def _build(self):
        hrow = ctk.CTkFrame(self, fg_color="transparent")
        hrow.pack(fill="x", padx=14, pady=8)
        ctk.CTkLabel(hrow, text="Process Table",
                     font=ctk.CTkFont("Consolas",13,"bold"), text_color=FG).pack(side="left")
        for txt, cmd, col in [("+ Add", self.app._add_process, ACCENT2),
                               ("✕ Clear All", self.app._clear_all, ACCENT)]:
            ctk.CTkButton(hrow, text=txt, width=80, height=26, fg_color=col,
                          hover_color="#1e3a4f" if col==ACCENT2 else BG,
                          font=ctk.CTkFont("Consolas",9), corner_radius=6,
                          command=cmd).pack(side="right", padx=3)

        hf = ctk.CTkFrame(self, fg_color=BG3, corner_radius=0)
        hf.pack(fill="x", padx=14)
        for c in ["Process ID","Arrival Time","Burst Time","Priority"]:
            ctk.CTkLabel(hf, text=c, font=ctk.CTkFont("Consolas",10,"bold"),
                         text_color=ACCENT2, width=100).pack(side="left", padx=6, pady=5)

        self.table_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=140)
        self.table_frame.pack(fill="x", padx=14, pady=(0,8))

    def refresh(self):
        for w in self.table_frame.winfo_children(): w.destroy()
        for p in self.app.processes:
            row = ctk.CTkFrame(self.table_frame, fg_color=BG3, corner_radius=6)
            row.pack(fill="x", pady=2)
            idx = _pid_idx(p["pid"])
            d = tk.Canvas(row, width=10, height=10, bg=BG3, highlightthickness=0)
            d.create_oval(1,1,9,9, fill=PROC_COLORS[idx % len(PROC_COLORS)], outline="")
            d.pack(side="left", padx=(10,4), pady=7)
            for val in [p["pid"], p["arrival"], p["burst"], p["priority"]]:
                ctk.CTkLabel(row, text=str(val), width=90,
                             font=ctk.CTkFont("Consolas",10), text_color=FG).pack(side="left", padx=6)
            pp = p
            ctk.CTkButton(row, text="✎", width=28, height=22, fg_color="transparent",
                          hover_color=BG, font=ctk.CTkFont("Consolas",11), text_color=ACCENT2,
                          command=lambda x=pp: self.app._edit_process(x)).pack(side="right", padx=4)
            ctk.CTkButton(row, text="✕", width=28, height=22, fg_color="transparent",
                          hover_color=BG, font=ctk.CTkFont("Consolas",11), text_color=ACCENT,
                          command=lambda x=pp: self.app._del_process(x)).pack(side="right", padx=2)


class GanttCell(ctk.CTkFrame):
    def __init__(self, parent, label="Gantt Chart", **kw):
        super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
        ctk.CTkLabel(self, text=label, font=ctk.CTkFont("Consolas", 12, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=14, pady=(8,4))

        canvas_frame = ctk.CTkFrame(self, fg_color="transparent")
        canvas_frame.pack(fill="x", padx=14, pady=(0,8))

        self.canvas = tk.Canvas(canvas_frame, bg=BG3, height=76, highlightthickness=0)
        self.canvas.pack(side="top", fill="x", expand=True)

        self.scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scroll_x.set)

    def draw(self, timeline):
        self.canvas.delete("all")
        if not timeline: return
        total = timeline[-1]["end"]
        if total == 0: return
        y1, y2 = 8, 50
        chart_width = max(total * 60, 900)

        for seg in timeline:
            col = PROC_COLORS[_pid_idx(seg["pid"]) % len(PROC_COLORS)]
            x1 = int(seg["start"] / total * chart_width)
            x2 = int(seg["end"] / total * chart_width)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=col, outline=BG3, width=1)
            if x2 - x1 > 18:
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                        text=seg["pid"], fill="white",
                                        font=("Consolas",9,"bold"))

        shown = set()
        for seg in timeline:
            for t in [seg["start"], seg["end"]]:
                if t not in shown:
                    x = int(t / total * chart_width)
                    self.canvas.create_line(x, y2, x, y2+5, fill=FG2)
                    self.canvas.create_text(x, 70, text=str(t), fill=FG2, font=("Consolas",8))
                    shown.add(t)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear(self): self.canvas.delete("all")


class ResultsCell(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
        hf = ctk.CTkFrame(self, fg_color=BG3, corner_radius=8)
        hf.pack(fill="x", padx=14, pady=(10,0))
        for h, w in zip(RHEADS, RWIDTHS):
            ctk.CTkLabel(hf, text=h, font=ctk.CTkFont("Consolas",9,"bold"),
                         text_color=ACCENT2, width=w).pack(side="left", padx=4, pady=6)

        self.res_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.res_frame.pack(fill="both", expand=True, padx=14, pady=(2,8))

    def fill(self, results):
        for w in self.res_frame.winfo_children(): w.destroy()
        for r in results:
            row = ctk.CTkFrame(self.res_frame, fg_color=BG3, corner_radius=6)
            row.pack(fill="x", pady=2)
            for key, w in zip(RCOLS, RWIDTHS):
                ctk.CTkLabel(row, text=str(r.get(key,"—")), width=w,
                             font=ctk.CTkFont("Consolas",10),
                             text_color=RCMAP.get(key, FG)).pack(side="left", padx=4, pady=5)

    def clear(self):
        for w in self.res_frame.winfo_children(): w.destroy()


class StatCardsCell(ctk.CTkFrame):
    CARDS = [("avg_wait", "Avg Waiting", ACCENT2),
             ("avg_tat", "Avg Turnaround", GREEN),
             ("avg_resp", "Avg Response", PURPLE)]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=BG2, corner_radius=12, **kw)
        self.labels = {}
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=10)
        for key, title, col in self.CARDS:
            card = ctk.CTkFrame(row, fg_color=BG3, corner_radius=10)
            card.pack(side="left", expand=True, fill="x", padx=4)
            ctk.CTkFrame(card, fg_color=col, height=3, corner_radius=2).pack(fill="x")
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont("Consolas",8), text_color=FG2).pack(pady=(6,1))
            lbl = ctk.CTkLabel(card, text="—", font=ctk.CTkFont("Consolas",17,"bold"), text_color=col)
            lbl.pack(pady=(0,8)); self.labels[key] = lbl

    def update(self, averages, results):
        self.labels["avg_wait"].configure(text=f"{averages['average_waiting_time']:.2f}")
        self.labels["avg_tat"].configure(text=f"{averages['average_turnaround_time']:.2f}")
        self.labels["avg_resp"].configure(text=f"{averages['average_response_time']:.2f}")

    def reset(self):
        for lbl in self.labels.values(): lbl.configure(text="—")


class SidebarCell(ctk.CTkScrollableFrame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, fg_color=BG2, width=260, corner_radius=12, **kw)
        self.app = app
        self._build()

    def _build(self):
        _section_label(self, "Algorithm Settings")
        ctk.CTkLabel(self, text="Time Quantum (ms)",
                     font=ctk.CTkFont("Consolas",10), text_color=FG2).pack(anchor="w", padx=12)
        qf = ctk.CTkFrame(self, fg_color="transparent"); qf.pack(fill="x", padx=12, pady=4)
        self.quantum_entry = ctk.CTkEntry(qf, width=80, justify="center",
                                          font=ctk.CTkFont("Consolas",12),
                                          fg_color=BG3, border_color=BG3, text_color=FG)
        self.quantum_entry.insert(0, "3"); self.quantum_entry.pack(side="left")

        ctk.CTkButton(self, text="▶ Run Simulation",
                      font=ctk.CTkFont("Consolas",12,"bold"),
                      fg_color=ACCENT, hover_color="#c1121f",
                      corner_radius=8, height=40, command=self.app._run
                      ).pack(fill="x", padx=12, pady=(12,4))

        ctk.CTkButton(self, text="⟳ Reset",
                      font=ctk.CTkFont("Consolas",10), fg_color=BG3,
                      hover_color=BG, corner_radius=8, height=32, text_color=FG,
                      command=self.app._reset).pack(fill="x", padx=12, pady=(0,6))

        ctk.CTkFrame(self, fg_color=BG3, height=1).pack(fill="x", padx=12, pady=8)
        _section_label(self, "Quick Info")
        for t in ["• RR: Each process gets a fixed time slice in turn.",
                  "• Priority: Higher-priority processes run first."]:
            ctk.CTkLabel(self, text=t, wraplength=220, justify="left",
                         font=ctk.CTkFont("Consolas",9), text_color=FG2).pack(anchor="w", padx=12, pady=1)