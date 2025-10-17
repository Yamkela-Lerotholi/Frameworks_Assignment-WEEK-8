
# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(layout="wide")
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers interactively!")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv')
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['abstract'] = df['abstract'].fillna('')
    return df

df = load_data()

# Sidebar filters
year_range = st.slider("Select year range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show data sample
st.subheader("Sample of Papers")
st.dataframe(filtered_df[['title','journal','publish_time','source_x']].head(20))

# Visualization: Papers per year
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, palette='viridis', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Visualization: Top journals
st.subheader("Top 10 Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, palette='magma', ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# Visualization: Word Cloud of Titles
st.subheader("Word Cloud of Paper Titles")
text = " ".join(str(title) for title in filtered_df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)
