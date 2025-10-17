
# CORD19_analysis.ipynb

# -------------------------------
# PART 1: LOAD DATA & EXPLORATION
# -------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
df = pd.read_csv('metadata.csv')

# Basic info
print("Shape of dataset:", df.shape)
print(df.info())
print(df.head())
print(df.isnull().sum())

# -------------------------------
# PART 2: DATA CLEANING
# -------------------------------
# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Extract year
df['year'] = df['publish_time'].dt.year

# Fill missing abstracts with empty string
df['abstract'] = df['abstract'].fillna('')

# Optional: abstract word count
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

# Drop columns with too many missing values (optional)
threshold = 0.5  # remove if >50% missing
df = df[df.columns[df.isnull().mean() < threshold]]

# -------------------------------
# PART 3: ANALYSIS & VISUALIZATION
# -------------------------------

# 1. Papers per year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
sns.barplot(x=year_counts.index, y=year_counts.values, palette='viridis')
plt.title('Publications by Year')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.show()

# 2. Top 10 journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='magma')
plt.title('Top 10 Journals Publishing COVID-19 Research')
plt.xlabel('Number of Papers')
plt.ylabel('Journal')
plt.show()

# 3. Word Cloud of paper titles
text = " ".join(str(title) for title in df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(15,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles')
plt.show()

# 4. Distribution by source
source_counts = df['source_x'].value_counts()
plt.figure(figsize=(8,5))
sns.barplot(x=source_counts.index, y=source_counts.values, palette='coolwarm')
plt.title('Distribution of Papers by Source')
plt.xlabel('Source')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()
