"""Publish an exact, validated copy of the production sitemap without dependencies."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

SOURCE_ORIGIN = 'https://summoners-war-index.pages.dev'
SOURCE_URL = SOURCE_ORIGIN + '/sitemap.xml'
NAMESPACE = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
MAX_BYTES = 50 * 1024 * 1024


def validate_sitemap(body):
    if len(body) > MAX_BYTES:
        raise ValueError('Sitemap exceeds the uncompressed size limit')
    try:
        text = body.decode('utf-8', errors='strict')
        if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
            raise ValueError('Unexpected DTD or entity declaration')
        root = ET.fromstring(text)
    except (UnicodeDecodeError, ET.ParseError) as error:
        raise ValueError('Invalid UTF-8 XML') from error
    if root.tag != NAMESPACE + 'urlset':
        raise ValueError('Expected a sitemap urlset')
    urls = []
    for item in root:
        locations = item.findall(NAMESPACE + 'loc')
        if item.tag != NAMESPACE + 'url' or len(locations) != 1:
            raise ValueError('Expected exactly one loc per url')
        value = locations[0].text or ''
        url = urlsplit(value)
        if (url.scheme != 'https' or url.netloc != urlsplit(SOURCE_ORIGIN).netloc
                or url.query or url.fragment or not url.path.endswith('/')
                or value != value.strip()):
            raise ValueError('Noncanonical production URL: ' + value)
        urls.append(value)
    if not 0 < len(urls) <= 50000 or len(urls) != len(set(urls)):
        raise ValueError('Empty, duplicate, or excessive sitemap URLs')
    return len(urls)


def main():
    request = Request(SOURCE_URL, headers={'User-Agent': 'SummonersWarSitemapMirror/1.0'})
    with urlopen(request, timeout=60) as response:
        if response.status != 200 or response.url != SOURCE_URL:
            raise ValueError('Unexpected source response or redirect')
        if response.headers.get_content_type() not in ('application/xml', 'text/xml'):
            raise ValueError('Source must serve XML')
        body = response.read(MAX_BYTES + 1)
    count = validate_sitemap(body)
    destination = Path('_site')
    destination.mkdir(exist_ok=True)
    (destination / 'sitemap.xml').write_bytes(body)
    status = {'source': SOURCE_URL, 'urlCount': count,
              'sha256': hashlib.sha256(body).hexdigest(),
              'syncedAt': datetime.now(timezone.utc).isoformat()}
    (destination / 'status.json').write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (destination / 'index.html').write_text('''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google-site-verification" content="sQ2nZTBNf51TMljuTnOk22pY-iFjuXt9I4UvAtPthF4" />
<meta name="robots" content="noindex"><title>サマナーズウォーモンスター図鑑 サイトマップ</title></head>
<body><h1>サマナーズウォーモンスター図鑑 サイトマップ</h1>
<p>本サイトのXMLを検証し、同じ内容を別ホストから配信しています。</p>
<ul><li><a href="sitemap.xml">XMLサイトマップ</a></li><li><a href="status.json">同期状態</a></li>
<li><a href="https://summoners-war-index.pages.dev/ja/">図鑑へ</a></li></ul></body></html>
''', encoding='utf-8')
    print(json.dumps(status, ensure_ascii=False))


if __name__ == '__main__':
    main()
