# 個人開発アプリ案内・Google連携ポリシーサイト

taketake-devの個人開発アプリの共通案内サイト。静的HTML/CSSをGitHub Pagesで配信します。動画制作・投稿ツールとJob Runnerを掲載します。

- リポジトリ：<https://github.com/taketake-dev/personal-apps-site>
- 公開先：<https://taketake-dev.github.io/personal-apps-site/>
- ローカル：`C:\dev\repos\personal-apps-site`
- `index.html`：共通トップ・アプリ一覧・運営者情報
- `privacy.html`：共通原則とアプリ別ポリシーへの入口。動画ツール固有の取り扱いも全文継続掲載
- `terms.html`：共通利用条件と既存の動画ツール個別条件
- `apps/video-publishing/`：動画ツール紹介・個別プライバシーポリシー
- `apps/job-runner/`：Job Runner紹介・個別プライバシーポリシー
- `templates/app/`：次のアプリ追加用テンプレート（公開しない）
- `public-files.json`：公開ファイルの明示リスト
- `scripts/prepare_site.py`：構造・相対リンク・ページ内リンク・互換掲載の一致確認と公開用ステージング

OAuthクライアントとトークンはアプリごとに分離します。サイト内に認証機能や秘密情報を置きません。

旧名は `video-publishing-site` です。改名に伴いPagesのURLも変更されます。GitHubのリポジトリURLとは異なり、旧Pages URLの自動転送はありません。既存YouTube OAuthに登録したホームページ・ポリシー・規約URLも、新URLの公開確認後に更新してください。[移行手順](docs/publishing.md)に対応表を記載しています。HTMLの相対パスとページ構成は維持します。

## ローカル確認

リポジトリルートで実行します。Python標準ライブラリのみ使用し、Pythonはuv管理環境を使用できます。

```powershell
uv run --no-project python scripts/prepare_site.py --check
uv run --no-project python scripts/prepare_site.py
uv run --no-project python -m http.server 18743 --bind 127.0.0.1 --directory _site
```

ブラウザで <http://127.0.0.1:18743/> を開きます。終了はCtrl+C。ステージングは `_site/` のみを再生成します。公開処理は行いません。詳細は [公開・移行手順](docs/publishing.md) を参照。

## 公開の境界

**mainへのpushでPagesが自動公開されます。** ローカルコミットは公開ではありません。変更内容・公開対象を確認して承認を得るまでpush、Workflow手動実行、Google設定変更を行いません。

Workflowは `public-files.json` のHTML/CSSだけを `_site/` へコピーします。README、docs、templates、スクリプト、秘密情報は公開物に含めません。新規ページは明示リストへ追加しない限り公開されず、既存ページから未登録ページへリンクすると検証に失敗します。

## アプリを追加する

1. `templates/app/` を `apps/<slug>/` へコピーし、全ての `{{APP_...}}` を実態に合わせて置換する。
2. アプリ名・対象者・用途・導入状態、サービスとスコープ、読み取り／送信、保存先・期間、認証情報の保護、外部共有・AI処理、削除と連携解除を記載する。未確定のものは明示し、認証・稼働前に更新する。
3. 共通トップ、共通ポリシーの一覧、必要なら利用規約へ追加する。アプリ固有の保存方法を共通原則へ移さない。
4. `public-files.json` に紹介とポリシーの2ファイルを追加し、ローカル検証・表示確認を行う。
5. 別のOAuthクライアント・トークンを用意し、[公開・移行手順](docs/publishing.md) に従ってレビュー後に公開・Google設定を行う。

動画ポリシーを変更する場合は、`privacy.html` 内の継続掲載と `apps/video-publishing/privacy.html` を同時更新してください。検証スクリプトが本文の一致を確認します。

## 内容の根拠

2026-11-07にJob RunnerのREADME、`docs/workflow-hooks.md`、作者プロファイルの `drive-logs.md`、`settings.yaml`、Workflow、`upload-log.ps1`、`transfer.json`、ログ整理・Hook・Discord実装を読み取り確認しました。秘密情報ファイルやログ本体は読み取っていません。Job Runnerのコード・認証設定は変更しません。

Drive転送は未認証・無効の段階です。スコープの明示設定がないため、rcloneの既定値と実際の許可範囲の未確定を区別して掲載しています。有効化時には実際の同意画面・設定に合わせて再確認が必要です。

動画ツールの情報は従来の掲載内容を維持しています。
