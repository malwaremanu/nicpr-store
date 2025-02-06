# Store Inventory and Indent Management System

## Overview
This project is a Flask-based Store Inventory and Indent Management System. It includes user authentication, role-based access control, and CRUD operations for inventory and indent management.

## Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, JavaScript (Vanilla + Select2.js)
- **Database**: JSON files

## User Roles
- **Superadmin**: Full access to manage everything.
- **Admin**: Manages users and inventory.
- **Store Assistant**: Issues items to users.
- **Store Incharge**: Approves indents before issuance.
- **Head of Division**: Approves indent requests from subordinates.
- **Indentor**: Creates indent requests.

## Project Structure
```
IMSv1/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── indent.py
│   │   ├── inventory.py
│   │   └── user.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── indent_form.html
│   │   ├── inventory_form.html
│   │   └── user_form.html
│   └── static/
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── main.js
│       └── images/
├── database.json
├── main.py
├── requirements.txt
└── README.md
```

## Setup
1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd IMSv1
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python main.py
    ```

4. **Access the application**:
    Open your browser and navigate to `http://127.0.0.1:5000/`.

## Contributing
Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.