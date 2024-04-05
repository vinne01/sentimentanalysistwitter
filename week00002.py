{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "e68c3d85-d7ed-4106-a92c-fc4fb2284773",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package punkt to\n",
      "[nltk_data]     C:\\Users\\vinne\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Unzipping tokenizers\\punkt.zip.\n",
      "[nltk_data] Downloading package wordnet to\n",
      "[nltk_data]     C:\\Users\\vinne\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data] Downloading package stopwords to\n",
      "[nltk_data]     C:\\Users\\vinne\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Unzipping corpora\\stopwords.zip.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Original text: The quick brown fox jumps over the lazy dogs.\n",
      "Stemmed tokens: ['quick', 'brown', 'fox', 'jump', 'lazi', 'dog']\n",
      "Lemmatized tokens: ['quick', 'brown', 'fox', 'jump', 'lazy', 'dog']\n",
      "\n",
      "Original text: Python is an amazing programming language for natural language processing.\n",
      "Stemmed tokens: ['python', 'amaz', 'program', 'languag', 'natur', 'languag', 'process']\n",
      "Lemmatized tokens: ['python', 'amazing', 'programming', 'language', 'natural', 'language', 'processing']\n",
      "\n",
      "Original text: NLTK makes it easy to perform various NLP tasks such as tokenization, stemming, and lemmatization.\n",
      "Stemmed tokens: ['nltk', 'make', 'easi', 'perform', 'variou', 'nlp', 'task', 'token', 'stem', 'lemmat']\n",
      "Lemmatized tokens: ['nltk', 'make', 'easy', 'perform', 'various', 'nlp', 'task', 'tokenization', 'stemming', 'lemmatization']\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import nltk\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.tokenize import RegexpTokenizer\n",
    "from nltk.stem import PorterStemmer, WordNetLemmatizer\n",
    "\n",
    "# Download NLTK resources if not already downloaded\n",
    "nltk.download('punkt')\n",
    "nltk.download('wordnet')\n",
    "nltk.download('stopwords')\n",
    "\n",
    "# Sample text dataset\n",
    "text_dataset = [\n",
    "    \"The quick brown fox jumps over the lazy dogs.\",\n",
    "    \"Python is an amazing programming language for natural language processing.\",\n",
    "    \"NLTK makes it easy to perform various NLP tasks such as tokenization, stemming, and lemmatization.\"\n",
    "]\n",
    "\n",
    "# Initialize tokenizer\n",
    "tokenizer = RegexpTokenizer(r'\\w+')\n",
    "\n",
    "# Initialize stemmer\n",
    "stemmer = PorterStemmer()\n",
    "\n",
    "# Initialize lemmatizer\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "\n",
    "# Preprocess function\n",
    "def preprocess_text(text):\n",
    "    # Tokenization\n",
    "    tokens = tokenizer.tokenize(text.lower())  # Convert to lowercase and tokenize\n",
    "    \n",
    "    # Remove stopwords\n",
    "    tokens = [token for token in tokens if token not in stopwords.words('english')]\n",
    "    \n",
    "    # Stemming\n",
    "    stemmed_tokens = [stemmer.stem(token) for token in tokens]\n",
    "    \n",
    "    # Lemmatization\n",
    "    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]\n",
    "    \n",
    "    return stemmed_tokens, lemmatized_tokens\n",
    "\n",
    "# Preprocess each document in the dataset\n",
    "for doc in text_dataset:\n",
    "    stemmed_tokens, lemmatized_tokens = preprocess_text(doc)\n",
    "    print(\"Original text:\", doc)\n",
    "    print(\"Stemmed tokens:\", stemmed_tokens)\n",
    "    print(\"Lemmatized tokens:\", lemmatized_tokens)\n",
    "    print()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e3f633a5-6802-4bad-b9bb-f277b9fc95d4",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
