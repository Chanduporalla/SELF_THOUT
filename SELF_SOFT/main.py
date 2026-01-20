import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
from datetime import datetime, date

# ---------------- CONFIG ----------------
APP_TITLE = "Edu Tantra - Internal CRM"
WINDOW_SIZE = "1200x700"

USERNAME = "admin"
PASSWORD = "edu123"

DATA_FILE = "students.json"

BG_COLOR = "#121212"
CARD_COLOR = "#1e1e1e"
TEXT_COLOR = "#ffffff"
ACCENT = "#4CAF50"
INPUT_BG = "#2b2b2b"

# ---------------- DATA FUNCTIONS ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- MAIN APP ----------------
class EduTantraApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)
        self.data = load_data()
        self.today_count = self.count_today()
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------------- LOGIN ----------------
    def show_login(self):
        self.clear()

        bg = Image.open("bg_login.png").resize((1200, 700))
        self.bg_login = ImageTk.PhotoImage(bg)
        tk.Label(self.root, image=self.bg_login).place(x=0, y=0)

        card = tk.Frame(self.root, bg=CARD_COLOR)
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=320)

        tk.Label(card, text="Edu Tantra Login",
                 fg=TEXT_COLOR, bg=CARD_COLOR,
                 font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.user = tk.Entry(card, bg=INPUT_BG, fg="white",
                             font=("Segoe UI", 11),
                             insertbackground="white")
        self.user.pack(pady=10, ipady=6, padx=30, fill="x")

        self.pwd = tk.Entry(card, bg=INPUT_BG, fg="white",
                            show="*", font=("Segoe UI", 11),
                            insertbackground="white")
        self.pwd.pack(pady=10, ipady=6, padx=30, fill="x")

        tk.Button(card, text="LOGIN",
                  bg=ACCENT, fg="white",
                  font=("Segoe UI", 11, "bold"),
                  command=self.login).pack(pady=20, ipadx=20)

    def login(self):
        if self.user.get() == USERNAME and self.pwd.get() == PASSWORD:
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")

    # ---------------- DASHBOARD ----------------
    def show_dashboard(self):
        self.clear()

        bg = Image.open("bg_dashboard.png").resize((1200, 700))
        self.bg_dash = ImageTk.PhotoImage(bg)
        tk.Label(self.root, image=self.bg_dash).place(x=0, y=0)

        # TARGET CARD
        target = tk.Frame(self.root, bg=CARD_COLOR)
        target.place(x=20, y=20, width=300, height=80)

        tk.Label(target, text="Today's Leads",
                 bg=CARD_COLOR, fg="gray").pack()
        self.target_lbl = tk.Label(target, text=str(self.today_count),
                                   bg=CARD_COLOR, fg=ACCENT,
                                   font=("Segoe UI", 22, "bold"))
        self.target_lbl.pack()

        # LEFT – NOTES
        left = tk.Frame(self.root, bg=CARD_COLOR)
        left.place(x=20, y=120, width=560, height=550)

        tk.Label(left, text="Pitch / Call Notes",
                 bg=CARD_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 15, "bold")).pack(pady=10)

        self.notes = tk.Text(left, bg=INPUT_BG, fg="white",
                             font=("Segoe UI", 11),
                             insertbackground="white")
        self.notes.pack(expand=True, fill="both", padx=15, pady=10)

        # RIGHT – STUDENT DETAILS
        right = tk.Frame(self.root, bg=CARD_COLOR)
        right.place(x=600, y=20, width=580, height=650)

        def field(label):
            tk.Label(right, text=label,
                     bg=CARD_COLOR, fg="gray").pack(anchor="w", padx=30, pady=(15, 5))
            e = tk.Entry(right, bg=INPUT_BG, fg="white",
                         font=("Segoe UI", 11),
                         insertbackground="white")
            e.pack(fill="x", padx=30, ipady=6)
            return e

        self.name = field("Student Name")
        self.mobile = field("Mobile Number")
        self.college = field("College")
        self.email = field("Email")

        tk.Label(right, text="Lead Status",
                 bg=CARD_COLOR, fg="gray").pack(anchor="w", padx=30, pady=(15, 5))
        self.status = tk.StringVar(value="Interested")
        tk.OptionMenu(right, self.status,
                      "Interested", "Follow-up", "Converted").pack(
            padx=30, fill="x"
        )

        tk.Button(right, text="SAVE LEAD",
                  bg=ACCENT, fg="white",
                  font=("Segoe UI", 11, "bold"),
                  command=self.save_lead).pack(pady=25, ipadx=25)

    def save_lead(self):
        student = {
            "name": self.name.get(),
            "mobile": self.mobile.get(),
            "college": self.college.get(),
            "email": self.email.get(),
            "status": self.status.get(),
            "notes": self.notes.get("1.0", "end").strip(),
            "datetime": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "date": date.today().isoformat()
        }

        self.data.append(student)
        save_data(self.data)

        self.today_count = self.count_today()
        self.target_lbl.config(text=str(self.today_count))

        self.name.delete(0, "end")
        self.mobile.delete(0, "end")
        self.college.delete(0, "end")
        self.email.delete(0, "end")
        self.notes.delete("1.0", "end")

        messagebox.showinfo("Success", "Lead saved successfully")

    def count_today(self):
        today = date.today().isoformat()
        return len([d for d in self.data if d.get("date") == today])


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EduTantraApp(root)
    root.mainloop()
