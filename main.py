"""
Final Submission File: HTML Article Analysis
Author: Ashitha P
Description: Extracts textual content from saved HTML files, performs sentiment
analysis, and calculates text metrics such as polarity, subjectivity, FOG index, 
and complexity scores. Saves results in the specified output format.
"""

import os
import re
import string
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# -----------------------------
# 1. LOAD INPUT FILES
# -----------------------------
input_df = pd.read_excel("Input.xlsx")
output_format = pd.read_excel("Output Data Structure.xlsx")

# -----------------------------
# 2. LOAD STOPWORDS
# -----------------------------
def load_stopwords(folder_path):
    """
    Load custom stopwords from all files in the given folder.
    """
    stop_words = set()
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r', encoding='latin-1') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    stop_words.add(word)
    return stop_words

custom_stopwords = load_stopwords("StopWords")
nltk_stopwords = set(stopwords.words('english'))
stop_words = custom_stopwords.union(nltk_stopwords)

# -----------------------------
# 3. LOAD MASTER DICTIONARY
# -----------------------------
def load_word_list(filepath):
    """
    Load a list of words from a text file, ignoring comments and blank lines.
    """
    words = set()
    with open(filepath, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip().lower()
            if line and not line.startswith(";"):
                words.add(line)
    return words

positive_words = load_word_list("MasterDictionary/positive-words.txt") - stop_words
negative_words = load_word_list("MasterDictionary/negative-words.txt") - stop_words

# -----------------------------
# 4. EXTRACT ARTICLE FROM HTML
# -----------------------------
def extract_article_from_file(filepath):
    """
    Extract the title and main content from the HTML file.
    Checks multiple possible container tags for content.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        title_tag = soup.find("h1")
        title = title_tag.get_text().strip() if title_tag else ""

        # Candidate containers for article content
        containers = [
            ("div", "td-post-content"),
            ("article", None),
            ("div", "content"),
            ("section", None),
            ("div", "post-body")
        ]

        article = ""
        for tag, class_name in containers:
            if article.strip():
                break
            container = soup.find(tag, class_=class_name) if class_name else soup.find(tag)
            if container:
                paragraphs = container.find_all("p")
                if paragraphs:
                    article = " ".join(p.get_text().strip() for p in paragraphs)
                else:
                    article = container.get_text().strip()

        if not article.strip():
            print("No usable content found in:", os.path.basename(filepath))
        else:
            print(f"Extracted length for {os.path.basename(filepath)}: {len(article)}")

        return title, article.strip()

    except Exception as e:
        print("Error reading file:", filepath, "|", e)
        return "", ""

# -----------------------------
# 5. CLEAN WORDS
# -----------------------------
def clean_words(text):
    """
    Lowercase, remove punctuation, tokenize, and remove stopwords.
    """
    text = text.lower()
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    words = word_tokenize(text)
    return [w for w in words if w.isalpha() and w not in stop_words]

# -----------------------------
# 6. SYLLABLE COUNT
# -----------------------------
def count_syllables(word):
    """
    Count approximate number of syllables in a word.
    """
    vowels = "aeiou"
    word = word.lower()
    if word.endswith(("es", "ed")):
        word = word[:-2]
    syllables = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                syllables += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    return max(syllables, 1)

# -----------------------------
# 7. PERSONAL PRONOUN COUNT
# -----------------------------
def count_pronouns(text):
    """
    Count personal pronouns: I, we, my, ours (excluding 'us').
    """
    matches = re.findall(r'\b(I|we|my|ours|us)\b', text, flags=re.IGNORECASE)
    return sum(1 for m in matches if m.lower() != "us")

# -----------------------------
# 8. SPLIT LONG PARAGRAPHS
# -----------------------------
def split_paragraphs_to_sentences(text):
    """
    Split text into sentences by common delimiters.
    """
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)
    sentences = [part.strip() for part in re.split(r'[.!?;]+', text) if part.strip()]
    return sentences

# -----------------------------
# 9. ANALYSIS FUNCTION
# -----------------------------
def analyze(text):
    """
    Compute all text metrics including:
    positive/negative scores, polarity, subjectivity,
    average sentence length, complex words, FOG index, etc.
    """
    sentences = split_paragraphs_to_sentences(text)
    words = clean_words(text)
    total_words = len(words)
    total_sentences = len(sentences)

    positive_score = sum(1 for w in words if w in positive_words)
    negative_score = sum(1 for w in words if w in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 1e-6)
    subjectivity_score = (positive_score + negative_score) / (total_words + 1e-6)

    avg_sentence_length = total_words / total_sentences if total_sentences else 0
    complex_words = [w for w in words if count_syllables(w) > 2]
    complex_word_count = len(complex_words)
    percentage_complex_words = complex_word_count / total_words if total_words else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    syllable_per_word = sum(count_syllables(w) for w in words) / total_words if total_words else 0
    pronouns = count_pronouns(text)
    avg_word_length = sum(len(w) for w in words) / total_words if total_words else 0

    return [
        positive_score,
        negative_score,
        polarity_score,
        subjectivity_score,
        avg_sentence_length,
        percentage_complex_words,
        fog_index,
        avg_sentence_length,
        complex_word_count,
        total_words,
        syllable_per_word,
        pronouns,
        avg_word_length
    ]

# -----------------------------
# 10. PROCESS ALL ARTICLES
# -----------------------------
results = []
missing_files = []
folder_path = "Saved_HTML"

for _, row in input_df.iterrows():
    url_id = row['URL_ID']
    file_path = os.path.join(folder_path, url_id)

    if os.path.exists(file_path):
        title, article = extract_article_from_file(file_path)
        if not article:
            print("Missing usable content for:", url_id)
            missing_files.append(url_id)
            metrics = [0]*13
        else:
            metrics = analyze(article)
    else:
        print("Missing file for:", url_id)
        missing_files.append(url_id)
        metrics = [0]*13

    results.append(list(row) + metrics)

# Save missing files log
with open("missing_files.txt", "w") as f:
    f.write("\n".join(missing_files))

# -----------------------------
# 11. SAVE OUTPUT
# -----------------------------
final_df = pd.DataFrame(results, columns=output_format.columns)
final_df.to_excel("Output.xlsx", index=False)
print("Assignment Completed Successfully")