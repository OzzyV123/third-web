from django import template
import re

register = template.Library()

BAD_WORDS = ["puknel","lorem","suka","kaka","popa",'kakashka']

def mask_word(word):
    if len(word) <= 1:
        return word
    return word[0] + "*" * (len(word) - 1)

@register.filter
def censor(text):
    def repl(match):
        word = match.group(0)
        lower = word.lower()

        if lower in BAD_WORDS:
            return mask_word(word)
        return word
    pattern = r"\w+"
    return re.sub(pattern, repl, text)