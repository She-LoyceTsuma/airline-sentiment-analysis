import pandas as pd
import sqlite3
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load CSV data
df = pd.read_csv('Tweets.csv')

# Display basic info
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Sentiment distribution from existing labels
print("\nSentiment distribution:")
print(df['airline_sentiment'].value_counts())

# Perform sentiment analysis using TextBlob
def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

df['predicted_sentiment'] = df['text'].apply(get_sentiment)

# Compare predicted vs actual
print("\nPredicted sentiment distribution:")
print(df['predicted_sentiment'].value_counts())

# Accuracy
accuracy = (df['airline_sentiment'] == df['predicted_sentiment']).mean()
print(f"\nAccuracy of TextBlob predictions: {accuracy:.2f}")

# Visualization 1: Sentiment distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='airline_sentiment', palette='viridis')
plt.title('Distribution of Airline Sentiments')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.savefig('sentiment_distribution.png')
plt.show()

# Visualization 2: Sentiment by airline
plt.figure(figsize=(12, 8))
sns.countplot(data=df, x='airline', hue='airline_sentiment', palette='viridis')
plt.title('Sentiment Distribution by Airline')
plt.xlabel('Airline')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Sentiment')
plt.savefig('sentiment_by_airline.png')
plt.show()

# Visualization 3: Negative reasons
negative_df = df[df['airline_sentiment'] == 'negative']
if 'negativereason' in df.columns:
    plt.figure(figsize=(12, 8))
    negative_reasons = negative_df['negativereason'].value_counts().head(10)
    negative_reasons.plot(kind='bar', color='red')
    plt.title('Top 10 Negative Reasons')
    plt.xlabel('Reason')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.savefig('negative_reasons.png')
    plt.show()

    # Visualization 4: Negative reasons by airline
    plt.figure(figsize=(14, 10))
    negative_by_airline = negative_df.groupby(['airline', 'negativereason']).size().unstack().fillna(0)
    negative_by_airline.plot(kind='bar', stacked=True, figsize=(14, 10), colormap='Reds')
    plt.title('Negative Reasons by Airline')
    plt.xlabel('Airline')
    plt.ylabel('Count')
    plt.legend(title='Negative Reason', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('negative_reasons_by_airline.png')
    plt.show()

    # Print detailed negative reasons analysis - Top 10 per airline
    print("\nDetailed Negative Reasons Analysis (Top 10 per Airline):")
    print("=======================================================")
    for airline in sorted(negative_df['airline'].unique()):
        print(f"\n{airline}:")
        airline_neg = negative_df[negative_df['airline'] == airline]
        reasons = airline_neg['negativereason'].value_counts().head(10)
        total_neg = len(airline_neg)
        print(f"  Total negative tweets: {total_neg}")
        print("  Top 10 reasons:")
        for i, (reason, count) in enumerate(reasons.items(), 1):
            percentage = (count / total_neg) * 100
            print(f"    {i}. {reason}: {count} ({percentage:.1f}%)")

    # Summary of top reasons across all airlines
    print("\n\nOverall Top 10 Negative Reasons Across All Airlines:")
    print("====================================================")
    overall_reasons = negative_df['negativereason'].value_counts().head(10)
    total_all_neg = len(negative_df)
    for i, (reason, count) in enumerate(overall_reasons.items(), 1):
        percentage = (count / total_all_neg) * 100
        print(f"{i}. {reason}: {count} ({percentage:.1f}%)")

    # Visualization 5: Negative sentiment confidence
    plt.figure(figsize=(10, 6))
    plt.hist(negative_df['airline_sentiment_confidence'], bins=20, alpha=0.7, color='red', edgecolor='black')
    plt.title('Confidence Distribution for Negative Sentiments')
    plt.xlabel('Confidence Score')
    plt.ylabel('Frequency')
    plt.savefig('negative_confidence_distribution.png')
    plt.show()

# Check SQLite database
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\nTables in database.sqlite:")
for table in tables:
    print(table[0])

# If there are tables, explore the first one
if tables:
    table_name = tables[0][0]
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    rows = cursor.fetchall()
    print(f"\nFirst 5 rows from {table_name}:")
    for row in rows:
        print(row)

conn.close()

print("\nAnalysis complete. Visualizations saved as PNG files.")