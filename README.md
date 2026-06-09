# 🎟️ Smart Museum Visitor Portal

A modern web-based museum ticket booking and visitor management system developed using **Flask, Python, SQLite, HTML, CSS, and JavaScript**. The platform enables visitors to register, book museum tickets, generate QR-based digital passes, manage bookings, and interact with a virtual Museum Assistant chatbot.

---

## 📌 Project Overview

Smart Museum Visitor Portal is designed to enhance the museum visitor experience by digitizing the ticket booking process and providing instant access to museum-related information.

The system eliminates manual ticketing procedures and offers a seamless platform for:

- Visitor Registration & Login
- Museum Ticket Booking
- Dynamic Ticket Pricing
- QR Code-Based Digital Passes
- Booking History Management
- Museum Information Assistance via Chatbot

---

## ✨ Features

### 👤 User Management
- Secure User Registration
- User Login Authentication
- Session Management
- Logout Functionality

### 🎟️ Ticket Booking System
- Museum Ticket Booking
- Adult and Child Ticket Categories
- Automatic Fare Calculation
- Booking Confirmation

### 📜 Booking History
- View Previous Bookings
- Track Booking Status
- Cancel Active Bookings

### 📱 Digital Museum Pass
- QR Code Generation
- Digital Ticket Display
- Booking Verification Support

### 🤖 Museum Assistant Chatbot
- Ticket Price Information
- Museum Timings
- Museum Location Details
- Gallery Information
- Instant Visitor Assistance

### 🎨 User Interface
- Responsive Dashboard
- Modern UI Design
- Interactive Booking Workflow
- Mobile-Friendly Layout

---

## 🏗️ System Architecture

```text
Visitor
   │
   ▼
Frontend (HTML/CSS/JavaScript)
   │
   ▼
Flask Application
   │
   ▼
SQLite Database
   │
   ├── Users
   ├── Museums
   └── Bookings
   │
   ▼
QR Code Generator
```

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript

### Libraries
- qrcode
- bcrypt
- python-dotenv

---

## 📂 Project Structure

```text
smart-museum-visitor-portal/
│
├── app.py
├── db.py
├── init_db.py
├── insert_data.py
├── requirements.txt
│
├── static/
│   ├── css/
│   ├── images/
│   └── qrcodes/
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── history.html
│   ├── ticket.html
│   └── admin.html
│
└── database.db
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Newshika28/smart-museum-visitor-portal.git
cd smart-museum-visitor-portal
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Application

```bash
python app.py
```

### 6. Open Browser

```text
http://127.0.0.1:5000
```

---

## 🚀 Workflow

```text
Home Page
      │
      ▼
User Signup/Login
      │
      ▼
Dashboard
      │
      ▼
Book Museum Ticket
      │
      ▼
Automatic Fare Calculation
      │
      ▼
Booking Confirmation
      │
      ▼
QR Code Generation
      │
      ▼
Booking History
      │
      ▼
Digital Museum Pass
```

---

## 🔮 Future Enhancements

- AI-Powered Museum Guide using Gemini API
- Online Payment Gateway Integration
- Museum Navigation Assistant
- Visitor Analytics Dashboard
- Email Ticket Delivery
- Multi-Museum Support

---

## 🎯 Learning Outcomes

Through this project, I gained hands-on experience in:

- Full-Stack Web Development
- Flask Framework
- Database Design
- User Authentication
- QR Code Integration
- Session Management
- Frontend-Backend Integration
- Project Deployment & Version Control

---

