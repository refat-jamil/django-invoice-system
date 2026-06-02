# 🧾 Django Invoice System

A modern invoice management system built with Django.  
Supports invoice creation, client management, PDF generation, and business branding with logo support.

---

## ✨ Features

- 🧾 Create and manage invoices
- 👤 Client details management
- 🏢 Business profile with logo support
- 📄 PDF invoice download (WeasyPrint)
- 💰 Auto total calculation
- 🧠 Amount in words conversion
- 📅 Due date & status tracking (Draft / Sent / Paid)
- 🎨 Clean minimal invoice UI (Black, White & Gold theme)
- 🖨 Print-ready invoice design

---

## 🛠 Tech Stack

- Python 3
- Django
- SQLite (default)
- HTML / CSS
- WeasyPrint (PDF generation)

---

## 🚀 Installation

```bash
git clone https://github.com/your-username/django-invoice-system.git
cd django-invoice-system

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver