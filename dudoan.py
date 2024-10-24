import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Bước 1: Tiền xử lý dữ liệu
def preprocess_data(data):
    texts = []
    labels = []
    for item in data:
        texts.append(item['content'])
        labels.append(item['category']['name'])
    return texts, labels

# Đọc dữ liệu từ tệp JSON
import json
with open('crawledData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

texts, labels = preprocess_data(data)

# Chuyển đổi nhãn thành số
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(texts, labels_encoded, test_size=0.2, random_state=42)

# Bước 2: Chuyển đổi văn bản thành vector sử dụng BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(X_train, truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(X_test, truncation=True, padding=True, max_length=512)

# Bước 3: Tạo mô hình học sâu sử dụng BERT
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_encoder.classes_))

# Bước 4: Huấn luyện mô hình
train_dataset = tf.data.Dataset.from_tensor_slices((dict(train_encodings), y_train)).shuffle(1000).batch(16)
test_dataset = tf.data.Dataset.from_tensor_slices((dict(test_encodings), y_test)).batch(16)

optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
model.compile(optimizer=optimizer, loss=model.compute_loss, metrics=['accuracy'])

model.fit(train_dataset, epochs=3, validation_data=test_dataset)

# Bước 5: Đánh giá mô hình
loss, accuracy = model.evaluate(test_dataset)
print(f'Accuracy: {accuracy}')