# サマナーズウォーモンスター図鑑 サイトマップ

本サイトのサイトマップをGitHub Pagesから配信し、Googleによる取得経路を検証するための専用リポジトリです。

- 本サイト: https://summoners-war-index.pages.dev/
- 取得元: https://summoners-war-index.pages.dev/sitemap.xml
- 外部配信: https://noobhuman8729.github.io/summoners-war-sitemaps/sitemap.xml
- 同期結果: https://noobhuman8729.github.io/summoners-war-sitemaps/status.json

本サイトが生成したXMLを変更せずコピーします。全URLが本サイトのHTTPS正規URLか、重複がないか、UTF-8・XML形式・件数とサイズが適切かを検証してから公開します。取得・検証に失敗すると新しい公開は行わず、直前に成功した配信を維持します。

## 更新

mainへのプッシュ、Actions画面の「Run workflow」、または毎日00:37 UTC（日本時間09:37）のスケジュールで同期します。スケジュールの実行には遅延や省略があり得ます。GitHubは公開リポジトリで60日間活動がない場合にスケジュールを無効化するため、長期利用ではActions画面で有効状態を確認してください。本サイト更新直後に反映する場合は手動で実行します。

GitHub PagesのSettings → Pages → Sourceは「GitHub Actions」に設定します。公開リポジトリの標準GitHub ActionsランナーとPagesの無料枠を使用し、外部のAPIキーや有料サービスは使用しません。

## ローカル検証

```sh
python3 -m unittest test_build.py
python3 build.py
```

生成物は`_site/`です。同期時刻・件数・元XMLのSHA-256は`status.json`に記録されます。
