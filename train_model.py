import pandas as pd
import joblib
import os

from urllib.parse import urlparse
from feature_extraction import extract_url_features

from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# Feature order
FEATURE_COLUMNS = [
    "url_length",
    "has_ip_address",
    "dot_count",
    "https_flag",
    "url_entropy",
    "token_count",
    "subdomain_count",
    "query_param_count",
    "tld_length",
    "path_length",
    "has_hyphen_in_domain",
    "number_of_digits",
    "tld_popularity",
    "suspicious_file_extension",
    "domain_name_length",
    "percentage_numeric_chars"
]


# Load dataset
data = pd.read_csv("dataset/cleaned_url_features.csv")

data = data.dropna(subset=["URL", "ClassLabel"])
data = data.drop_duplicates(subset=["URL"])

# Extract hostname
def get_hostname(url):
    try:
        return urlparse(str(url)).hostname
    except ValueError:
        return None


data["hostname"] = data["URL"].apply(get_hostname)
data = data.dropna(subset=["hostname"])

# Recalculate features using our feature extraction code
print("Extracting URL features...")

X = pd.DataFrame(
    data["URL"].apply(extract_url_features).tolist()
)

X = X[FEATURE_COLUMNS]

y = data["ClassLabel"]
groups = data["hostname"]

# Domain-based train-test split
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(X, y, groups)
)

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

print("\nTraining model...")

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/phishing_model.pkl")

print("\nUpdated model saved successfully!")