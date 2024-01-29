import re


def not_empty_comment(content: str) -> bool:
    # Регулярний вираз для пошуку всіх блоків <blockquote>...</blockquote>
    pattern = r"<blockquote>(.*?)</blockquote>"

    # Видаляємо весь вміст до останнього блоку <blockquote>
    index = content.rfind("<blockquote>")
    cleaned_text = content[index:]

    # Видаляємо знайдені блоки <blockquote>...</blockquote>
    cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.DOTALL)

    # Виводимо лише вміст після останнього блоку </blockquote>
    result = cleaned_text.split("</blockquote>")[-1].strip()
    if result == "<p>&nbsp;</p>":
        return False
    else:
        return True
