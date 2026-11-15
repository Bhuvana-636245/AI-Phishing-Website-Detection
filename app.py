import streamlit as st
import pandas as pd
import joblib
import os
from urllib.parse import urlparse

from feature_extraction import extract_url_features


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="AI Phishing Detection",
    page_icon="🔍",
    layout="centered"
)


# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>

.main {
    background-color: #f8f9fc;
}

.title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #17365D;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #555555;
}

.stButton button {
    width: 100%;
    border-radius: 8px;
    height: 45px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# FEATURE COLUMNS
# -------------------------------

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


# -------------------------------
# LOAD MODEL
# -------------------------------

MODEL_PATH = "models/phishing_model.pkl"

try:
    if not os.path.exists(MODEL_PATH):
        st.error("Model not found. Run train_model.py first.")
        st.stop()

    model = joblib.load(MODEL_PATH)

except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()


# -------------------------------
# URL VALIDATION
# -------------------------------

def validate_url(url):

    url = url.strip()

    if not url:
        return False, "Please enter a URL."

    if any(char.isspace() for char in url):
        return False, "URL must not contain spaces."

    if not url.startswith(("http://", "https://")):
        return False, "URL must start with http:// or https://"

    try:
        parsed = urlparse(url)

        if not parsed.hostname or "." not in parsed.hostname:
            return False, "Please enter a valid website URL."

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            return False, "Invalid port number."

    except ValueError:
        return False, "Invalid URL format."

    return True, "Valid URL"


# -------------------------------
# CLEAR INPUT
# -------------------------------

def clear_input():
    st.session_state.url_input = ""


# -------------------------------
# APPLICATION HEADER
# -------------------------------

st.markdown(
    '<div class="title">AI-Powered Phishing Website Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Machine Learning Based Website URL Analysis</div>',
    unsafe_allow_html=True
)

st.write("")

st.info(
    "Enter a website URL to identify whether it is potentially "
    "phishing or legitimate."
)

st.divider()


# -------------------------------
# URL INPUT
# -------------------------------

url = st.text_input(
    "Website URL",
    placeholder="https://example.com",
    key="url_input"
)


# -------------------------------
# BUTTONS
# -------------------------------

col1, col2 = st.columns(2)

with col1:
    analyse = st.button("Analyse URL")

with col2:
    st.button("Clear", on_click=clear_input)


# -------------------------------
# ANALYSIS
# -------------------------------

if analyse:

    is_valid, message = validate_url(url)

    if not is_valid:

        st.error(message)

    else:

        try:

            features = extract_url_features(url.strip())

            input_data = pd.DataFrame(
                [features],
                columns=FEATURE_COLUMNS
            )

            prediction = model.predict(input_data)[0]

            probabilities = model.predict_proba(input_data)[0]

            confidence = max(probabilities) * 100

            st.divider()

            st.subheader("Analysis Result")

            if prediction == 0:

                st.error("Potential Phishing Website Detected!")

                st.write(
                    "The model has classified this URL as "
                    "potentially malicious."
                )

            elif prediction == 1:

                st.success("Predicted as Legitimate Website")

                st.write(
                    "The model has classified this URL as "
                    "potentially legitimate."
                )

            else:

                st.warning("Unknown prediction class.")

            st.metric(
                label="Model Prediction Confidence",
                value=f"{confidence:.2f}%"
            )

            st.progress(int(confidence))

            # FEATURE DETAILS

            with st.expander("View Extracted URL Features"):

                feature_table = pd.DataFrame(
                    features.items(),
                    columns=["Feature", "Value"]
                )

                st.dataframe(
                    feature_table,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:

            st.error(f"Analysis failed: {e}")


# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "Disclaimer: This is an automated prediction, not a guarantee "
    "that the website is safe or malicious."
)

st.caption(
    "Developed as an academic machine learning project."
)