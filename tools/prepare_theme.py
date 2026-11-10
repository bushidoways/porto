from pathlib import Path
import os
root = Path(__file__).resolve().parents[1]
pages = [root / 'index.html', *sorted((root / 'journal').rglob('*.html'))]
for page in pages:
    text = page.read_text(encoding='utf-8')
    if 'data-shared-theme' in text:
        continue
    css = os.path.relpath(root / 'assets/site-theme.css', page.parent).replace(os.sep, '/')
    js = os.path.relpath(root / 'assets/site-theme.js', page.parent).replace(os.sep, '/')
    if '</head>' not in text:
        raise ValueError(f'Missing head: {page}')
    text = text.replace('</head>', f'<link data-shared-theme rel="stylesheet" href="{css}"><script src="{js}"></script></head>', 1)
    page.write_text(text, encoding='utf-8')
print(f'Prepared shared theme on {len(pages)} HTML pages')
