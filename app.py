from flask import Flask, render_template, request
import pandas as pd
import re
import pickle
import json
import plotly
import plotly.express as px
import nltk
from nltk.corpus import stopwords
from sklearn.metrics import confusion_matrix, accuracy_score
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

try:
    stop_words = stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)
    stop_words = stopwords.words("english")

def clean_text(text):
    text = str(text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower()
    text = " ".join([w for w in text.split() if w not in stop_words])
    return text

df = pd.read_csv("phishing_email.csv")
df["cleaned_text"] = df["text_combined"].apply(clean_text)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

phishing = len(df[df["label"] == 1])
legit = len(df[df["label"] == 0])

fig1 = px.bar(
    x=["Phishing", "Legitimate"],
    y=[phishing, legit],
    title="Email Threat Distribution"
)

graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

y_true = df["label"]
y_pred = model.predict(vectorizer.transform(df["cleaned_text"]))

cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

fig2 = px.imshow(
    cm,
    text_auto=True,
    title="Confusion Matrix",
    labels=dict(x="Predicted", y="Actual")
)

graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

accuracy = accuracy_score(y_true, y_pred)

fig3 = px.bar(
    x=["Model Accuracy"],
    y=[accuracy],
    title="Model Accuracy"
)

graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

def generate_wordcloud():
    text = " ".join(df["text_combined"].astype(str))
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    img = BytesIO()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(img, format="png")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

wordcloud_img = generate_wordcloud()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        email = request.form["email"].strip()

        if not email:
            result = {
                "prediction": "Invalid Input",
                "confidence": "Please enter an email message"
            }
        else:
            cleaned = clean_text(email)

            if not cleaned:
                result = {
                    "prediction": "Invalid Input",
                    "confidence": "Text not meaningful after cleaning"
                }
            else:
                X_input = vectorizer.transform([cleaned])
                prediction = model.predict(X_input)[0]
                confidence = model.predict_proba(X_input)[0].max()

                result = {
                    "prediction": "Phishing" if prediction == 1 else "Legitimate",
                    "confidence": f"{confidence:.2%}"
                }

    return render_template(
        "index.html",
        result=result,
        accuracy=f"{accuracy:.2%}",
        graphJSON1=graphJSON1,
        graphJSON2=graphJSON2,
        graphJSON3=graphJSON3,
        wordcloud_img=wordcloud_img
    )

if __name__ == "__main__":
    app.run(port=8000, debug=True, threaded=True)