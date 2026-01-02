#!/usr/bin/env python3
"""
Clean up the Simply Static WordPress export for static hosting.
- Removes comment forms (won't work on static sites)
- Adds archive notice
- Disables search form
"""

import re
import os
from pathlib import Path

EXPORT_DIR = Path("/mnt/c/code/home/firedk/simply-static-1-1767369415")

ARCHIVE_NOTICE = '''<div class="archive-notice" style="background: #f5f5f5; border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 4px;">
	<p style="margin: 0; color: #666;"><em>This is an archived version of the site. Comments are no longer accepted.</em></p>
</div>'''

def process_html_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Replace comment form with archive notice
    # Pattern matches the respond div containing the comment form
    comment_form_pattern = r'<div id="respond" class="comment-respond">.*?</div><!-- #respond -->'
    content = re.sub(comment_form_pattern, ARCHIVE_NOTICE, content, flags=re.DOTALL)

    # Disable search form by replacing it with a notice
    search_form_pattern = r'<form role="search" method="get" class="search-form" action="/">\s*<label>.*?</form>'
    search_replacement = '''<div class="search-disabled" style="color: #999; font-style: italic;">
	<p>Search is not available in this archived version.</p>
</div>'''
    content = re.sub(search_form_pattern, search_replacement, content, flags=re.DOTALL)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    modified_count = 0

    for html_file in EXPORT_DIR.rglob("*.html"):
        if process_html_file(html_file):
            modified_count += 1
            print(f"Modified: {html_file.relative_to(EXPORT_DIR)}")

    print(f"\nTotal files modified: {modified_count}")

if __name__ == "__main__":
    main()
