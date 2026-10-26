import unittest
from build import validate_sitemap


def sitemap(*urls):
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + ''.join('<url><loc>' + url + '</loc></url>' for url in urls)
            + '</urlset>').encode('utf-8')


class SitemapValidationTests(unittest.TestCase):
    def test_accepts_production_pages(self):
        self.assertEqual(validate_sitemap(sitemap(
            'https://summoners-war-index.pages.dev/ja/',
            'https://summoners-war-index.pages.dev/en/monster/sw-10131/')), 2)

    def test_rejects_invalid_or_unrelated_content(self):
        bodies = [b'<html>Authentication required</html>', sitemap(),
                  sitemap('http://summoners-war-index.pages.dev/ja/'),
                  sitemap('https://other.example/ja/'),
                  sitemap('https://summoners-war-index.pages.dev/ja/?q=1'),
                  sitemap('https://summoners-war-index.pages.dev/ja/',
                          'https://summoners-war-index.pages.dev/ja/')]
        for body in bodies:
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    validate_sitemap(body)


if __name__ == '__main__':
    unittest.main()
