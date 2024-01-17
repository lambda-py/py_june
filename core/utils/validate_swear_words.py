import os
import re


def censored_text(text: str) -> str:
    file_path = os.path.join(os.path.dirname(__file__), "badwords.txt")
    with open(file_path, "r") as file:
        badwords = set(word.strip().lower() for word in file)

    words = re.findall(r"\b\w+\b", text)
    censor_text = " ".join(
        "*****" if word.lower() in badwords else word for word in words
    )

    return censor_text


# text = "<p>First look, at her fuck ass. </p>"
# censored_text(text)
# print(censored_text(text))
