import re
def clean_text(text:str)->str:
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()
