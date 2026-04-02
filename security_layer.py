import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# 🔥 Rule-based layer (VERY IMPORTANT)
dangerous_patterns = [
    "rm -rf",
    "/etc/shadow",
    "chmod 777",
    "kill -9",
]

def rule_check(text):
    for pattern in dangerous_patterns:
        if pattern in text:
            return "BLOCK ❌ (Rule-based)"
    return None


def predict(text):
    X = vectorizer.transform([text])
    probs = model.predict_proba(X)[0]
    label = model.classes_[probs.argmax()]
    confidence = max(probs)
    return label, confidence


def security_check(text):
    # 🔥 1. Rule-based check first
    rule_result = rule_check(text)
    if rule_result:
        print("RULE TRIGGERED!")
        return rule_result

    # 🔥 2. ML check
    label, confidence = predict(text)

    print(f"DEBUG → Label: {label}, Confidence: {confidence:.2f}")

    if label == "DANGEROUS":
        return "BLOCK ❌"

    if label == "SENSITIVE":
        return "WARN ⚠️"

    if label == "SAFE":
        if confidence < 0.4:
            return "WARN ⚠️"
        return "ALLOW ✅"