# 📘 SmartGate - 仕様書

## 🏷️ プロジェクト名

SmartGate

## 🎯 概要

SmartGate は、SwitchBot API を活用して自宅の鍵を安全に制御するための Web アプリケーションです。アクセス者はブラウザ上で出題される質問に正解すると、鍵を開けるために必要な「6 桁の数字コード」を取得できます。コードには有効期限が設定され、期限切れコードは自動で無効化されます。

このアプリは **管理者が発行した「パスコード（4 ～ 6 桁の数字）」を知っている人だけがアクセス可能** です。パスコードを入力しないとトップページに進めません。

## 🔐 主な機能

### 🔸 アクセス制限（パスコード）

- アプリにアクセスするには、最初に「パスコード」の入力が必要。
- パスコードは 4〜6 桁の数字で、管理者から共有された URL と一緒に提供される。
- パスコードが正しければトップページ（ログイン画面）へ遷移。
- 一度通過すれば、セッションが有効な間は再入力不要。

### 🔸 ログイン機能

- 誰でもログインできるが、**事前にパスコードを通過している必要あり**。
- 一般的な ID/PW 認証方式を採用。
- 未ログイン時は質問ページ・ダッシュボードにアクセスできない。

### 🔸 鍵制御

- SwitchBot API を用いて自宅のスマートロックを制御。
- 開錠処理は直接ではなく、6 桁の開錠コードを表示する方式。

### 🔸 質問回答と認証フロー

- **ログイン必須**：ログインしていないと質問に答えることはできない。
- 質問は 3 問、内容は本人に関するもの。
- 名前と有効時間（1〜24 時間）を選択・入力必須。
- 全問正解で 6 桁のランダムコードを生成。
- 正解後、SwitchBot API 経由でコードをデバイスに登録。

### 🔸 回答制限

- 回答は最大 3 回まで。
- 3 回間違えるとアクセス制限（時間制限 or ロック）をかける。

### 🔸 開錠コード

- 成功時に発行される 6 桁の数字。
- 有効期限を 1〜24 時間（1 時間単位）で選択可能。
- バックエンドで有効期限切れのコードを定期的に削除。

### 🔸 通知機能

- LINE Messaging API を活用して、開錠コード発行時に LINE 通知を送信。
- 通知内容には「発行者名」「発行時間」「有効時間」などを含む予定。

### 🔸 ダッシュボード（管理者向け）

- 開錠履歴の確認
- 有効なコード一覧と有効期限の確認
- 通知 ON/OFF 切替
- ログアウト

## 🖼️ 想定画面一覧

1. パスコード入力画面（最初に表示される）
2. ログイン画面
3. 質問回答フォーム（名前、時間選択を含む）
4. 成功時のコード表示画面
5. アクセス制限エラーページ
6. 管理者ダッシュボード

## 📚 使用予定技術

- フロントエンド：HTML/CSS + JavaScript（必要に応じて）
- バックエンド：Python（Flask）
- API 連携：SwitchBot API / LINE Messaging API
- データベース：SQLite または PostgreSQL（Heroku 利用の場合）
- 認証：Flask-Login
- アクセス制限：Flask セッション＋パスコード管理ロジック

## 🗂️ フォルダ構成

```
SmartGate/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── gate.py
│   │   ├── question.py
│   │   ├── admin.py
│   │   └── passcode.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── access_log.py
│   │   └── code.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── passcode.html
│   │   ├── login.html
│   │   ├── question.html
│   │   ├── code.html
│   │   ├── error.html
│   │   └── dashboard.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── main.js
│   └── utils/
│       ├── __init__.py
│       ├── switchbot.py
│       ├── line_notify.py
│       └── helpers.py
├── migrations/                 # DBマイグレーション
├── venv/                       # Python仮想環境（Git管理対象外）
├── .env                        # 環境変数ファイル
├── config.py                   # 設定ファイル
├── requirements.txt            # 依存ライブラリ
├── run.py                      # アプリ起動エントリポイント
├── README.md                   # プロジェクト概要
└── spec.md                     # 本仕様書ファイル
```

## 🔸 参照リンク

- [SwitchBotAPI](https://github.com/OpenWonderLabs/SwitchBotAPI)
