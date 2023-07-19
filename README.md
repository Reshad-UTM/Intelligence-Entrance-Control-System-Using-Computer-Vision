# Intelligence-Entrance-Control-System-Using-Computer-Vision
System Demo
Introduction

This repository contains the implementation of an Intelligent Entrance Control System using computer vision. The system integrates face recognition, number plate recognition, database management, and hardware control to create an efficient and secure access control solution.
Features

    Face Recognition: The system can accurately detect and recognize known individuals using facial features.
    Number Plate Recognition: It can extract and recognize vehicle number plates using OCR technology.
    Database Management: The system stores entry data in a Google Sheet for record-keeping and analysis.
    Hardware Integration: It controls an Arduino-based gate system for automated access control.

Requirements

    Python 3.x
    OpenCV
    Face Recognition Library
    Tesseract OCR Engine
    Google Sheets API
    Raspberry Pi (or compatible microcontroller)
    Arduino Board

Installation

    Clone the repository: git clone https://github.com/Reshad-UTM/intelligent-entrance-control.git
    Install dependencies: pip install -r requirements.txt
    Configure the Arduino port and Tesseract OCR path in the code.

Usage

    Add known individual images in the Test_Image folder for face recognition.
    Prepare a sample image with a vehicle number plate for testing number plate recognition.
    Run the code: python main.py
    The system will display the recognized name and number plate information.
    If the face is recognized, the gate will open for a specified duration.
    The entry details will be logged in the Google Sheet.

Performance

    Face Recognition: 100% accuracy in recognizing known individuals.
    Number Plate Recognition: 67% accuracy, can be further optimized for improved performance.
    Overall System Accuracy: 89%, showing promising results.

Contributing

Contributions are welcome! If you find any issues or want to enhance the system, please open a pull request or create an issue.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    Face Recognition Library
    Tesseract OCR Engine
    Google Sheets API

