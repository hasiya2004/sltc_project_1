

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import webbrowser

# ════════════════════════════════════════════════════════════
#  CONSTANTS  (TUPLE – fixed, immutable data)
# ════════════════════════════════════════════════════════════
COLUMN_HEADERS = ("ID", "Name", "Email", "Event")   # TUPLE
FILE_NAME = "registrations.csv"
GITHUB_URL = "https://github.com/hasiya2004"

# ── Light Colour Palette ─────────────────────────────────
BG = "#f0f4f8"
PANEL = "#ffffff"
SIDEBAR = "#1e293b"
SIDEBAR2 = "#0f172a"
INPUT_BG = "#f8fafc"
BORDER = "#e2e8f0"
BORDER2 = "#cbd5e1"
ACCENT = "#3b82f6"
ACCENT_HOV = "#2563eb"
GREEN = "#22c55e"
GREEN_BG = "#f0fdf4"
RED = "#ef4444"
RED_BG = "#fef2f2"
TEXT = "#0f172a"
TEXT2 = "#334155"
MUTED = "#94a3b8"
GOLD_LIGHT = "#fcd34d"
GOLD = "#f59e0b"

TAG_COLORS = {
    "Workshop": ("#1d4ed8", "#eff6ff"),
    "Seminar":  ("#7c3aed", "#f5f3ff"),
    "Gala":     ("#b45309", "#fffbeb"),
}


# ════════════════════════════════════════════════════════════
#  HELPER WIDGETS
# ════════════════════════════════════════════════════════════
class FlatEntry(tk.Entry):
    """Styled Entry with placeholder text."""

    def __init__(self, master, placeholder="", **kw):
        super().__init__(master,
                         bg=INPUT_BG, fg=TEXT, insertbackground=ACCENT,
                         relief="flat", font=("Helvetica", 11),
                         highlightthickness=1, highlightbackground=BORDER2,
                         highlightcolor=ACCENT, **kw)
        self.placeholder = placeholder
        self._has_ph = False
        if placeholder:
            self._put_placeholder()
        self.bind("<FocusIn>",  self._clear_ph)
        self.bind("<FocusOut>", self._set_ph)

    def _put_placeholder(self):
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self.config(fg=MUTED)
        self._has_ph = True

    def _clear_ph(self, _=None):
        if self._has_ph:
            self.delete(0, tk.END)
            self.config(fg=TEXT)
            self._has_ph = False

    def _set_ph(self, _=None):
        if not self.get().strip() and self.placeholder:
            self._put_placeholder()

    def real_value(self):
        return "" if self._has_ph else self.get().strip()


class RoundButton(tk.Label):
    """Styled clickable button."""

    def __init__(self, master, text, command, primary=False, **kw):
        bg = ACCENT if primary else BORDER
        fg = "#ffffff" if primary else TEXT2
        hbg = ACCENT_HOV if primary else BORDER2
        super().__init__(master, text=text, bg=bg, fg=fg,
                         font=("Helvetica", 10, "bold" if primary else "normal"),
                         padx=20, pady=9, cursor="hand2", relief="flat", **kw)
        self._bg = bg
        self._fg = fg
        self._hbg = hbg
        self._hfg = "#ffffff" if primary else TEXT
        self.bind("<Button-1>", lambda _: command())
        self.bind("<Enter>", lambda _: self.config(bg=self._hbg, fg=self._hfg))
        self.bind("<Leave>", lambda _: self.config(bg=self._bg,  fg=self._fg))


# ════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ════════════════════════════════════════════════════════════
class EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Event Registration System  |  Hasindu Senarathna  "
            "|  CIT-25-02-0120  |  Hasi Developers")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        # DATA STRUCTURES
        self.registration_list = []   # LIST: stores all records
        self.email_set = set()        # SET:  prevents duplicate emails

        self._center_window(980, 680)
        self._apply_styles()
        self._build_ui()
        self._load_data()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.root.minsize(860, 580)

    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("default")
        s.configure("Light.Treeview",
                    background=PANEL, foreground=TEXT,
                    fieldbackground=PANEL, rowheight=34,
                    borderwidth=0, font=("Helvetica", 10))
        s.configure("Light.Treeview.Heading",
                    background=BG, foreground=TEXT2,
                    relief="flat", borderwidth=0,
                    font=("Helvetica", 9, "bold"))
        s.map("Light.Treeview",
              background=[("selected", "#dbeafe")],
              foreground=[("selected", "#1e40af")])
        s.layout("Light.Treeview",
                 [("Treeview.treearea", {"sticky": "nswe"})])
        s.configure("TCombobox",
                    fieldbackground=INPUT_BG, background=PANEL,
                    foreground=TEXT, selectbackground=PANEL,
                    selectforeground=TEXT, arrowcolor=ACCENT)
        s.map("TCombobox",
              fieldbackground=[("readonly", INPUT_BG)],
              foreground=[("readonly", TEXT)])
        s.configure("Vertical.TScrollbar",
                    background=BORDER, troughcolor=BG,
                    borderwidth=0, arrowcolor=MUTED)

    # ── UI BUILD ────────────────────────────────────────

    def _build_ui(self):
        self._build_titlebar()
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)
        sidebar = tk.Frame(body, bg=SIDEBAR, width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)
        main = tk.Frame(body, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        self._build_main(main)
        self._build_footer()

    def _build_titlebar(self):
        bar = tk.Frame(self.root, bg=PANEL,
                       highlightbackground=BORDER, highlightthickness=1,
                       height=58)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        lf = tk.Frame(bar, bg=PANEL)
        lf.pack(side="left", padx=20, pady=8)
        tk.Label(lf, text="◈", bg=PANEL, fg=ACCENT,
                 font=("Helvetica", 22)).pack(side="left", padx=(0, 8))
        tf = tk.Frame(lf, bg=PANEL)
        tf.pack(side="left")
        tk.Label(tf, text="Event Registration System",
                 bg=PANEL, fg=TEXT,
                 font=("Helvetica", 14, "bold")).pack(anchor="w")
        tk.Label(tf,
                 text="Hasi Developers  ·  Hasindu Senarathna  ·  CIT-25-02-0120",
                 bg=PANEL, fg=MUTED, font=("Helvetica", 8)).pack(anchor="w")

        # GitHub button
        rf = tk.Frame(bar, bg=PANEL)
        rf.pack(side="right", padx=20)
        gh = tk.Label(rf, text="⌥  github.com/hasiya2004",
                      bg=SIDEBAR, fg="#ffffff",
                      font=("Helvetica", 9, "bold"),
                      padx=12, pady=6, cursor="hand2", relief="flat")
        gh.pack()
        gh.bind("<Button-1>", lambda _: webbrowser.open(GITHUB_URL))
        gh.bind("<Enter>", lambda _: gh.config(bg=ACCENT))
        gh.bind("<Leave>", lambda _: gh.config(bg=SIDEBAR))

        # Stats
        sf = tk.Frame(bar, bg=PANEL)
        sf.pack(side="right", padx=24)
        self.lbl_total = self._topstat(sf, "0", "Registered", ACCENT)
        self._topstat(sf, "3", "Events", GREEN)

    def _topstat(self, parent, val, label, color):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(side="right", padx=14)
        lbl = tk.Label(f, text=val, bg=PANEL, fg=color,
                       font=("Helvetica", 18, "bold"))
        lbl.pack()
        tk.Label(f, text=label, bg=PANEL, fg=MUTED,
                 font=("Helvetica", 7)).pack()
        return lbl

    def _build_sidebar(self, parent):
        # Dev card
        dev = tk.Frame(parent, bg=SIDEBAR2)
        dev.pack(fill="x")
        tk.Label(dev, text="👤", bg=SIDEBAR2, fg="#ffffff",
                 font=("Helvetica", 28)).pack(pady=(20, 4))
        tk.Label(dev, text="Hasindu Senarathna",
                 bg=SIDEBAR2, fg="#ffffff",
                 font=("Helvetica", 11, "bold")).pack()
        tk.Label(dev, text="CIT-25-02-0120",
                 bg=SIDEBAR2, fg=MUTED,
                 font=("Helvetica", 9)).pack(pady=(2, 4))
        gh = tk.Label(dev, text="⌥  hasiya2004",
                      bg=SIDEBAR2, fg=GOLD_LIGHT,
                      font=("Helvetica", 9), cursor="hand2")
        gh.pack(pady=(0, 14))
        gh.bind("<Button-1>", lambda _: webbrowser.open(GITHUB_URL))
        gh.bind("<Enter>", lambda _: gh.config(fg=GOLD))
        gh.bind("<Leave>", lambda _: gh.config(fg=GOLD_LIGHT))

        tk.Frame(parent, bg="#2d3f55", height=1).pack(fill="x")

        tk.Label(parent, text="SELECT EVENT",
                 bg=SIDEBAR, fg=MUTED,
                 font=("Helvetica", 8, "bold")).pack(
            anchor="w", padx=16, pady=(16, 8))

        self.chip_frames = {}
        self.event_var = tk.StringVar(value="Workshop")
        for icon, name, desc in [
            ("🎨", "Workshop", "Hands-on learning"),
            ("🎤", "Seminar",  "Expert discussions"),
            ("✨", "Gala",     "Evening of elegance"),
        ]:
            self._make_chip(parent, icon, name, desc)

        tk.Frame(parent, bg="#2d3f55", height=1).pack(fill="x", pady=12)
        tk.Label(parent, text="HASI DEVELOPERS",
                 bg=SIDEBAR, fg=MUTED,
                 font=("Helvetica", 8, "bold")).pack(pady=(4, 2))
        tk.Label(parent, text="CCS1300 Mini Project",
                 bg=SIDEBAR, fg="#3d5066",
                 font=("Helvetica", 8)).pack()

        tk.Frame(parent, bg=SIDEBAR).pack(fill="both", expand=True)
        foot = tk.Label(parent, text="github.com/hasiya2004",
                        bg=SIDEBAR2, fg="#3d5066",
                        font=("Helvetica", 8), cursor="hand2",
                        padx=12, pady=8)
        foot.pack(fill="x")
        foot.bind("<Button-1>", lambda _: webbrowser.open(GITHUB_URL))
        foot.bind("<Enter>", lambda _: foot.config(fg=MUTED))
        foot.bind("<Leave>", lambda _: foot.config(fg="#3d5066"))

        self._select_event("Workshop")

    def _make_chip(self, parent, icon, name, desc):
        f = tk.Frame(parent, bg=SIDEBAR, cursor="hand2")
        f.pack(fill="x", padx=10, pady=2)
        inner = tk.Frame(f, bg=SIDEBAR)
        inner.pack(fill="x", padx=10, pady=8)
        tk.Label(inner, text=icon, bg=SIDEBAR, fg="#ffffff",
                 font=("Helvetica", 15)).pack(side="left", padx=(0, 10))
        txt = tk.Frame(inner, bg=SIDEBAR)
        txt.pack(side="left")
        tk.Label(txt, text=name, bg=SIDEBAR, fg="#ffffff",
                 font=("Helvetica", 10, "bold")).pack(anchor="w")
        tk.Label(txt, text=desc, bg=SIDEBAR, fg=MUTED,
                 font=("Helvetica", 8)).pack(anchor="w")
        self.chip_frames[name] = f
        for w in [f, inner, txt] + inner.winfo_children() + txt.winfo_children():
            w.bind("<Button-1>", lambda _, n=name: self._select_event(n))

    def _select_event(self, name):
        self.event_var.set(name)
        for n, frame in self.chip_frames.items():
            active = (n == name)
            abg = ACCENT if active else SIDEBAR
            frame.config(bg=abg,
                         highlightbackground=ACCENT if active else SIDEBAR,
                         highlightthickness=1 if active else 0)
            for w in self._all_children(frame):
                try:
                    w.config(bg=abg)
                except Exception:
                    pass

    def _all_children(self, widget):
        kids = widget.winfo_children()
        out = list(kids)
        for c in kids:
            out.extend(self._all_children(c))
        return out

    def _build_main(self, parent):
        # Form card
        fw = tk.Frame(parent, bg=BG)
        fw.pack(fill="x", padx=20, pady=(16, 10))
        card = tk.Frame(fw, bg=PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x")
        pad = tk.Frame(card, bg=PANEL)
        pad.pack(fill="x", padx=24, pady=20)

        hdr = tk.Frame(pad, bg=PANEL)
        hdr.pack(fill="x", pady=(0, 16))
        tk.Label(hdr, text="Registration Details",
                 bg=PANEL, fg=TEXT,
                 font=("Helvetica", 13, "bold")).pack(side="left")
        tk.Label(hdr, text="All fields are required",
                 bg=PANEL, fg=MUTED,
                 font=("Helvetica", 9)).pack(side="right")

        r1 = tk.Frame(pad, bg=PANEL)
        r1.pack(fill="x", pady=(0, 10))
        self._field(r1, "REGISTRATION ID", "ent_id",
                    "e.g. REG-001", side="left")
        tk.Frame(r1, bg=PANEL, width=14).pack(side="left")
        self._field(r1, "FULL NAME", "ent_name",
                    "Your full name", side="left")

        self._field(pad, "EMAIL ADDRESS", "ent_email", "you@example.com")

        btn_row = tk.Frame(pad, bg=PANEL)
        btn_row.pack(fill="x", pady=(8, 0))
        RoundButton(btn_row, "✓  Register Now",
                    self._add_registration, primary=True).pack(side="left")
        tk.Frame(btn_row, bg=PANEL, width=10).pack(side="left")
        RoundButton(btn_row, "✕  Clear",
                    self._clear_fields).pack(side="left")

        # Toast notification
        self.toast_lbl = tk.Label(parent, text="",
                                  bg=GREEN_BG, fg=GREEN,
                                  font=("Helvetica", 10),
                                  padx=16, pady=8, anchor="w")

        # Table card
        tw = tk.Frame(parent, bg=BG)
        tw.pack(fill="both", expand=True, padx=20, pady=(0, 0))
        tcard = tk.Frame(tw, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        tcard.pack(fill="both", expand=True)

        th = tk.Frame(tcard, bg=PANEL)
        th.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(th, text="Registered Attendees",
                 bg=PANEL, fg=TEXT,
                 font=("Helvetica", 12, "bold")).pack(side="left")
        self.count_lbl = tk.Label(th, text="0 entries",
                                  bg="#dbeafe", fg="#1d4ed8",
                                  font=("Helvetica", 9, "bold"),
                                  padx=10, pady=3)
        self.count_lbl.pack(side="right")

        tf = tk.Frame(tcard, bg=PANEL)
        tf.pack(fill="both", expand=True, pady=(8, 0))
        tf.grid_rowconfigure(0, weight=1)
        tf.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tf, columns=COLUMN_HEADERS,
                                 show="headings", style="Light.Treeview")
        vsb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        col_w = {"ID": 100, "Name": 160, "Email": 230, "Event": 110}
        for col in COLUMN_HEADERS:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=col_w.get(col, 120), anchor="w")

    def _field(self, parent, label, attr, placeholder, side=None):
        wrap = tk.Frame(parent, bg=PANEL)
        if side:
            wrap.pack(side=side, expand=True, fill="x")
        else:
            wrap.pack(fill="x", pady=(0, 10))
        tk.Label(wrap, text=label, bg=PANEL, fg=ACCENT,
                 font=("Helvetica", 8, "bold")).pack(anchor="w", pady=(0, 4))
        ent = FlatEntry(wrap, placeholder=placeholder)
        ent.pack(fill="x", ipady=7)
        setattr(self, attr, ent)

    def _build_footer(self):
        bar = tk.Frame(self.root, bg=PANEL,
                       highlightbackground=BORDER, highlightthickness=1,
                       height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        tk.Label(bar,
                 text="  Hasindu Senarathna  ·  CIT-25-02-0120  "
                 "·  Hasi Developers  ·  CCS1300",
                 bg=PANEL, fg=MUTED, font=("Helvetica", 8),
                 anchor="w").pack(side="left", padx=8)
        gh = tk.Label(bar, text="⌥  github.com/hasiya2004  ",
                      bg=PANEL, fg=ACCENT,
                      font=("Helvetica", 8), cursor="hand2")
        gh.pack(side="right")
        gh.bind("<Button-1>", lambda _: webbrowser.open(GITHUB_URL))
        gh.bind("<Enter>", lambda _: gh.config(fg=ACCENT_HOV))
        gh.bind("<Leave>", lambda _: gh.config(fg=ACCENT))

    # ════════════════════════════════════════════════════
    #  CORE LOGIC FUNCTIONS
    # ════════════════════════════════════════════════════

    def _add_registration(self):
        """Function 1 – Validate and register a new attendee."""
        reg_id = self.ent_id.real_value()
        name = self.ent_name.real_value()
        email = self.ent_email.real_value()
        event = self.event_var.get()

        # if/else validation (Control Structures)
        if not all([reg_id, name, email]):
            self._toast("⚠  Please fill in all required fields.", error=True)
            return
        if "@" not in email or "." not in email:
            self._toast("⚠  Please enter a valid email address.", error=True)
            return
        # SET: check for duplicate email
        if email.lower() in self.email_set:
            self._toast(f"⚠  '{email}' is already registered!", error=True)
            return

        # DICTIONARY: structured record
        record = {"ID": reg_id, "Name": name, "Email": email, "Event": event}
        self.registration_list.append(record)   # LIST
        self.email_set.add(email.lower())        # SET

        tag = event.lower()
        fg, bg = TAG_COLORS.get(event, (TEXT, PANEL))
        self.tree.tag_configure(tag, foreground=fg, background=bg)
        self.tree.insert("", 0, values=(reg_id, name, email, event),
                         tags=(tag,))
        self._update_stats()
        self._save_data()
        self._clear_fields()
        self._toast(f"✓  {name} registered for {event}!")

    def _toast(self, msg, error=False):
        """Function 2 – Show a brief notification banner."""
        self.toast_lbl.config(
            text=msg,
            bg=RED_BG if error else GREEN_BG,
            fg=RED if error else GREEN)
        self.toast_lbl.pack(fill="x", padx=20, pady=(0, 6))
        self.root.after(3500, self.toast_lbl.pack_forget)

    def _update_stats(self):
        """Function 3 – Refresh the registration count labels."""
        n = len(self.registration_list)
        self.lbl_total.config(text=str(n))
        self.count_lbl.config(
            text=f"{n} {'entry' if n == 1 else 'entries'}")

    def _clear_fields(self):
        """Function 4 – Reset all input fields to placeholder state."""
        for ent in (self.ent_id, self.ent_name, self.ent_email):
            ent._put_placeholder()
        self.event_var.set("Workshop")
        self._select_event("Workshop")

    def _load_data(self):
        """Function 5 – Load registrations from CSV on startup."""
        try:
            if not os.path.exists(FILE_NAME):
                return
            with open(FILE_NAME, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):   # for loop (Control Structures)
                    if not {"ID", "Name", "Email", "Event"}.issubset(row):
                        continue
                    record = {k: row[k]
                              for k in ["ID", "Name", "Email", "Event"]}
                    self.registration_list.append(record)    # LIST
                    self.email_set.add(row["Email"].lower())  # SET
                    tag = row["Event"].lower()
                    fg, bg = TAG_COLORS.get(row["Event"], (TEXT, PANEL))
                    self.tree.tag_configure(tag, foreground=fg, background=bg)
                    self.tree.insert("", "end",
                                     values=(row["ID"], row["Name"],
                                             row["Email"], row["Event"]),
                                     tags=(tag,))
            self._update_stats()
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def _save_data(self):
        """Function 6 – Save all registrations to CSV file."""
        try:
            with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["ID", "Name", "Email", "Event"])
                writer.writeheader()
                writer.writerows(self.registration_list)   # LIST
        except IOError as e:
            messagebox.showerror("Save Error", str(e))


# ════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = EventApp(root)
    root.mainloop()
