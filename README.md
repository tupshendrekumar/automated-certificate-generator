# 🎓 Automated Certificate Generator

A batch-processing tool that automatically generates personalized 
PDF certificates and emails them to participants.

## ✨ Features
- Reads participant names and emails from CSV file
- Supports 3 certificate designs (Blue, Green, Black/Gold)
- Automatically generates personalized PDF certificates
- Emails certificates directly to each participant
- Date is automatically printed on each certificate

## 🛠️ Technologies Used
- Python 3
- Pillow (image processing)
- ReportLab (PDF generation)
- SMTP / Gmail (email sending)

## 🚀 How to Run

### 1. Install dependencies
pip install pillow reportlab pandas

### 2. Add participants in CSV
Edit participants.csv:
Name,Email
John Doe,john@example.com

### 3. Run the tool
python main.py

## 📁 Project Structure
Hackathon_Project/
├── main.py
├── participants.csv
├── design1.jpg
├── design2.jpg
├── design3.jpg
└── certificates/
