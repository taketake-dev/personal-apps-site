"""Validate the public file list and stage only those files for Pages."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs['id'])
        self.h1 += tag == 'h1'
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag in ('script', 'iframe', 'form'):
            raise ValueError(f'Unexpected active content: {tag}')


def validate():
    names = json.loads((ROOT / 'public-files.json').read_text(encoding='utf-8'))
    if len(names) != len(set(names)):
        raise ValueError('Duplicate public files')
    documents = {}
    for name in names:
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name:
            raise ValueError(f'Unsafe path: {name}')
        if relative.suffix not in ('.html', '.css') or any(p.startswith('.') for p in relative.parts):
            raise ValueError(f'Unexpected public file: {name}')
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or ROOT not in path.resolve().parents:
            raise ValueError(f'Invalid source file: {name}')
        source = path.read_text(encoding='utf-8')
        if '\ufffd' in source or '{{APP_' in source:
            raise ValueError(f'Invalid text or unfinished template: {name}')
        if path.suffix == '.html':
            doc = Document(source)
            if doc.h1 != 1 or 'main' not in doc.ids or '<html lang="ja">' not in source:
                raise ValueError(f'Missing page structure: {name}')
            documents[path.resolve()] = doc
    allowed = {(ROOT / name).resolve() for name in names}
    links_checked = 0
    for path, doc in documents.items():
        for link in doc.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                if url.scheme not in ('https', 'mailto') or not url.path:
                    raise ValueError(f'Unexpected external link in {path.name}: {link}')
                continue
            if url.path.startswith('/'):
                raise ValueError(f'Link escapes Pages project prefix: {link}')
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target = target / 'index.html'
            if target not in allowed:
                raise ValueError(f'Link is not in public file list: {path.relative_to(ROOT)} -> {link}')
            if url.fragment and (target not in documents or unquote(url.fragment) not in documents[target].ids):
                raise ValueError(f'Broken fragment: {link}')
            links_checked += 1
    old = (ROOT / 'privacy.html').read_text(encoding='utf-8')
    specific = (ROOT / 'apps/video-publishing/privacy.html').read_text(encoding='utf-8')
    start = specific.index('    <section>')
    end = specific.index('  </main>', start)
    if specific[start:end].strip() not in old:
        raise ValueError('Legacy and app-specific video policies have diverged')
    print(f'Validated {len(documents)} HTML pages, {len(names)} public files, {links_checked} local links/fragments.')
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate without staging')
    args = parser.parse_args()
    names = validate()
    if args.check:
        return
    destination = ROOT / '_site'
    if destination.is_symlink():
        raise ValueError('Refusing a symlink staging directory')
    if destination.exists():
        # Fixed checkout-local path; never accept a caller-supplied delete path.
        if destination.resolve().parent != ROOT:
            raise ValueError('Staging directory is outside checkout')
        shutil.rmtree(destination)
    destination.mkdir()
    for name in names:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    print('Staged public files in _site/ (no publication performed).')


if __name__ == '__main__':
    main()
