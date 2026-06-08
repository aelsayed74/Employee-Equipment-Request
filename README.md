# Employee Equipment Request Module (Odoo 17)

A comprehensive, production-ready Odoo 17 custom module designed to streamline the procurement and tracking of company equipment assigned to employees. This module manages the complete lifecycle of equipment requests, from initial drafting to approval, and features robust reporting and management tools.

## 🚀 Features

- **Custom Workflow Lifecycle:** Supports standard Odoo state transitions: `Draft` ➔ `Submitted` ➔ `Approved` / `Rejected` ➔ `Done`.
- **Automated Sequence Generation:** Automatically generates unique sequence references (e.g., `EQ-2026-0001`) upon request submission.
- **Dynamic Kanban & Tree Views:** Beautifully structured UI incorporating conditional colors and badges based on the state.
- **HR Employee Integration (Smart Button):** Inherits the standard `hr.employee` model to add a tracking smart button showing the total number of requests per employee with direct filtering.
- **Interactive Rejection Wizard:** Implements a conditional workflow where rejection requires inputting a validation reason through a transient model popup.
- **Scheduled Actions (Cron Jobs):** Includes an automated cron job that scans for pending requests, highlights late submittals in red via compute logic, and posts chatter logs.
- **Advanced Reporting:**
  - **PDF Report:** Custom QWeb printable template for individual equipment vouchers.
  - **Excel (XLSX) Export Wizard:** Interactive filtering wizard allowing dynamic reports to be exported based on dates and request statuses.
- **Security & Access Control:** Fine-tuned `ir.model.access.csv` providing dedicated access rules for Employees and Managers.

## 📁 Module Structure

```text
employee_equipment_request/
├── data/
│   ├── sequence.xml
│   └── cron_data.xml
├── models/
│   ├── __init__.py
│   ├── employee_equipment_request.py
│   └── hr_employee.py
├── reports/
│   └── equipment_report.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── views/
│   ├── base_menu.xml
│   ├── employee_equipment_request.xml
│   └── hr_employee.xml
├── wizard/
│   ├── __init__.py
│   ├── equipment_excel_wizard.py
│   ├── equipment_excel_wizard_view.xml
│   ├── reject_request.py
│   └── reject_request_view.xml
├── __init__.py
├── __manifest__.py
└── .gitignore