#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

INPUT = "../data/a3_fieldnotes_dataset.csv"


def clean_text(t):
    t = str(t).lower()
    t = re.sub(r"[^a-z\s]", " ", t)
    return t


def theme_frequency(df):

    counts = df["section_key"].value_counts()

    plt.figure(figsize=(10,6))
    counts.head(12).plot(kind="bar")

    plt.title("Observation Themes Frequency")
    plt.ylabel("Count")
    plt.xlabel("Theme")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("../output/theme_frequency.png")
    print("Saved: output/theme_frequency.png")


def keyword_frequency(df):

    text = " ".join(df["text"].astype(str))

    text = clean_text(text)

    stopwords = set([
        "the","a","and","to","of","in","for","is","it","that","this",
        "with","on","as","at","be","are","was","they","their","from"
    ])

    words = [w for w in text.split() if w not in stopwords and len(w) > 3]

    counts = Counter(words)

    common = counts.most_common(20)

    labels = [w for w,c in common]
    values = [c for w,c in common]

    plt.figure(figsize=(10,6))
    plt.bar(labels, values)

    plt.xticks(rotation=45)
    plt.title("Most Common Keywords in Field Notes")

    plt.tight_layout()
    plt.savefig("../output/keyword_frequency.png")

    print("Saved: output/keyword_frequency.png")


def quote_samples(df):

    quotes = df[df["item_type"]=="quote"]["text"]

    print("\nExample Quotes / Insights:\n")

    for q in quotes.head(10):
        print("-", q)


def main():

    df = pd.read_csv(INPUT)

    print("Rows:", len(df))

    theme_frequency(df)

    keyword_frequency(df)

    quote_samples(df)


if __name__ == "__main__":
    main()