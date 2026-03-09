

# HTML Article Text Analysis using NLP

## Author

**Ashitha P**

## Project Description

This project performs **text extraction and natural language processing (NLP)** on articles obtained from the **Blackcoffer Insights website**.

The program reads **saved HTML article files**, extracts the **title and article content**, and performs **sentiment analysis and readability analysis** using a predefined **Master Dictionary and StopWords list**.

The final output calculates multiple **text analysis variables** such as:

* Positive Score
* Negative Score
* Polarity Score
* Subjectivity Score
* Average Sentence Length
* Percentage of Complex Words
* Fog Index
* Complex Word Count
* Word Count
* Syllable Per Word
* Personal Pronouns
* Average Word Length

The results are saved in the **required output format specified in the assignment**.

---

# Project Workflow

The solution follows these main steps:

### 1. Input Loading

* Reads article URLs and IDs from `Input.xlsx`
* Reads output structure from `Output Data Structure.xlsx`

### 2. Stopwords Loading

Stopwords are loaded from:

* Custom stopwords provided in the **StopWords folder**
* NLTK English stopwords

Both are combined to create a **complete stopword list**.

### 3. Master Dictionary Loading

Positive and negative word lists are loaded from:

```
MasterDictionary/
 ├── positive-words.txt
 └── negative-words.txt
```

Stopwords are removed from these lists to improve sentiment accuracy.

### 4. HTML Article Extraction

The script extracts:

* Article **Title**
* **Main Content**

From saved HTML files located in:

```
Saved_HTML/
```

The parser searches multiple possible containers such as:

* `td-post-content`
* `article`
* `post-body`
* `content`

This ensures robust extraction even if page structures vary.

### 5. Text Cleaning

The article text is processed by:

* Converting to lowercase
* Removing punctuation
* Tokenizing words using NLTK
* Removing stopwords

### 6. Sentiment Analysis

Using the **Master Dictionary**, the program calculates:

* Positive Score
* Negative Score
* Polarity Score
* Subjectivity Score

### 7. Readability & Complexity Metrics

The following readability metrics are computed:

* Average Sentence Length
* Percentage of Complex Words
* Fog Index
* Syllables Per Word
* Complex Word Count
* Word Count
* Average Word Length
* Personal Pronouns

### 8. Output Generation

The results are saved in:

```
Output.xlsx
```

Matching the format specified in **Output Data Structure.xlsx**.

Any missing or unreadable HTML files are logged in:

```
missing_files.txt
```

---

# Project Structure

```
Blackcoffer_Assignment
│
├── Input.xlsx
├── Output Data Structure.xlsx
├── Output.xlsx
│
├── Saved_HTML
│   ├── 123.html
│   ├── 124.html
│   └── ...
│
├── StopWords
│   ├── StopWords_Auditor.txt
│   ├── StopWords_Currencies.txt
│   └── ...
│
├── MasterDictionary
│   ├── positive-words.txt
│   └── negative-words.txt
│
├── missing_files.txt
├── analysis.py
└── README.md
```

---

# Technologies Used

* Python
* Pandas
* BeautifulSoup
* NLTK
* Regular Expressions

---

# Python Libraries Required

Install dependencies using:

```bash
pip install pandas beautifulsoup4 nltk openpyxl
```

NLTK datasets are downloaded automatically by the script:

```
punkt
stopwords
```

---

# How to Run the Project

1. Clone the repository

```
git clone https://github.com/your-username/blackcoffer-nlp-analysis.git
```

2. Navigate to the project folder

```
cd blackcoffer-nlp-analysis
```

3. Run the script

```
python analysis.py
```

4. Output will be generated as:

```
Output.xlsx
```


# Notes

* The script processes **locally saved HTML files** instead of live scraping.
* This approach ensures stability in case of **SSL issues or website restrictions**.

---

