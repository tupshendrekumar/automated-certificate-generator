#  Automated Certificate Generator

## Team Name
The Debuggers

##  Project Title
Automated Certificate Generator

## Brief Description
A batch-processing tool that automatically generates personalized 
PDF certificates for workshop participants and emails them directly 
to their inbox.

## Solution
We built a Python-based batch processing tool that:
- Takes a CSV file containing participant names and email addresses
- Uses certificate template images (Blue, Green, Black/Gold designs)
- Automatically generates personalized PDF certificates for each participant
- Prints the participant's name and date on the certificate
- Emails the certificate as a PDF attachment to each participant
- Supports multiple certificate designs for variety

## Features
- CSV batch processing
- 3 professional certificate designs
- Auto PDF generation using Pillow + ReportLab
- Automated email sending via Gmail SMTP
- Date auto-printed on every certificate

## Technologies Used
- Python 3
- Pillow (image processing)
- ReportLab (PDF generation)
- SMTP / Gmail (email sending)

## How to Run

### 1. Install dependencies
pip install pillow reportlab pandas

### 2. Add participants in CSV
Edit participants.csv:
Name,Email
John Doe,john@example.com

### 3. Run the tool
python main.py

## Project Structure
Hackathon_Project/
 main.py
 participants.csv
 design1.jpg
 design2.jpg
 design3.jpg
 certificates/
