import os
from bs4 import BeautifulSoup
import json

DOCS_PATH = "/Users/aryankix101/Desktop/EduTok/manim-docs/docs.manim.community/en/stable"

def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")  

    main_content_div = soup.find("div", class_="document")
    if not main_content_div:
        main_content_div = soup

    sidebars = main_content_div.find_all("div", class_="sphinxsidebar")
    for sb in sidebars:
        sb.decompose()

    nav_bars = main_content_div.find_all("nav")
    for nb in nav_bars:
        nb.decompose()

    text_content = main_content_div.get_text(separator="\n")
    clean_text = "\n".join(line.strip() for line in text_content.splitlines() if line.strip())


    
    code_blocks = []
    for code_block in main_content_div.find_all("div", class_="highlight"):
        code_text = code_block.get_text(separator="\n")
        code_blocks.append(code_text)

    return clean_text, code_blocks

def main():
    all_docs = []

    # Traverse all .html files
    for root, dirs, files in os.walk(DOCS_PATH):
        for file in files:
            if file.endswith(".html"):
                html_file_path = os.path.join(root, file)
                text_content, code_blocks = parse_html_file(html_file_path)

                all_docs.append({
                    "file_path": html_file_path,
                    "text": text_content,
                    "code_blocks": code_blocks
                })

    print(f"Parsed {len(all_docs)} documents.")

    with open("manim_docs.json", "w", encoding="utf-8") as out_f:
        json.dump(all_docs, out_f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
