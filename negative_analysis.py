import pandas as pd

# Load CSV data
df = pd.read_csv('Tweets.csv')

# Filter negative tweets
negative_df = df[df['airline_sentiment'] == 'negative']

print("TOP 10 NEGATIVE REASONS FOR EACH AIRLINE")
print("=" * 50)

# Get unique airlines and sort them
airlines = sorted(negative_df['airline'].unique())

for airline in airlines:
    print(f"\n{airline.upper()}:")
    print("-" * (len(airline) + 1))

    airline_neg = negative_df[negative_df['airline'] == airline]
    total_neg = len(airline_neg)
    print(f"Total negative tweets: {total_neg}")

    if 'negativereason' in airline_neg.columns:
        reasons = airline_neg['negativereason'].value_counts().head(10)

        print("\nTop 10 Negative Reasons:")
        for i, (reason, count) in enumerate(reasons.items(), 1):
            percentage = (count / total_neg) * 100
            print(f"{i:2d}. {reason}: {count} ({percentage:.1f}%)")

        # Show some example tweets for the top reason
        if len(reasons) > 0:
            top_reason = reasons.index[0]
            print(f"\nExample tweets for '{top_reason}':")
            examples = airline_neg[airline_neg['negativereason'] == top_reason]['text'].head(3)
            for j, tweet in enumerate(examples, 1):
                print(f"  {j}. {tweet[:100]}...")
    else:
        print("No negative reason data available")

print("\n" + "=" * 50)
print("OVERALL TOP 10 NEGATIVE REASONS ACROSS ALL AIRLINES")
print("=" * 50)

overall_reasons = negative_df['negativereason'].value_counts().head(10)
total_all_neg = len(negative_df)

for i, (reason, count) in enumerate(overall_reasons.items(), 1):
    percentage = (count / total_all_neg) * 100
    print(f"{i:2d}. {reason}: {count} ({percentage:.1f}%)")

print(f"\nTotal negative tweets across all airlines: {total_all_neg}")