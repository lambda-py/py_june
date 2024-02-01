import re


def is_empty_comment(content: str) -> bool:
    # A regular expression to find all blocks <blockquote>...</blockquote>
    pattern = r"<blockquote>(.*?)</blockquote>"

    # We delete all the content up to the last block <blockquote>
    index = content.rfind("<blockquote>")
    cleaned_text = content[index:]

    # Remove the found blocks <blockquote>...</blockquote>
    cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.DOTALL)

    # We output only the content after the last block </blockquote>
    result = cleaned_text.split("</blockquote>")[-1].strip()
    if result == "<p>&nbsp;</p>":
        return True
    else:
        return False
