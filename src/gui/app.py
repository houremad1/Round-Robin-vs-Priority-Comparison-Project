import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import copy

from src.scheduler.round_robin import roundRobin
from src.scheduler.priority_preemptive import preemptivePriority
from src.gui.widgets import *
from src.gui.widgets import GanttCell
from src.gui.comparision import ComparisonTab



class OSSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OS Scheduler")
        self.geometry("1360x980")
        self.configure(fg_color=BG)
        self.processes = []
        self.algorithm = "Round Robin"
        self.next_pid = 1
        self._last_rr = None
        self._last_pp = None
        self._build_ui()
        self._load_defaults()

    def _build_ui(self):
        hdr = ctk.CTkFrame(self, fg_color=BG2, height=60, corner_radius=0)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="⚙ OS Scheduler",
                     font=ctk.CTkFont("Consolas",20,"bold"),
                     text_color=ACCENT).pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(hdr, text="CPU Scheduling Simulator",
                     font=ctk.CTkFont("Consolas",10),
                     text_color=FG2).pack(side="left", pady=(14,0))

        self.algo_seg = ctk.CTkSegmentedButton(
            hdr, values=[RR_LABEL, PP_LABEL], command=self._on_algo_change,
            font=ctk.CTkFont("Consolas",11),
            selected_color=ACCENT, selected_hover_color="#c1121f",
            unselected_color=BG3, fg_color=BG3, text_color=FG)
        self.algo_seg.set(RR_LABEL)
        self.algo_seg.pack(side="right", padx=20, pady=10)

        self.tabs = ctk.CTkTabview(
            self, fg_color=BG,
            segmented_button_fg_color=BG2,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color="#c1121f",
            segmented_button_unselected_color=BG3,
            text_color=FG, corner_radius=0)
        self.tabs.pack(fill="both", expand=True, padx=6, pady=4)

        sim_tab = self.tabs.add(" Simulator ")
        cmp_tab = self.tabs.add(" Comparison ")

        # Simulator tab
        sim_tab.columnconfigure(1, weight=1)
        sim_tab.rowconfigure(0, weight=1)

        self.sidebar = SidebarCell(sim_tab, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0,8), pady=4)

        right = ctk.CTkFrame(sim_tab, fg_color=BG, corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew", pady=4)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(2, weight=1)

        self.proc_cell = ProcessTableCell(right, self)
        self.proc_cell.grid(row=0, column=0, sticky="ew", pady=(0,8))

        self.gantt_cell = GanttCell(right)
        self.gantt_cell.grid(row=1, column=0, sticky="ew", pady=(0,8))

        self.results_cell = ResultsCell(right)
        self.results_cell.grid(row=2, column=0, sticky="nsew", pady=(0,8))

        self.stats_cell = StatCardsCell(right)
        self.stats_cell.grid(row=3, column=0, sticky="ew")

        # Comparison tab
        self.cmp_tab = ComparisonTab(cmp_tab)
        self.cmp_tab.pack(fill="both", expand=True)

    def _on_algo_change(self, val):
        self.algorithm = "Round Robin" if val == RR_LABEL else "Priority Preemptive"

    def _refresh_table(self):
        self.proc_cell.refresh()

    def _add_process(self):
        self._process_dialog()

    def _edit_process(self, p):
        self._process_dialog(p)

    def _del_process(self, p):
        self.processes.remove(p)
        self._refresh_table()

    def _process_dialog(self, process=None):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Add Process" if not process else "Edit Process")
        dlg.geometry("380x320")
        dlg.configure(fg_color=BG2)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="Add Process" if not process else "Edit Process",
                     font=ctk.CTkFont("Consolas",14,"bold"),
                     text_color=ACCENT2).pack(pady=(16,10))

        entries = {}
        for label, key in [("Process ID","pid"), ("Arrival Time","arrival"),
                           ("Burst Time","burst"), ("Priority","priority")]:
            r = ctk.CTkFrame(dlg, fg_color="transparent")
            r.pack(fill="x", padx=24, pady=4)
            ctk.CTkLabel(r, text=label, width=110, anchor="w",
                         font=ctk.CTkFont("Consolas",10), text_color=FG2).pack(side="left")
            e = ctk.CTkEntry(r, width=160, fg_color=BG3, border_color=BG3,
                             text_color=FG, font=ctk.CTkFont("Consolas",10))
            e.pack(side="left", padx=8)
            e.insert(0, str(process[key]) if process else
                     (f"P{self.next_pid}" if key=="pid" else ""))
            entries[key] = e

        def save():
            try:
                pid = entries["pid"].get().strip()
                arr = int(entries["arrival"].get())
                bst = int(entries["burst"].get())
                pri = int(entries["priority"].get())
                if bst <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Invalid", "Please enter valid values.", parent=dlg)
                return

            if process:
                process.update({"arrival":arr, "arrivalTime":arr,
                                "burst":bst, "burstTime":bst, "priority":pri})
            else:
                self.processes.append({
                    "pid":pid, "id":pid, "arrival":arr, "arrivalTime":arr,
                    "burst":bst, "burstTime":bst, "priority":pri
                })
                self.next_pid += 1

            self._refresh_table()
            dlg.destroy()

        bf = ctk.CTkFrame(dlg, fg_color="transparent")
        bf.pack(pady=12)
        ctk.CTkButton(bf, text="Save", fg_color=ACCENT, hover_color="#c1121f",
                      font=ctk.CTkFont("Consolas",11,"bold"),
                      corner_radius=8, command=save).pack(side="left", padx=6)

        if process:
            ctk.CTkButton(bf, text="Delete", fg_color="#6e1a1a", hover_color="#4a0f0f",
                          font=ctk.CTkFont("Consolas",11), corner_radius=8,
                          command=lambda: (self.processes.remove(process),
                                           self._refresh_table(), dlg.destroy())
                          ).pack(side="left", padx=4)

        ctk.CTkButton(bf, text="Cancel", fg_color=BG3, hover_color=BG, text_color=FG,
                      font=ctk.CTkFont("Consolas",11), corner_radius=8,
                      command=dlg.destroy).pack(side="left", padx=4)

    def _clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all processes?"):
            self.processes.clear()
            self._last_rr = self._last_pp = None
            self._refresh_table()
            self.gantt_cell.clear()
            self.stats_cell.reset()
            self.results_cell.clear()
            self.cmp_tab.reset()

    def _reset(self):
        self.processes.clear()
        self._last_rr = self._last_pp = None
        self._refresh_table()
        self.gantt_cell.clear()
        self.stats_cell.reset()
        self.results_cell.clear()
        self.cmp_tab.reset()
        self._load_defaults()

    def _load_defaults(self):
        for d in [
            {"pid":"P1","id":"P1","arrival":0,"arrivalTime":0,"burst":5,"burstTime":5,"priority":2},
            {"pid":"P2","id":"P2","arrival":1,"arrivalTime":1,"burst":3,"burstTime":3,"priority":1},
            {"pid":"P3","id":"P3","arrival":2,"arrivalTime":2,"burst":8,"burstTime":8,"priority":3},
            {"pid":"P4","id":"P4","arrival":3,"arrivalTime":3,"burst":6,"burstTime":6,"priority":1},
        ]:
            self.processes.append(d)
        self.next_pid = 5
        self._refresh_table()

    def _run(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add at least one process.")
            return

        try:
            q = int(self.sidebar.quantum_entry.get())
            if q <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantum must be a positive integer.")
            return

        procs_copy = copy.deepcopy(self.processes)

        if self.algorithm == "Round Robin":
            timeline, results, averages = roundRobin(procs_copy, q)
            self._last_rr = (timeline, results, averages)
            self.cmp_tab.set_rr(timeline, results, averages)
            if self._last_pp:
                self.cmp_tab.set_pp(*self._last_pp)
        else:
            timeline, results, averages = preemptivePriority(procs_copy)
            self._last_pp = (timeline, results, averages)
            self.cmp_tab.set_pp(timeline, results, averages)
            if self._last_rr:
                self.cmp_tab.set_rr(*self._last_rr)

        self.gantt_cell.draw(timeline)
        self.results_cell.fill(results)
        self.stats_cell.update(averages, results)


if __name__ == "__main__":
    app = OSSchedulerApp()
    app.mainloop()