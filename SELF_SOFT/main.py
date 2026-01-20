import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json, os
from datetime import date, datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

APP_TITLE = "Edu Tantra Mini CRM"
DATA_FILE = "leads.json"

# ---------- DATA ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- APP ----------
class EduTantraCRM:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.configure(bg="#f4f6f9")

        self.root.update_idletasks()
        try:
            self.root.attributes("-zoomed", True)
        except:
            self.root.geometry(
                f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0"
            )

        self.data = load_data()
        self.show_login()

    # ---------- LOGIN ----------
    def show_login(self):
        self.clear()
        container = tk.Frame(self.root, bg="#f4f6f9")
        container.pack(expand=True)

        if os.path.exists("logo.png"):
            img = Image.open("logo.png").resize((320, 120))
            self.logo = ImageTk.PhotoImage(img)
            tk.Label(container, image=self.logo, bg="#f4f6f9").pack(pady=30)
        else:
            tk.Label(container, text="EDU TANTRA",
                     font=("Segoe UI", 28, "bold"),
                     bg="#f4f6f9").pack(pady=30)

        card = tk.Frame(container, bg="white", padx=30, pady=25)
        card.pack()

        tk.Label(card, text="Login",
                 font=("Segoe UI", 18, "bold"),
                 bg="white").grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(card, text="Username", bg="white").grid(row=1, column=0, sticky="e")
        tk.Label(card, text="Password", bg="white").grid(row=2, column=0, sticky="e")

        self.u = tk.Entry(card, width=25)
        self.p = tk.Entry(card, show="*", width=25)
        self.u.grid(row=1, column=1, pady=5)
        self.p.grid(row=2, column=1, pady=5)

        ttk.Button(card, text="Login", command=self.login)\
            .grid(row=3, column=0, columnspan=2, pady=15)

    def login(self):
        if self.u.get() == "admin" and self.p.get() == "edu123":
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    # ---------- DASHBOARD ----------
    def show_dashboard(self):
        self.clear()
        self.build_topbar()
        self.build_main()
        self.show_leads()

    def build_topbar(self):
        top = tk.Frame(self.root, bg="white")
        top.pack(fill="x")
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=2)
        top.grid_columnconfigure(2, weight=1)

        tk.Label(top, text="Edu Tantra CRM",
                 font=("Segoe UI", 13, "bold"),
                 bg="white").grid(row=0, column=0, sticky="w", padx=20)

        if os.path.exists("logo.png"):
            img = Image.open("logo.png").resize((220, 80))
            self.logo = ImageTk.PhotoImage(img)
            tk.Label(top, image=self.logo, bg="white").grid(row=0, column=1, pady=5)
        else:
            tk.Label(top, text="EDU TANTRA",
                     font=("Segoe UI", 18, "bold"),
                     bg="white").grid(row=0, column=1)

        menu = tk.Frame(top, bg="white")
        menu.grid(row=0, column=2, sticky="e", padx=20)

        for txt, cmd in [
            ("Add Lead", lambda: self.add_lead()),
            ("Leads", self.show_leads),
            ("Pitch", self.show_pitch),
            ("Stats", self.show_stats),
            ("Save", lambda: save_data(self.data))
        ]:
            ttk.Button(menu, text=txt, command=cmd).pack(side="left", padx=4)

    def build_main(self):
        self.main = tk.Frame(self.root, bg="#f4f6f9")
        self.main.pack(fill="both", expand=True)

    # ---------- ADD / EDIT LEAD ----------
    def add_lead(self, existing_lead=None):
        win = tk.Toplevel(self.root)
        win.title("Add Lead")
        win.geometry("420x500")

        fields = ["Name", "Mobile", "College", "Email", "Follow-up (YYYY-MM-DD)"]
        entries = {}

        for f in fields:
            tk.Label(win, text=f).pack(anchor="w", padx=20, pady=2)
            e = tk.Entry(win)
            e.pack(fill="x", padx=20)
            entries[f] = e

        tk.Label(win, text="Status").pack(anchor="w", padx=20, pady=5)
        status = ttk.Combobox(win, values=["Interested", "Follow-up", "Converted"])
        status.pack(fill="x", padx=20)

        tk.Label(win, text="Pitch Notes").pack(anchor="w", padx=20, pady=5)
        pitch = tk.Text(win, height=5)
        pitch.pack(fill="x", padx=20)

        if existing_lead:
            for f in fields:
                entries[f].insert(0, existing_lead[f.lower()])
            status.set(existing_lead["status"])
            pitch.insert("1.0", existing_lead.get("pitch", ""))

        def save():
            lead_data = {
                "name": entries["Name"].get(),
                "mobile": entries["Mobile"].get(),
                "college": entries["College"].get(),
                "email": entries["Email"].get(),
                "followup": entries["Follow-up (YYYY-MM-DD)"].get(),
                "status": status.get(),
                "pitch": pitch.get("1.0", "end").strip(),
                "date": str(date.today())
            }

            if existing_lead:
                idx = self.data.index(existing_lead)
                self.data[idx] = lead_data
            else:
                self.data.append(lead_data)

            save_data(self.data)
            win.destroy()
            self.show_leads()

        ttk.Button(win, text="Save Lead", command=save).pack(pady=15)

    # ---------- LEADS LIST ----------
    def show_leads(self):
        for w in self.main.winfo_children():
            w.destroy()

        search = tk.Entry(self.main)
        search.pack(fill="x", padx=20, pady=10)

        tree = ttk.Treeview(self.main, columns=("name", "mobile", "status"), show="headings")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        for c in ("name", "mobile", "status"):
            tree.heading(c, text=c.title())

        def load(text=""):
            tree.delete(*tree.get_children())
            for l in self.data:
                if text.lower() in l["name"].lower() or text in l["mobile"]:
                    tree.insert("", "end",
                                values=(l["name"], l["mobile"], l["status"]))

        load()
        search.bind("<KeyRelease>", lambda e: load(search.get()))

    # ---------- PITCH VIEW ----------
    def show_pitch(self):
        for w in self.main.winfo_children():
            w.destroy()

        tk.Label(self.main, text="Student Pitch Notes",
                 font=("Segoe UI", 16, "bold"),
                 bg="#f4f6f9").pack(pady=15)

        canvas = tk.Canvas(self.main, bg="#f4f6f9")
        scrollbar = ttk.Scrollbar(self.main, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f4f6f9")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for l in self.data:
            box = tk.LabelFrame(scroll_frame, text=l["name"], bg="white")
            box.pack(fill="x", padx=20, pady=6)
            tk.Label(box, text=f"Pitch Notes:\n{l.get('pitch','')}",
                     bg="white", wraplength=900, justify="left").pack(padx=10, pady=5)
            ttk.Button(box, text="Edit Pitch",
                       command=lambda lead=l: self.add_lead(existing_lead=lead)).pack(pady=5)

    # ---------- STATS ----------
    def show_stats(self):
        for w in self.main.winfo_children():
            w.destroy()

        today = date.today()
        daily = sum(1 for l in self.data if l["date"] == str(today))
        weekly = sum(1 for l in self.data
                     if (today - datetime.strptime(l["date"], "%Y-%m-%d").date()).days <= 7)
        monthly = sum(1 for l in self.data
                      if datetime.strptime(l["date"], "%Y-%m-%d").month == today.month)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(["Today", "This Week", "This Month"], [daily, weekly, monthly], color="#4CAF50")
        ax.set_title("Lead Performance")
        ax.set_ylabel("Number of Leads")

        canvas = FigureCanvasTkAgg(fig, master=self.main)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, pady=40)

    # ---------- UTILITY ----------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()


# ---------- RUN ----------
root = tk.Tk()
EduTantraCRM(root)
root.mainloop()
