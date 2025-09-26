import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import pytesseract
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Set Tesseract OCR Path (Change this based on your Tesseract installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\vamshith\exam\Tesseract-OCR\tesseract.exe'  # Windows


# Function to extract text from an image using OCR
def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()


# Function to upload prebuilt answer file (text-based model answer)
def upload_prebuilt():
    global prebuilt_answer
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            prebuilt_answer = file.read()
        prebuilt_label.config(text="Prebuilt Answer Loaded")


# Function to upload student answer image and extract text
def upload_student():
    global student_answer
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        student_answer = extract_text_from_image(filepath)
        student_label.config(text="Student Answer Extracted")


# Function to evaluate the extracted answer
def evaluate_answer():
    global student_name, subject_name
    if not prebuilt_answer or not student_answer:
        messagebox.showwarning("Warning", "Please upload both prebuilt and student answers.")
        return

    student_name = name_entry.get().strip()  # Get student's name from input
    subject_name = subject_entry.get().strip()  # Get subject name from input

    if not student_name or not subject_name:
        messagebox.showwarning("Warning", "Please enter both student name and subject name.")
        return

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([prebuilt_answer, student_answer])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

    # Assign grades based on similarity score
    if similarity > 90:
        grade = "Excellent"
    elif similarity > 75:
        grade = "Good"
    elif similarity > 50:
        grade = "Average"
    elif similarity > 30:
        grade = "Poor"
    else:
        grade = "Very Poor"

    # Save the evaluation results in an Excel file
    save_results_to_excel(student_name, subject_name, prebuilt_answer, student_answer, similarity, grade)

    result_text.set(f"Student: {student_name}\nSubject: {subject_name}\nScore: {similarity:.2f}%\nGrade: {grade}")
    messagebox.showinfo("Evaluation Complete",
                        f"Student: {student_name}\nSubject: {subject_name}\nScore: {similarity:.2f}%\nGrade: {grade}")


# Function to save results in an Excel file
def save_results_to_excel(name, subject, prebuilt, student, score, grade):
    file_path = "evaluation_results.xlsx"

    # Create a DataFrame for the new record
    new_data = pd.DataFrame({
        "Student Name": [name],
        "Subject Name": [subject],
        "Prebuilt Answer": [prebuilt],
        "Student Answer": [student],
        "Similarity Score (%)": [score],
        "Grade": [grade]
    })

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_excel(file_path, engine='openpyxl')
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        except Exception as e:
            messagebox.showerror("Error", f"Corrupt Excel file detected! Creating a new one.\n\n{e}")
            os.remove(file_path)  # Delete the corrupted file
            updated_data = new_data  # Start fresh
    else:
        updated_data = new_data  # No existing file, create a new one

    # Save to Excel
    updated_data.to_excel(file_path, index=False, engine='openpyxl')


# Initialize GUI
root = tk.Tk()
root.title("Subjective Answer Evaluation")
root.geometry("600x500")

prebuilt_answer = ""
student_answer = ""

# Label & Entry for Student Name
name_label = tk.Label(root, text="Enter Student Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Label & Entry for Subject Name
subject_label = tk.Label(root, text="Enter Subject Name:")
subject_label.pack(pady=5)
subject_entry = tk.Entry(root)
subject_entry.pack(pady=5)

# Upload Prebuilt Answer Button
upload_prebuilt_btn = tk.Button(root, text="Upload Prebuilt Answers", command=upload_prebuilt)
upload_prebuilt_btn.pack(pady=5)
prebuilt_label = tk.Label(root, text="No file uploaded")
prebuilt_label.pack()

# Upload Student Answer Image Button
upload_student_btn = tk.Button(root, text="Upload Student Answer Image", command=upload_student)
upload_student_btn.pack(pady=5)
student_label = tk.Label(root, text="No image uploaded")
student_label.pack()

# Evaluate Button
evaluate_btn = tk.Button(root, text="Evaluate Answer", command=evaluate_answer)
evaluate_btn.pack(pady=10)

# Result Display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12))
result_label.pack()

root.mainloop()
