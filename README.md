# Phishing Email Detection System

A Python web application that classifies submitted email text as **Phishing** or **Legitimate** using a saved machine-learning model. The Flask interface also presents dataset/model evaluation visualizations, including email-label distribution, a confusion matrix, model accuracy, and a word cloud.

> **Important:** This project is a learning and demonstration tool, not a complete email-security product. Predictions can be wrong. Do not use it as the sole basis for deciding whether an email is safe.

## Features

- Web form for submitting email text for classification
- Text preprocessing using regular expressions and NLTK English stopwords
- Saved scikit-learn model and text vectorizer
- Prediction label and model-reported confidence score
- Plotly charts for label distribution, confusion matrix, and accuracy
- Word-cloud visualization of dataset text
- Flask development entry point and Waitress server entry point

## Technology stack

- Python
- Flask
- pandas
- scikit-learn
- NLTK
- Plotly
- WordCloud and Matplotlib
- Waitress (serving entry point)

## Project structure

```text
phishing-email-detection/
├── app.py                  # Flask routes, preprocessing, predictions, analytics
├── server.py               # Waitress server entry point
├── model.pkl               # Saved trained model (required for predictions)
├── vectorizer.pkl          # Saved text vectorizer (required for predictions)
├── phishing_email.csv      # Local dataset; not included in this repository
├── requirements.txt        # Python dependencies
├── .gitignore
├── ARCHITECTURE.md         # Architecture and workflow diagram
├── templates/
│   └── index.html          # Web interface
└── screenshots/
    └── .gitkeep            # Add application screenshots here
```

## Requirements

- Python 3.10+ recommended; use the Python version with which the saved model was created if you encounter scikit-learn pickle compatibility warnings.
- The dataset file `phishing_email.csv`
- The matching `model.pkl` and `vectorizer.pkl` files

The dataset is intentionally not included because it exceeds GitHub's 100 MB per-file limit. The app currently reads the CSV at startup and expects these columns:

- `text_combined` — email text used for preprocessing
- `label` — target label, where `1` is phishing and `0` is legitimate

Obtain the dataset from its original, permitted source and place it in the project root. Do not commit private, licensed, or sensitive email data without permission. The saved model and vectorizer must be a matching pair from the same training pipeline.

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/Ayushman2004-collab/phishing-email-detection.git
cd phishing-email-detection
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add required local files

Place `phishing_email.csv`, `model.pkl`, and `vectorizer.pkl` in the project root. The CSV is required by the current app for its dashboard analytics as well as the labels used to calculate the displayed evaluation metrics.

### 5. Start the app

Development server:

```bash
python app.py
```

Open http://127.0.0.1:8000 in your browser.

Waitress server:

```bash
python server.py
```

Open http://127.0.0.1:5000 in your browser.

## How it works

1. A user pastes email text into the web form.
2. The preprocessing function removes HTML-like tags and URLs, keeps alphabetic characters, lowercases the text, and removes English stopwords.
3. The saved vectorizer converts the cleaned text to the feature representation expected by the saved model.
4. The model predicts a class: `1` is displayed as **Phishing** and `0` as **Legitimate**.
5. The app displays the predicted class and the maximum probability returned by `predict_proba`, formatted as a confidence percentage.

The current app calculates dashboard charts from the local CSV when the server starts. The accuracy shown by the app is calculated by predicting on the same dataset loaded for the dashboard; it should **not** be interpreted as an independent test-set score unless the dataset and evaluation method are confirmed to be held out.

## Screenshots

Add screenshots of your own running application to `screenshots/`, then embed them here. Suggested captures:

- `screenshots/home.png` — initial web page
- `screenshots/phishing-result.png` — a sample phishing prediction
- `screenshots/dashboard.png` — dashboard charts

Only use test messages or data that you have permission to share. Avoid including real people's private emails or sensitive information.

## Limitations and security notes

- This is a text-classification demonstration, not a mail gateway or complete phishing defense.
- The result depends on the training data, preprocessing, model, and vectorizer; false positives and false negatives are possible.
- The displayed confidence is the model's reported probability, not a guarantee that the prediction is correct.
- The current evaluation chart uses predictions over the CSV loaded by the application. If that is the training data, the displayed accuracy may be optimistic.
- The app uses Python pickle files. Only load model/vectorizer files from a trusted source; pickle files can execute code when deserialized.
- The current development entry point enables Flask debug mode. Use a production configuration and do not expose the debug server to the public internet.
- The current preprocessing strips URLs, which can remove potentially useful phishing indicators. Consider URL/domain features, robust HTML parsing, and additional email-header features as future improvements.

## Future improvements

- Separate training, validation, and test evaluation with precision, recall, F1-score, and ROC-AUC where appropriate
- Add unit tests for preprocessing and prediction
- Add a safe dataset-download/configuration step and make dashboard analytics optional when the CSV is absent
- Improve validation, error handling, logging, and production configuration
- Add screenshots and a short demo video
- Evaluate performance on recent, diverse emails and document dataset provenance and licensing

## Author

Add your name and preferred portfolio/contact links here.

## Disclaimer

For educational and research use. This tool does not guarantee detection of all phishing emails and should not replace user awareness, email security controls, or verification through trusted channels.
