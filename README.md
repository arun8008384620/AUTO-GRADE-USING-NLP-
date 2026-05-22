# Auto Grade Using NLP 📝

An automated answer evaluation system that uses **Natural Language Processing (NLP)** and **OCR** to grade subjective answers. The system compares student handwritten/typed answers against model answers using TF-IDF and Cosine Similarity, then saves results to an Excel spreadsheet.

---

## Features

- 📷 Extract text from student answer **images** using OCR (Tesseract)
- 📄 Load **model answers** from plain text files
- 🤖 Score answers using **TF-IDF + Cosine Similarity**
- 🎓 Auto-assign **grades** (Excellent / Good / Average / Poor / Very Poor)
- 📊 Save all results to **Excel** (`evaluation_results.xlsx`)
- 🖥️ Simple **Tkinter GUI** — no command-line needed

---

## Grading Scale

| Similarity Score | Grade      |
|-----------------|------------|
| > 90%           | Excellent  |
| > 75%           | Good       |
| > 50%           | Average    |
| > 30%           | Poor       |
| ≤ 30%           | Very Poor  |

---

## Project Structure

```
AUTO-GRADE-USING-NLP/
├── subjective.py          # Main application
├── requirements.txt       # Python dependencies
├── sample_answer.txt      # Sample model answer (for testing)
├── evaluation_results.xlsx  # Auto-generated output file
├── Final Report.pdf
├── Review-1.pdf
├── Review-2.pdf
└── Review-3.pdf
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/arun8008384620/AUTO-GRADE-USING-NLP-.git
cd AUTO-GRADE-USING-NLP-
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

Then update the path in `subjective.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Linux:**
```bash
sudo apt install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

---

## How to Run

```bash
python subjective.py
```

The GUI will open. Then:

1. Enter the **Student Name** and **Subject Name**
2. Click **"Upload Prebuilt Answers"** → select a `.txt` file with the model answer
3. Click **"Upload Student Answer Image"** → select a `.png` / `.jpg` of the student's answer
4. Click **"Evaluate Answer"**
5. View the score and grade — results are saved automatically to `evaluation_results.xlsx`

---

## Sample Model Answer File (`sample_answer.txt`)

```
Photosynthesis is the process by which green plants convert sunlight into food.
It uses carbon dioxide and water to produce glucose and oxygen.
This process occurs in the chloroplasts of plant cells.
```

---

## Technologies Used

| Library        | Purpose                        |
|---------------|--------------------------------|
| `tkinter`      | GUI framework                  |
| `opencv-python`| Image preprocessing            |
| `pytesseract`  | OCR — extract text from images |
| `scikit-learn` | TF-IDF vectorizer & cosine similarity |
| `pandas`       | Save results to Excel          |
| `openpyxl`     | Excel file read/write          |
| `numpy`        | Numerical operations           |

---

## Output

Results are saved to `evaluation_results.xlsx` with columns:

| Student Name | Subject Name | Prebuilt Answer | Student Answer | Similarity Score (%) | Grade |
|---|---|---|---|---|---|

