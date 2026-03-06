# 🎟️ Event Registration System
### CCS1300 – Programming Concepts | Mini Project
**Sri Lanka Technology Campus (SLTC)**

---

![Python](https://img.shields.io/badge/Python-3.x-3b82f6?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-22c55e?style=for-the-badge)
![CSV](https://img.shields.io/badge/Storage-CSV-f59e0b?style=for-the-badge)
![SLTC](https://img.shields.io/badge/SLTC-Mini%20Project-ef4444?style=for-the-badge)

---

## 👨‍💻 Developer

| Field | Details |
|---|---|
| **Name** | Hasindu Senarathna |
| **Reg Number** | CIT-25-02-0120 |
| **Company** | Hasi Developers |
| **GitHub** | [@hasiya2004](https://github.com/hasiya2004) |
| **Institution** | Sri Lanka Technology Campus (SLTC) |
| **Course** | CCS1300 – Programming Concepts |

---

## 📌 About This Project

This is my **first mini project** at Sri Lanka Technology Campus (SLTC), built as part of the **CCS1300 – Programming Concepts** module.

The **Event Registration System** is a fully functional desktop application built using **Python** and **Tkinter**. It allows users to register attendees for different types of events — Workshops, Seminars, and Galas — with a clean, modern light-themed interface.

All registered data is saved to a **CSV file** so records are preserved between sessions.

---

## ✨ Features

- 🎨 **Modern Light UI** — Clean white panels with a dark navy sidebar and blue accents
- ➕ **Register Attendees** — Add registrations with ID, name, email, and event type
- 🔒 **Duplicate Prevention** — Uses a `set` to block the same email from registering twice
- 💾 **CSV File Storage** — Data is automatically saved and loaded on every run
- 🎯 **Event Type Selector** — Clickable sidebar chips for Workshop, Seminar, and Gala
- ✅ **Input Validation** — Checks for empty fields and valid email format
- 🔔 **Toast Notifications** — Success and error messages with colour-coded banners
- 🌐 **GitHub Link** — Clickable profile link built into the UI
- 📊 **Live Stats** — Registration count updates in real time

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core programming language |
| **Tkinter** | GUI framework (built-in) |
| **ttk (themed Tkinter)** | Styled Treeview and Combobox widgets |
| **CSV module** | File-based data storage |
| **OS module** | File existence checking |
| **Webbrowser module** | Opens GitHub profile link |

---

## 📚 Python Concepts Demonstrated

This project was built to demonstrate the following concepts from **CCS1300**:

| Concept | How It's Used |
|---|---|
| **List** | `registration_list` stores all attendee records |
| **Dictionary** | Each registration is stored as a `dict` with keys ID, Name, Email, Event |
| **Tuple** | `COLUMN_HEADERS` stores fixed column names |
| **Set** | `email_set` prevents duplicate email registrations |
| **if / else** | Input validation and duplicate checks |
| **for loop** | Iterates over CSV rows on file load |
| **Functions** | 6 user-defined functions handling all core logic |
| **File Handling** | CSV read on startup, write on every new registration |
| **Exception Handling** | try/except wraps all file I/O operations |
| **OOP / Classes** | `EventApp`, `FlatEntry`, `RoundButton` custom classes |

---

## 🚀 How to Run

**Requirements:** Python 3.x (Tkinter is included by default)

```bash
# 1. Clone the repository
git clone https://github.com/hasiya2004/sltc_project_1.git

# 2. Navigate into the folder
cd sltc_project_1

# 3. Run the app
python event_registration.py

> ⚠️ No extra libraries needed — everything uses Python's standard library.

---

## 📁 Project Structure

```
event-registration-system/
│
├── event_registration.py   # Main application source code
├── registrations.csv       # Auto-generated data file (created on first run)
└── README.md               # Project documentation
```

---

## 📸 UI Overview

| Section | Description |
|---|---|
| **Title Bar** | App name, developer name, reg number, GitHub button |
| **Dark Sidebar** | Developer card + clickable event type chips |
| **Form Panel** | Input fields for ID, name, email + register button |
| **Table** | Colour-coded list of all registered attendees |
| **Footer** | Persistent branding bar with GitHub link |

---

## 🎓 Academic Info

> **Course:** CCS1300 – Programming Concepts  
> **Institution:** Sri Lanka Technology Campus (SLTC)  
> **Project Type:** Mini Project (Individual)  
> **Submission:** 03/06/2026  

This is my **first mini project** submitted at SLTC. It was a great learning experience that helped me understand how to combine Python fundamentals — data structures, file handling, and GUI development — into a real, working desktop application.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/hasiya2004">Hasindu Senarathna</a> · Hasi Developers · SLTC 2026
</p>
