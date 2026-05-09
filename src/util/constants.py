import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#e63946"
ACCENT2 = "#4cc9f0"
ORANGE = "#f0a500"
PURPLE = "#a371f7"
GREEN = "#3fb950"
BG = "#0d1117"
BG2 = "#161b22"
BG3 = "#21262d"
FG = "#c9d1d9"
FG2 = "#8b949e"

PROC_COLORS = ["#3fb950", "#4cc9f0", "#a371f7", "#f0a500",
               "#e63946", "#58a6ff", "#ffa657", "#79c0ff"]

RR_LABEL = " Round Robin"
PP_LABEL = " Priority (Preemptive)"

RCOLS = ["process_id", "arrival", "burst", "completion",
         "turnaround_time", "waiting_time", "response_time"]

RHEADS = ["PID", "Arrival", "Burst", "Completion",
          "Turnaround", "Waiting", "Response"]

RWIDTHS = [55, 70, 60, 100, 100, 80, 80]

RCMAP = {"waiting_time": ORANGE, "response_time": GREEN}