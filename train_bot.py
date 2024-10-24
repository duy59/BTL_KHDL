import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from bs4 import BeautifulSoup
import re

# Load the JSON data
with open('crawledData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Filter out non-dictionary items
filtered_data = [item for item in data if isinstance(item, dict)]

# Convert JSON data to DataFrame
df = pd.DataFrame(filtered_data)

# Clean the text data
def clean_text(text):
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

df['clean_content'] = df['content'].apply(clean_text)

# Encode the target labels
df['category_name'] = df['category'].apply(lambda x: x['name'])
df = df.dropna(subset=['clean_content', 'category_name'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['clean_content'], df['category_name'], test_size=0.2, random_state=42)

# Feature extraction using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
import joblib
joblib.dump(model, 'text_classification_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')