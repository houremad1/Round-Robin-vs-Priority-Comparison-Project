import customtkinter as ctk
import tkinter as tk
from src.util.constants import *
from src.gui.widgets import GanttCanvas, ResultsMiniTable


class ComparisonTab(ctk.CTkScrollableFrame):
    METRICS = [
        ("average_waiting_time", "Avg Waiting Time", ORANGE),
        ("average_turnaround_time", "Avg Turnaround Time", GREEN),
        ("average_response_time", "Avg Response Time", PURPLE),
    ]

    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color=BG, corner_radius=0, **kw)
        self._rr_data = None
        self._pp_data = None
        self._build()

    def _build(self):
        title_f = ctk.CTkFrame(self, fg_color=BG2, corner_radius=12)
        title_f.pack(fill="x", padx=4, pady=(6,8))
        ctk.CTkLabel(
            title_f,
            text="Round Robin vs Priority Scheduling — Comparison",
            font=ctk.CTkFont("Consolas",14,"bold"),
            text_color=FG
        ).pack(side="left", padx=16, pady=12)

        self.status_lbl = ctk.CTkLabel(
            title_f,
            text="Run both algorithms to populate this report",
            font=ctk.CTkFont("Consolas",9),
            text_color=FG2
        )
        self.status_lbl.pack(side="right", padx=16)

        # Gantt Charts Row
        g_row = ctk.CTkFrame(self, fg_color="transparent")
        g_row.pack(fill="x", padx=4, pady=(0,8))
        g_row.columnconfigure(0, weight=1)
        g_row.columnconfigure(1, weight=1)

        self.rr_gantt = GanttCanvas(g_row, "⬤ Round Robin — Gantt Chart")
        self.rr_gantt.grid(row=0, column=0, sticky="ew", padx=(0,4))

        self.pp_gantt = GanttCanvas(g_row, "⬤ Priority PP — Gantt Chart")
        self.pp_gantt.grid(row=0, column=1, sticky="ew", padx=(4,0))

        # Results Tables Row
        r_row = ctk.CTkFrame(self, fg_color="transparent")
        r_row.pack(fill="x", padx=4, pady=(0,8))
        r_row.columnconfigure(0, weight=1)
        r_row.columnconfigure(1, weight=1)

        # Round Robin Card
        rr_card = ctk.CTkFrame(r_row, fg_color=BG2, corner_radius=10)
        rr_card.grid(row=0, column=0, sticky="ew", padx=(0,4))
        ctk.CTkLabel(
            rr_card,
            text="Round Robin — Results",
            font=ctk.CTkFont("Consolas",11,"bold"),
            text_color=ACCENT2
        ).pack(anchor="w", padx=12, pady=(8,0))
        self.rr_table = ResultsMiniTable(rr_card)
        self.rr_table.pack(fill="x")

        # Priority Card
        pp_card = ctk.CTkFrame(r_row, fg_color=BG2, corner_radius=10)
        pp_card.grid(row=0, column=1, sticky="ew", padx=(4,0))
        ctk.CTkLabel(
            pp_card,
            text="Priority PP — Results",
            font=ctk.CTkFont("Consolas",11,"bold"),
            text_color=ACCENT
        ).pack(anchor="w", padx=12, pady=(8,0))
        self.pp_table = ResultsMiniTable(pp_card)
        self.pp_table.pack(fill="x")

        # Metric Comparison
        cmp_card = ctk.CTkFrame(self, fg_color=BG2, corner_radius=12)
        cmp_card.pack(fill="x", padx=4, pady=(0,8))
        ctk.CTkLabel(
            cmp_card,
            text=" Metric Comparison",
            font=ctk.CTkFont("Consolas",13,"bold"),
            text_color=FG
        ).pack(anchor="w", padx=14, pady=(10,6))

        hf = ctk.CTkFrame(cmp_card, fg_color=BG3, corner_radius=8, height=34)
        hf.pack(fill="x", padx=10, pady=(0,4))
        hf.pack_propagate(False)
        for txt, col, w, anc in [
            ("Metric",FG2,200,"w"),
            ("Round Robin",ACCENT2,140,"center"),
            ("Priority PP",ACCENT,140,"center"),
            ("Winner",GREEN,130,"center"),
            ("Note",FG2,220,"w")
        ]:
            ctk.CTkLabel(
                hf, text=txt, width=w, anchor=anc,
                font=ctk.CTkFont("Consolas",10,"bold"),
                text_color=col
            ).pack(side="left", padx=3, pady=3)

        self.metric_rows = {}
        notes = {
            "average_waiting_time":"lower is better",
            "average_turnaround_time":"lower is better",
            "average_response_time":"lower is better"
        }

        for key, label, color in self.METRICS:
            row = ctk.CTkFrame(cmp_card, fg_color=BG3, corner_radius=6, height=38)
            row.pack(fill="x", padx=8, pady=1)
            row.pack_propagate(False)

            name_f = ctk.CTkFrame(row, fg_color="transparent", width=160)
            name_f.pack(side="left", padx=6, pady=8)
            name_f.pack_propagate(False)
            d = tk.Canvas(name_f, width=10, height=10, bg=BG3, highlightthickness=0)
            d.create_oval(1,1,9,9, fill=color, outline="")
            d.pack(side="left")
            ctk.CTkLabel(
                name_f,
                text=f" {label}",
                font=ctk.CTkFont("Consolas",10),
                text_color=FG
            ).pack(side="left")

            rr_v = ctk.CTkLabel(row, text="—", width=140, anchor="center",
                                 font=ctk.CTkFont("Consolas",11,"bold"),
                                 text_color=ACCENT2)
            rr_v.pack(side="left", padx=2)

            pp_v = ctk.CTkLabel(row, text="—", width=140, anchor="center",
                                 font=ctk.CTkFont("Consolas",11,"bold"),
                                 text_color=ACCENT)
            pp_v.pack(side="left", padx=2)

            win = ctk.CTkLabel(row, text="—", width=130, anchor="center",
                               font=ctk.CTkFont("Consolas",11,"bold"),
                               text_color=FG2)
            win.pack(side="left", padx=2)

            ctk.CTkLabel(
                row,
                text=notes[key],
                width=220,
                anchor="w",
                font=ctk.CTkFont("Consolas",9),
                text_color=FG2
            ).pack(side="left", padx=6)

            self.metric_rows[key] = (rr_v, pp_v, win)

        # Analysis Section
        self.analysis_box = ctk.CTkFrame(self, fg_color=BG2, corner_radius=12)
        self.analysis_box.pack(fill="x", padx=4, pady=(0,8))
        ctk.CTkLabel(
            self.analysis_box,
            text="Algorithm Analysis",
            font=ctk.CTkFont("Consolas",13,"bold"),
            text_color=FG
        ).pack(anchor="w", padx=14, pady=(10,6))

        self.analysis_text = ctk.CTkLabel(
            self.analysis_box,
            text="— Run both algorithms to generate analysis —",
            justify="left",
            wraplength=900,
            font=ctk.CTkFont("Consolas",10),
            text_color=FG2
        )
        self.analysis_text.pack(anchor="w", padx=14, pady=(0,10))

    def set_rr(self, timeline, results, averages):
        self._rr_data = (timeline, results, averages)
        self.rr_gantt.draw(timeline)
        self.rr_table.fill(results)
        self._refresh()

    def set_pp(self, timeline, results, averages):
        self._pp_data = (timeline, results, averages)
        self.pp_gantt.draw(timeline)
        self.pp_table.fill(results)
        self._refresh()

    def reset(self):
        self._rr_data = self._pp_data = None
        self.rr_gantt.clear()
        self.pp_gantt.clear()
        self.rr_table.clear()
        self.pp_table.clear()
        for rr_v, pp_v, win in self.metric_rows.values():
            rr_v.configure(text="—", text_color=ACCENT2)
            pp_v.configure(text="—", text_color=ACCENT)
            win.configure(text="—", text_color=FG2)
        self.analysis_text.configure(
            text="— Run both algorithms to generate analysis —",
            text_color=FG2
        )
        self.status_lbl.configure(
            text="Run both algorithms to populate this report"
        )

    def _refresh(self):
        rr = self._rr_data
        pp = self._pp_data
        rr_avg = rr[2] if rr else None
        pp_avg = pp[2] if pp else None
        both = rr_avg is not None and pp_avg is not None

        for key, (rr_v, pp_v, win) in self.metric_rows.items():
            rv = rr_avg[key] if rr_avg else None
            pv = pp_avg[key] if pp_avg else None
            rr_v.configure(text=f"{rv:.2f}" if rv is not None else "—")
            pp_v.configure(text=f"{pv:.2f}" if pv is not None else "—")
            if both:
                if rv < pv:
                    win.configure(text="✓ RR", text_color=ACCENT2)
                elif pv < rv:
                    win.configure(text="✓ PP", text_color=ACCENT)
                else:
                    win.configure(text="Tie", text_color=FG2)
            else:
                win.configure(text="—")

        if both:
            self._generate_analysis(rr_avg, pp_avg)
            self.status_lbl.configure(text="Both algorithms completed")
        else:
            self.status_lbl.configure(text="Run both algorithms to complete comparison")

    def _generate_analysis(self, rr_avg, pp_avg):
        text = """Fairness vs Urgency:
• Round Robin is fair (equal CPU time sharing).
• Priority is urgency-based (important tasks first).

Execution Order:
• Priority changes execution dynamically based on priority.
• RR keeps cyclic order regardless of priority.

Urgent Process Benefit:
• Priority scheduling benefits high priority processes more.

Starvation Risk:
• Low priority processes may starve in Priority scheduling.

Fairness:
• Round Robin provides more balanced CPU distribution."""
        self.analysis_text.configure(text=text, text_color=FG)
