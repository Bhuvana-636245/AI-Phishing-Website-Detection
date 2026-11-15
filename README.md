# AI-Powered Phishing Website Detection

## 1. Project Overview

AI-Powered Phishing Website Detection is a machine learning-based application designed to identify potentially phishing and legitimate website URLs.

The system analyses URL characteristics using feature extraction techniques and predicts the URL category using a trained Random Forest classifier.

An interactive web application is developed using Streamlit to allow users to enter URLs and view prediction results.

## 2. Objectives

- Detect potentially phishing website URLs.
- Identify legitimate website URLs.
- Extract important URL-based features.
- Apply machine learning for URL classification.
- Display prediction results and confidence scores.

## 3. Technologies Used

- Python
- Machine Learning
- Random Forest Classifier
- Pandas
- Scikit-learn
- Streamlit
- Joblib

## 4. System Architecture

User Input
↓
URL Validation
↓
URL Feature Extraction
↓
Feature Processing
↓
Random Forest Model
↓
Phishing / Legitimate Prediction
↓
Display Analysis Result

## 5. Features Extracted

The system extracts 16 URL-based features:

1. URL Length
2. IP Address Detection
3. Dot Count
4. HTTPS Flag
5. URL Entropy
6. Token Count
7. Subdomain Count
8. Query Parameter Count
9. TLD Length
10. Path Length
11. Hyphen in Domain
12. Number of Digits
13. TLD Popularity
14. Suspicious File Extension
15. Domain Name Length
16. Percentage of Numeric Characters

## 6. Machine Learning Model

The project uses a Random Forest Classifier to classify URLs into two categories:

- Class 0: Phishing
- Class 1: Legitimate

The model was evaluated using a hostname-separated training and testing split.

Dataset evaluation accuracy: Approximately 99.94%.

## 7. Application Features

- Website URL input.
- URL format validation.
- Phishing and legitimate URL classification.
- Model prediction confidence display.
- Extracted URL feature visualization.
- Error handling.
- Clear input option.

## 8. Application Testing

The application was manually tested using:

- 6 phishing URL examples.
- 5 legitimate URL examples.

All 11 examples received the expected predictions.

These preliminary manual results do not establish real-world detection accuracy.

## 9. Project Structure

```text
AI_Phishing_Detection/
│
├── dataset/
│   └── cleaned_url_features.csv
│
├── models/
│   └── phishing_model.pkl
│
├── app.py
├── feature_extraction.py
├── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 10. How to Run the Project

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Train the model

```bash
python train_model.py
```

### Step 3: Run the application

```bash
streamlit run app.py
```

### Step 4: Analyse a URL

Enter a website URL in the application and click the Analyse URL button to view the prediction.

## 11. Limitations

- Detection is based on URL characteristics.
- The application does not perform complete website security verification.
- Predictions may contain false positives and false negatives.
- Dataset evaluation performance does not guarantee real-world performance.

## 12. Future Enhancements

- Integrate domain reputation checking.
- Include webpage content analysis.
- Improve detection using larger and diverse datasets.
- Develop a browser extension for URL checking.

## 13. Conclusion

This project demonstrates the application of machine learning in phishing website detection. It uses URL feature extraction and a Random Forest classifier to identify potentially suspicious website URLs through an interactive Streamlit application.