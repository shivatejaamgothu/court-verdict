import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ✅ Load dataset
df = pd.read_csv("dataset.csv")

# ✅ Check columns
print(df.head())

# Expected:
# text → case description
# ipc → IPC section (label)

# ✅ Features & Labels
X = df['text']
y = df['ipc']

# ✅ Vectorization (VERY IMPORTANT UPGRADE)
vectorizer = TfidfVectorizer(
    ngram_range=(1,2),   # unigrams + bigrams
    max_features=5000,
    stop_words='english'
)

X_vec = vectorizer.fit_transform(X)

# ✅ Model
model = LogisticRegression(max_iter=200)

# ✅ Train
model.fit(X_vec, y)

# ✅ Save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained and saved successfully!")
