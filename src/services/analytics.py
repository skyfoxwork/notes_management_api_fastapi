import numpy as np
import pandas as pd
import nltk
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
nltk.download("punkt_tab")

STOPWORDS = set(stopwords.words("english"))


async def get_analyze_notes(notes: list):
    """
    Analyzes the notes database and returns statistics.
    """

    # Loading Note Texts into a Pandas DataFrame
    df = pd.DataFrame([{"id": note.id, "content": note.content} for note in notes])

    # Count the number of words in each note
    df["word_count"] = df["content"].apply(lambda x: len(x.split()))

    # Total number of words in all notes
    total_word_count = df["word_count"].sum()

    #Average length of note
    avg_note_length = np.mean(df["word_count"])

    # Most common words (without stop words)
    all_words = " ".join(df["content"]).lower()
    words = [word for word in word_tokenize(all_words) if word.isalnum() and word not in STOPWORDS]
    most_common_words = Counter(words).most_common(5)  # Топ-5 частых слов

    # Top 3 Long and Short Notes
    longest_notes = df.nlargest(3, "word_count")[["id", "word_count"]].to_dict(orient="records")
    shortest_notes = df.nsmallest(3, "word_count")[["id", "word_count"]].to_dict(orient="records")

    return {
        "total_word_count": total_word_count.item(),
        "average_note_length": avg_note_length.item(),
        "most_common_words": most_common_words,
        "top_3_longest_notes": longest_notes,
        "top_3_shortest_notes": shortest_notes
    }
