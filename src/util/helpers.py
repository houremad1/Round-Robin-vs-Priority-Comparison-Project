import customtkinter as ctk
from src.util.constants import *
from src.util.constants import ACCENT2

def _section_label(parent, text, color=ACCENT2):
    import customtkinter as ctk
    ctk.CTkLabel(parent, text=text,
                 font=ctk.CTkFont("Consolas", 12, "bold"),
                 text_color=color).pack(anchor="w", padx=12, pady=(14, 4))

def _pid_idx(pid):
    raw = pid[1:] if len(pid) > 1 else "1"
    return (int(raw) - 1) if raw.isdigit() else 0