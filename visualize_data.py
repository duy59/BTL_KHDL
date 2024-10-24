import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load the JSON data
with open('crawledData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Filter out non-dictionary items
filtered_data = [item for item in data if isinstance(item, dict)]

# Convert JSON data to DataFrame
df = pd.DataFrame(filtered_data)

# Display the first few rows of the DataFrame
print(df.head())

# Check if 'author' and 'category' columns exist
if 'author' in df.columns and 'category' in df.columns:
    # Plotting the number of articles per author
    plt.figure(figsize=(10, 6))
    author_counts = df['author'].value_counts()
    sns.barplot(x=author_counts.index, y=author_counts.values, palette='viridis')
    plt.title('Number of Articles per Author')
    plt.xlabel('Author')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plotting the number of articles per category
    plt.figure(figsize=(10, 6))
    category_counts = df['category'].apply(lambda x: x['name']).value_counts()
    sns.barplot(x=category_counts.index, y=category_counts.values, palette='viridis')
    plt.title('Number of Articles per Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Check if 'content' column exists
if 'content' in df.columns:
    # Plotting the distribution of article lengths
    df['content_length'] = df['content'].apply(len)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['content_length'], bins=30, kde=True, color='blue')
    plt.title('Distribution of Article Lengths')
    plt.xlabel('Content Length')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
else:
    print("The 'content' column is missing in the data.")