#!/usr/bin/python3

"""
This script parses World English Bible HTML files with Deuterocanon
and generates TAGL files for each book using metadata from a TSV index.

Generated using a specialized GPT named "Systems Refactor Engineer"
based on OpenAI GPT-4-turbo, customized in May 2025 for TAGL parsing,
C/C++ systems refactoring, and semantic web architecture.
"""

import os
import sys
import csv
from bs4 import BeautifulSoup

# Constants
BIBLES_DIR = "bibles"
TAGL_DIR = "tagl"


def parse_web_html_to_tagl(target):
    input_dir = os.path.join(BIBLES_DIR, target)
    index_path = os.path.join(BIBLES_DIR, f"{target}.tsv")
    output_dir = os.path.join(TAGL_DIR, target)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(index_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) < 5:
                continue

            order, title, _, index_file, *chapter_files = row
            book_tag = title.replace(" ", "_")
            output_filename = f"{order}-{book_tag}.tagl"
            tagl_lines = [f">> /bible/{book_tag} ;"]

            for i, chapter_file in enumerate(chapter_files):
                chapter_path = os.path.join(input_dir, chapter_file)
                chapter_num = str(i + 1)
                tagl_lines.append(f">> /bible/{book_tag}/{chapter_num} ;")

                with open(chapter_path, 'r', encoding='utf-8') as cf:
                    soup = BeautifulSoup(cf, 'html.parser')

                for p in soup.find_all('p'):
                    for verse in p.find_all('span', class_='verse'):
                        num = verse.get('id') or verse.get('name') or 'UNK'
                        text = verse.text.strip().replace('"', '\"')
                        path = f"/bible/{book_tag}/{chapter_num}/{num}"
                        tagl_lines.append(f">> {path} \"{text}\" ;")

            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write("\n".join(tagl_lines))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: bin/parse_html_to_tagl.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    parse_web_html_to_tagl(target)

