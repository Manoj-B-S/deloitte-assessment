"""
Deloitte Graduate Hiring – AI & Machine Learning Assessment
============================================================
Candidate  : Manoj B S
Email      : bsmanoj65@gmail.com
College    : Alliance University, Bangalore
Skill Track: AI & Machine Learning
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report

# ─────────────────────────────────────────────────────────────
# TASK 1 – Data Generation & Preprocessing
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("TASK 1: Data Preprocessing & Exploratory Data Analysis")
print("=" * 60)

np.random.seed(42)
n = 200

data = pd.DataFrame({
    "age":            np.random.randint(22, 60, n),
    "experience":     np.random.randint(0, 35, n),
    "hours_per_week": np.random.randint(30, 60, n),
    "performance":    np.random.randint(1, 11, n),          # 1-10 score
    "salary":         np.random.randint(300000, 1500000, n) # in INR
})

# Inject a few missing values
data.loc[[5, 15, 42], "salary"] = np.nan
data.loc[[3, 77], "experience"] = np.nan

print("\nDataset shape:", data.shape)
print("\nFirst 5 rows:")
print(data.head())
print("\nMissing values before cleaning:")
print(data.isnull().sum())

# Fill missing values with column median
data.fillna(data.median(numeric_only=True), inplace=True)

print("\nMissing values after cleaning:")
print(data.isnull().sum())
print("\nBasic statistics:")
print(data.describe().round(2))


# ─────────────────────────────────────────────────────────────
# TASK 2 – Linear Regression (Salary Prediction)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TASK 2: Linear Regression – Salary Prediction")
print("=" * 60)

features = ["age", "experience", "hours_per_week", "performance"]
X = data[features].values
y = data["salary"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

lr = LinearRegression()
lr.fit(X_train_sc, y_train)
y_pred = lr.predict(X_test_sc)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\nModel Coefficients : {np.round(lr.coef_, 2)}")
print(f"Intercept          : {lr.intercept_:.2f}")
print(f"RMSE               : ₹{rmse:,.2f}")
print(f"R² Score           : {lr.score(X_test_sc, y_test):.4f}")

# Sample prediction
sample = np.array([[30, 5, 45, 8]])
sample_sc = scaler.transform(sample)
predicted_salary = lr.predict(sample_sc)[0]
print(f"\nSample prediction (age=30, exp=5yrs, 45hr/wk, perf=8): ₹{predicted_salary:,.0f}")


# ─────────────────────────────────────────────────────────────
# TASK 3 – Classification (Decision Tree)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TASK 3: Decision Tree Classifier – Performance Category")
print("=" * 60)

# Create target: Low (1-4), Medium (5-7), High (8-10)
def categorize(score):
    if score <= 4:
        return "Low"
    elif score <= 7:
        return "Medium"
    return "High"

data["category"] = data["performance"].apply(categorize)

X_cls = data[["age", "experience", "hours_per_week", "salary"]].values
y_cls = data["category"].values

X_tr, X_te, y_tr, y_te = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)

dt = DecisionTreeClassifier(max_depth=5, random_state=42)
dt.fit(X_tr, y_tr)
y_pred_cls = dt.predict(X_te)

print(f"\nAccuracy: {accuracy_score(y_te, y_pred_cls):.4f}")
print("\nClassification Report:")
print(classification_report(y_te, y_pred_cls, zero_division=0))


# ─────────────────────────────────────────────────────────────
# TASK 4 – Simple Neural Network from Scratch (NumPy)
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("TASK 4: Neural Network from Scratch (NumPy) – XOR Problem")
print("=" * 60)

# XOR dataset
X_xor = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=float)
y_xor = np.array([[0],[1],[1],[0]], dtype=float)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_deriv(z):
    s = sigmoid(z)
    return s * (1 - s)

np.random.seed(0)
W1 = np.random.randn(2, 4) * 0.5
b1 = np.zeros((1, 4))
W2 = np.random.randn(4, 1) * 0.5
b2 = np.zeros((1, 1))

lr_rate = 0.5
epochs  = 10000

for epoch in range(epochs):
    # Forward pass
    Z1 = X_xor @ W1 + b1
    A1 = sigmoid(Z1)
    Z2 = A1 @ W2 + b2
    A2 = sigmoid(Z2)

    # Loss (Binary Cross-Entropy)
    loss = -np.mean(y_xor * np.log(A2 + 1e-8) + (1 - y_xor) * np.log(1 - A2 + 1e-8))

    # Backward pass
    dA2 = -(y_xor / (A2 + 1e-8)) + (1 - y_xor) / (1 - A2 + 1e-8)
    dZ2 = dA2 * sigmoid_deriv(Z2)
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0, keepdims=True)

    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * sigmoid_deriv(Z1)
    dW1 = X_xor.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    W2 -= lr_rate * dW2
    b2 -= lr_rate * db2
    W1 -= lr_rate * dW1
    b1 -= lr_rate * db1

    if (epoch + 1) % 2000 == 0:
        print(f"  Epoch {epoch+1:5d} | Loss: {loss:.6f}")

predictions = (A2 > 0.5).astype(int)
print(f"\nXOR Predictions : {predictions.flatten().tolist()}")
print(f"Expected        : {y_xor.flatten().astype(int).tolist()}")
print(f"Accuracy        : {np.mean(predictions == y_xor) * 100:.1f}%")


# ─────────────────────────────────────────────────────────────
# TASK 5 – Rule-based Sentiment Analysis (NLP)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TASK 5: Sentiment Analysis (Rule-Based NLP)")
print("=" * 60)

POSITIVE_WORDS = {
    "good","great","excellent","amazing","outstanding","brilliant",
    "fantastic","wonderful","superb","best","love","enjoy","happy",
    "perfect","impressive","recommend","helpful","innovative","fast","clean"
}
NEGATIVE_WORDS = {
    "bad","poor","terrible","awful","horrible","worst","hate","slow",
    "broken","useless","disappointing","frustrating","annoying","ugly",
    "boring","failed","error","crash","difficult","confusing"
}
NEGATIONS = {"not","never","no","neither","nobody","nothing","nor","hardly"}

def analyze_sentiment(text: str) -> dict:
    tokens     = text.lower().split()
    pos = neg  = 0
    negate     = False

    for i, tok in enumerate(tokens):
        clean = tok.strip(".,!?;:")
        if clean in NEGATIONS:
            negate = True
            continue
        if clean in POSITIVE_WORDS:
            neg += 1 if negate else 0
            pos += 0 if negate else 1
        elif clean in NEGATIVE_WORDS:
            pos += 1 if negate else 0
            neg += 0 if negate else 1
        negate = False  # reset after one word

    score = pos - neg
    if score > 0:
        label = "POSITIVE 😊"
    elif score < 0:
        label = "NEGATIVE 😞"
    else:
        label = "NEUTRAL 😐"

    return {"text": text, "positive": pos, "negative": neg, "score": score, "sentiment": label}

reviews = [
    "The product is excellent and the support team is very helpful.",
    "This is the worst experience I have ever had. Totally broken and slow.",
    "Not bad, but could be better. Average performance.",
    "I love the clean interface and amazing features!",
    "The app crashes frequently. Very frustrating and annoying.",
    "Not a bad product actually, works great for me.",
]

for review in reviews:
    result = analyze_sentiment(review)
    print(f"\n  Text     : {result['text'][:65]}...")
    print(f"  Pos/Neg  : {result['positive']}/{result['negative']}  | Score: {result['score']}")
    print(f"  Sentiment: {result['sentiment']}")


print("\n" + "=" * 60)
print("  ALL TASKS COMPLETED SUCCESSFULLY")
print("  Candidate: [Your Full Name] | Track: AI & Machine Learning")
print("=" * 60)
