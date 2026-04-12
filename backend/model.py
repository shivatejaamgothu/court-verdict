import pandas as pd
import pickle
import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.utils.class_weight import compute_class_weight

nltk.download('punkt')
nltk.download('stopwords')

# ✅ Load dataset
df = pd.read_csv("dataset.csv")

# ✅ Text Cleaning Function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    words = [w for w in words if w not in stop_words]

    return " ".join(words)

# ✅ Apply cleaning
df['clean_text'] = df['text'].apply(clean_text)

# ✅ Features & Labels
X = df['clean_text']
y = df['ipc']

# ✅ Handle Class Imbalance (IMPORTANT 🔥)
classes = y.unique()
weights = compute_class_weight(class_weight='balanced', classes=classes, y=y)
class_weights = dict(zip(classes, weights))

# ✅ Better Vectorizer
vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    max_features=8000,
    min_df=2,             # ignore rare words
    max_df=0.9            # ignore very common words
)

X_vec = vectorizer.fit_transform(X)

# ✅ Improved Model
model = LogisticRegression(
    max_iter=300,
    class_weight=class_weights
)

# ✅ Train
model.fit(X_vec, y)

# ✅ Save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Improved Model trained successfully!")
