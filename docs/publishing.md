# 公開・Google設定・移行手順

## 今回の移行

リポジトリ名を `video-publishing-site` から `personal-apps-site` へ変更します。ローカルの同じGitリポジトリも `C:\dev\repos\personal-apps-site` に改名し、originを `git@github.com:taketake-dev/personal-apps-site.git` に更新します。

`index.html`、`privacy.html`、`terms.html` とアプリ別ページのパスは維持しますが、PagesのベースURLは `https://taketake-dev.github.io/personal-apps-site/` へ変わります。動画ツールの従来のデータ説明は引き続きルートのポリシーページにも全文掲載します。

**旧Pages URLは自動転送されません。既存YouTube OAuthの登録URLも更新が必要です。** GitHubのリポジトリURL・Git操作の転送とPagesのURLは別です（[GitHub公式の改名説明](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository)）。旧Pagesが停止する可能性があるため、新サイトの公開確認とGoogle側のURL更新を連続して進めてください。旧名の別リポジトリによる転送サイトは作成しません。

Job RunnerのDrive転送有効化、OAuth認証、実転送、Discord通知、ジョブ実行、シャットダウンは、このサイト変更の範囲外です。

## 公開前のレビュー

1. `git diff` で内容を確認する。特にJob Runnerの未認証・無効状態、スコープ未確定、Museでの処理、保存・削除方法を確認する。
2. READMEのローカル確認コマンドで `_site/` を作る。`public-files.json` と `_site/` のファイル一覧が一致することを確認する。公開対象は現在HTML 7ページとCSS 1ファイルのみ。
3. PC・スマートフォン幅で、共通トップ、両アプリ紹介、ポリシー・規約を表示する。各ページからポリシーへ移動できることを確認する。Pagesのパス階層も確認する場合は、`_site` を `work/preview/personal-apps-site/` にコピーして `work/preview/` を配信する。
4. 公開ページに認証情報、内部ログ、実ユーザーのデータ、未置換テンプレートがないことを確認する。
5. **ユーザーによる変更内容・公開対象の確認と承認後**、コミットをmainへpushする。main pushとWorkflowの手動実行は公開操作である。
6. Pagesの完了後、下記の新URLが認証なしで表示できること、リンク・CSSが読み込めることを確認する。リポジトリのWebサイト欄も新URLに合わせる。問題時は直前の公開コミットへ戻す修正をレビューして公開する。ただしコードを戻すだけではリポジトリ名・旧Pages URLは戻らない。
7. 新URLの表示確認後、別途承認されたGoogle設定作業として、既存YouTubeのホームページ・プライバシー・規約URLを更新する。Job Runnerの登録も下記URLを使う。OAuthクライアント・トークンの再作成や共用化はこの改名には不要で、変更しない。

## 公開後に登録する予定URL

| アプリ／項目 | URL |
| --- | --- |
| 共通トップ | https://taketake-dev.github.io/personal-apps-site/ |
| 共通プライバシー（既存YouTubeの移行先） | https://taketake-dev.github.io/personal-apps-site/privacy.html |
| 共通利用規約（既存YouTubeの移行先） | https://taketake-dev.github.io/personal-apps-site/terms.html |
| 動画ツール・ホームページ（個別ページを使う場合） | https://taketake-dev.github.io/personal-apps-site/apps/video-publishing/ |
| 動画ツール・個別ポリシー（個別ページを使う場合） | https://taketake-dev.github.io/personal-apps-site/apps/video-publishing/privacy.html |
| Job Runner・ホームページ | https://taketake-dev.github.io/personal-apps-site/apps/job-runner/ |
| Job Runner・プライバシーポリシー | https://taketake-dev.github.io/personal-apps-site/apps/job-runner/privacy.html |
| Job Runner・利用規約 | https://taketake-dev.github.io/personal-apps-site/terms.html |

Job Runnerには、用途が明確な個別ホームページと、共通原則へのリンクを含む個別ポリシーを登録する想定です。未公開の段階でGoogleへ登録したり、既存YouTubeクライアントのURLを一括変更したりしません。

### 既存YouTube登録の移行対応表

| 項目 | 旧URL | 新URL |
| --- | --- | --- |
| ホームページ | https://taketake-dev.github.io/video-publishing-site/ | https://taketake-dev.github.io/personal-apps-site/ |
| プライバシーポリシー | https://taketake-dev.github.io/video-publishing-site/privacy.html | https://taketake-dev.github.io/personal-apps-site/privacy.html |
| 利用規約 | https://taketake-dev.github.io/video-publishing-site/terms.html | https://taketake-dev.github.io/personal-apps-site/terms.html |

ホスト名 `taketake-dev.github.io` は変わりません。Authorized domainsはパスの改名だけで新しいドメインになるものではありませんが、現在のConsoleの要件と登録内容を確認してください。紹介サイトの改名に合わせてOAuthのリダイレクトURIを変更する必要はありません。

## Google Cloud Consoleで確認する情報

- 対象：専用プロジェクト `job-runner-logs`。Drive API・デスクトップ用OAuthクライアントは準備済み。既存YouTubeのプロジェクト／クライアントとは分離する。
- Branding：アプリ名（Job Runnerと整合する表示名）、ユーザーサポートメール、開発者連絡先、上記ホームページ・ポリシー・規約。サポートメールの候補はサイト記載の `utsuroi.media@gmail.com` だが、Consoleで選択・利用できるアカウントを本人が確認する。
- Authorized domains：登録URLに対応するドメインを、現在のConsoleの入力要件に従って確認する。URLの `/personal-apps-site/` はドメインではない。`github.io` 全体の所有を主張しない。
- Audience：本人利用の対象アカウント、現在の「テスト中」状態、公開切替の前提を確認する。
- Data Access：認証フローで実際に要求するスコープと整合させる。現設定はスコープ未明示なので「最新ログだけの権限」と記入しない。認証前にrclone設定と最小権限の実現方法を別作業で確定する。
- Clients：デスクトップ用クライアントを使う。サイト用URLはOAuthのリダイレクトURIではない。認証値・トークンを本リポジトリ、チャット、スクリーンショットへ載せない。

## 審査免除と公開状態は別に確認する

2026-11-07確認。個人利用に対する審査免除は、Cloud Consoleのブランディング入力や「テスト中」からの公開切替の要件がなくなることを意味しません。[rclone公式](https://rclone.org/drive/#making-your-own-client-id)は、個人用でも公開ボタンが無効の場合にホームページ・ポリシーURL等をBrandingへ入力する手順を案内しています。

[Google公式のブランド確認手順](https://developers.google.com/identity/protocols/oauth2/production-readiness/brand-verification)は、ホームページの一般公開、アプリとの関連性、データのアクセス・利用・保存・共有の開示、関連ドメインの確認を説明しています。[OAuthポリシー適合の説明](https://developers.google.com/identity/protocols/oauth2/production-readiness/policy-compliance)では、共有ドメインの場合は独自ドメインを使える構成も推奨しています。GitHub Pagesで今回のページを用意するだけで、公開切替・ブランド審査・ドメイン確認が必ず成功するとは保証できません。所有権確認が要求された場合は、対応するSearch Consoleの確認方法や独自ドメインの要否を、実画面と公式手順で別途判断してください。

ExternalかつTestingの更新トークンは、基本プロフィールだけの例外を除き原則7日で失効するため、Driveの継続運用では公開状態も検討が必要です（[Google公式の失効条件](https://developers.google.com/identity/protocols/oauth2#expiration)）。サイト公開とOAuthアプリの公開は別の操作です。

## Job Runner連携を有効にする前の更新

別作業で、実要求スコープと同意画面を確認し、疑似ログによる転送・上書き・Museの読み取りを検証する。検証用ログでもDriveの固定ファイルを上書きするため、サイト確認のついでには実行しない。

実態が確定したら `apps/job-runner/index.html` と同ディレクトリの `privacy.html` の状態・権限・最終更新日を更新し、同じ公開前レビューを行う。ローカルログの30日とDriveファイルの管理、動画ツールのDPAPIとJob Runnerの `.env` を混同しない。
