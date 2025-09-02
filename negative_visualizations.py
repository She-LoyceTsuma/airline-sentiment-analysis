import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load CSV data
df = pd.read_csv('Tweets.csv')

# Filter negative tweets
negative_df = df[df['airline_sentiment'] == 'negative']

# Get unique airlines
airlines = sorted(negative_df['airline'].unique())

# Create a figure with subplots for each airline
fig, axes = plt.subplots(3, 2, figsize=(20, 18))
fig.suptitle('Top 10 Negative Reasons by Airline', fontsize=16, fontweight='bold')
axes = axes.flatten()

for i, airline in enumerate(airlines):
    airline_neg = negative_df[negative_df['airline'] == airline]
    reasons = airline_neg['negativereason'].value_counts().head(10)

    # Create horizontal bar chart
    bars = axes[i].barh(range(len(reasons)), reasons.values)
    axes[i].set_yticks(range(len(reasons)))
    axes[i].set_yticklabels(reasons.index, fontsize=8)
    axes[i].set_xlabel('Number of Complaints')
    axes[i].set_title(f'{airline}\n({len(airline_neg)} negative tweets)', fontweight='bold')

    # Add value labels on bars
    for j, bar in enumerate(bars):
        width = bar.get_width()
        axes[i].text(width + 5, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', ha='left', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('top10_negative_by_airline.png', dpi=300, bbox_inches='tight')
plt.show()

# Create overall top 10 visualization
plt.figure(figsize=(14, 10))
overall_reasons = negative_df['negativereason'].value_counts().head(10)

bars = plt.barh(range(len(overall_reasons)), overall_reasons.values)
plt.yticks(range(len(overall_reasons)), overall_reasons.index)
plt.xlabel('Number of Complaints')
plt.title('Overall Top 10 Negative Reasons Across All Airlines', fontweight='bold', fontsize=14)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + 30, bar.get_y() + bar.get_height()/2,
             f'{int(width)} ({width/len(negative_df)*100:.1f}%)',
             ha='left', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('overall_top10_negative.png', dpi=300, bbox_inches='tight')
plt.show()

# Create percentage-based visualization
plt.figure(figsize=(16, 10))

# Calculate percentages for each airline
percentage_data = {}
for airline in airlines:
    airline_neg = negative_df[negative_df['airline'] == airline]
    reasons = airline_neg['negativereason'].value_counts().head(5)  # Top 5 for clarity
    percentage_data[airline] = (reasons / len(airline_neg) * 100).round(1)

# Create DataFrame for heatmap
max_len = max(len(reasons) for reasons in percentage_data.values())
reason_names = set()
for reasons in percentage_data.values():
    reason_names.update(reasons.index)
reason_names = sorted(list(reason_names))[:10]  # Top 10 reasons overall

# Create percentage matrix
percentage_matrix = pd.DataFrame(index=reason_names, columns=airlines)

for airline in airlines:
    for reason in reason_names:
        if reason in percentage_data[airline].index:
            percentage_matrix.loc[reason, airline] = percentage_data[airline][reason]
        else:
            percentage_matrix.loc[reason, airline] = 0

# Create heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(percentage_matrix, annot=True, fmt='.1f', cmap='Reds',
            cbar_kws={'label': 'Percentage of Negative Tweets'})
plt.title('Negative Reason Distribution by Airline (Percentage)', fontweight='bold', fontsize=14)
plt.xlabel('Airline')
plt.ylabel('Negative Reason')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('negative_percentage_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Create comparative bar chart
plt.figure(figsize=(15, 10))

# Get top 5 reasons overall
top_5_overall = negative_df['negativereason'].value_counts().head(5).index

# Create data for each reason by airline
reason_by_airline = {}
for reason in top_5_overall:
    reason_by_airline[reason] = []
    for airline in airlines:
        airline_neg = negative_df[negative_df['airline'] == airline]
        count = (airline_neg['negativereason'] == reason).sum()
        reason_by_airline[reason].append(count)

# Plot
x = range(len(airlines))
width = 0.15

for i, (reason, counts) in enumerate(reason_by_airline.items()):
    plt.bar([pos + i*width for pos in x], counts, width, label=reason, alpha=0.8)

plt.xlabel('Airline')
plt.ylabel('Number of Complaints')
plt.title('Top 5 Negative Reasons Comparison Across Airlines', fontweight='bold', fontsize=14)
plt.xticks([pos + 2*width for pos in x], airlines, rotation=45)
plt.legend(title='Negative Reason', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('negative_reasons_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

print("Visualizations created:")
print("1. top10_negative_by_airline.png - Individual charts for each airline")
print("2. overall_top10_negative.png - Overall top 10 across all airlines")
print("3. negative_percentage_heatmap.png - Percentage distribution heatmap")
print("4. negative_reasons_comparison.png - Comparative bar chart")