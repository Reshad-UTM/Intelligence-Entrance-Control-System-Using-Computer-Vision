import serial
import time
import cv2
import face_recognition
import os
import pytesseract
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime
import pyttsx3

# Configure the Arduino port and baud rate
arduino_port = 'COM3'
baud_rate = 9600

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the path to the license plate cascade classifier XML file
plate_cascade_path = r'G:\fyp\haarcascade_russian_plate_number.xml'

# Load the known images and names
known_images_path = 'Test_Image'
known_encodings = []
known_names = []

# Iterate over the known images folder
for filename in os.listdir(known_images_path):
    image_path = os.path.join(known_images_path, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]
    known_encodings.append(encoding)
    known_names.append(os.path.splitext(filename)[0])

# Connect to the Arduino
arduino = serial.Serial(arduino_port, baud_rate)

# Wait for Arduino to initialize
time.sleep(2)

# Load the input face image
face_image_path = r'G:\fyp\pic.jpg'
face_image = cv2.imread(face_image_path)

# Resize the input face image
scale_percent = 50  # Adjust the scale as needed
width = int(face_image.shape[1] * scale_percent / 100)
height = int(face_image.shape[0] * scale_percent / 100)
dim = (width, height)
resized_face_image = cv2.resize(face_image, dim, interpolation=cv2.INTER_AREA)

# Convert the resized face image from BGR color to RGB color
rgb_face_image = cv2.cvtColor(resized_face_image, cv2.COLOR_BGR2RGB)

# Find all face locations and encodings in the current frame
face_locations = face_recognition.face_locations(rgb_face_image)
face_encodings = face_recognition.face_encodings(rgb_face_image, face_locations)

# Iterate over the face encodings in the current frame
for face_encoding in face_encodings:
    # Compare the face encoding with the known encodings
    matches = face_recognition.compare_faces(known_encodings, face_encoding)
    name = "Unknown"  # Default name if no match is found

    # Check if there is a match
    if True in matches:
        match_index = matches.index(True)
        name = known_names[match_index]

    # Print the recognized name
    print("Recognized:", name)

    # Send a command to Arduino to move the servo
    if name != "Unknown":
        arduino.write(b'1')  # Send command to open the gate
        print("Okay, gate is open.")
        time.sleep(20)  # Wait for 20 seconds
        arduino.write(b'0')  # Send command to close the gate
        print("Gate is closing.")
        time.sleep(2)  # Wait for 2 seconds for the gate to close
        print("Gate closed.")

    else:
        print("Unknown person. Gate remains closed.")

    # Draw a box around the face
    top, right, bottom, left = face_locations[0]
    cv2.rectangle(resized_face_image, (left, top), (right, bottom), (0, 255, 0), 2)

    # Draw the name below the face box
    cv2.rectangle(resized_face_image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
    cv2.putText(resized_face_image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

# Continue with the rest of your license plate recognition, Google Sheets, and text-to-speech code.


# Load the input image for license plate detection
image_path = r'G:\fyp\n4.jpg'
frame = cv2.imread(image_path)

# Convert the frame to grayscale for license plate detection
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Load the license plate cascade classifier
plate_cascade = cv2.CascadeClassifier(plate_cascade_path)

# Detect license plates in the grayscale frame
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Process each detected license plate
for (x, y, w, h) in plates:
    plate_img = frame[y:y + h, x:x + w]  # Extract the license plate region

    # Convert the license plate region to grayscale for OCR
    plate_gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the license plate region
    plate_text = pytesseract.image_to_string(plate_gray,
                                              config='--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    # Remove any non-alphanumeric characters from the recognized text
    plate_text = ''.join(e for e in plate_text if e.isalnum())

    # Draw a bounding box around the license plate
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the recognized text on the frame
    cv2.putText(frame, plate_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Print the license plate text
    print("License Plate:", plate_text)

# Get the current date and time
entry_date = datetime.datetime.now().strftime('%Y-%m-%d')
entry_time = datetime.datetime.now().strftime('%H:%M:%S')

# Print all the information together
print("Name:", name)
print("Number Plate:", plate_text)
print("Entry Date:", entry_date)
print("Entry Time:", entry_time)

# Create a list of data to be written to the Google Sheet
data = [["Driver Name", "Number Plate", "Entry Date", "Entry Time"], [name, plate_text, entry_date, entry_time]]

# Google Sheets API authentication
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'G:\fyp\credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
spreadsheet = client.open('Number Plates')
sheet = spreadsheet.sheet1

# Append the data to the Google Sheet
sheet.append_rows(data)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice properties (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Select the voice

# Output voice command based on recognition result
if name != "Unknown":
    engine.say("Welcome, " + name + "!")  # Voice command for recognized person
else:
    engine.say("You are not a resident. Please use another gate.")  # Voice command for unrecognized person

engine.runAndWait()

# Check and adjust the dimensions of the images for concatenation
if resized_face_image.shape[0] != frame.shape[0]:
    height_diff = abs(resized_face_image.shape[0] - frame.shape[0])
    padding = (0, height_diff, 0) if resized_face_image.shape[0] < frame.shape[0] else (0, 0, height_diff)
    resized_face_image = cv2.copyMakeBorder(resized_face_image, *padding, cv2.BORDER_CONSTANT, None, value=(0, 0, 0))

# Concatenate the face image and license plate image horizontally
resized_frame = cv2.resize(frame, (resized_face_image.shape[1], resized_face_image.shape[0]))
combined_image = cv2.hconcat([resized_face_image, resized_frame])

# Display the combined image
cv2.imshow('Face and License Plate Recognition', cv2.resize(combined_image, (800, 400)))
cv2.waitKey(0)
cv2.destroyAllWindows()
# Close the connection to the Arduino
arduino.close()