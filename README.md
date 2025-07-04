# 🔐 SmartGate

> ⚠️ **このプロジェクトは現在作成途中です。仕様や実装は今後変更される可能性があります。**

## 📘 概要

**SmartGate** は、SwitchBot API を活用して自宅のスマートロックを制御するための Web アプリケーションです。  
アクセス制限や本人認証クイズを通して、一定条件を満たしたユーザーに一時的な「開錠コード」を発行します。

本アプリは以下のような特徴を持ちます：

- パスコードによる初期アクセス制限
- ログイン後、本人に関する質問による認証プロセス
- 条件を満たすと 6 桁の開錠コードを表示
- SwitchBot API との連携によるスマートロック操作
- LINE 通知機能
- 管理者向けダッシュボード

## 💡 主な機能（予定）

- パスコード入力によるアクセス制限
- Flask-Login を用いたログイン機能
- 本人確認用の質問回答システム（最大3回まで）
- 開錠コードの有効期限設定と自動無効化
- LINE API による通知送信
- 管理者向けダッシュボード

## 🛠️ 使用技術

- **フロントエンド**：HTML / CSS / JavaScript
- **バックエンド**：Python (Flask)
- **データベース**：SQLite or PostgreSQL
- **API**：SwitchBot API / LINE Messaging API
- **認証**：Flask-Login

## 📁 フォルダ構成（予定）

```
SmartGate/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── models/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── utils/
├── migrations/                 # DBマイグレーション
├── venv/                       # Python仮想環境（Git管理対象外）
├── .env                        # 環境変数ファイル
├── config.py                   # 設定ファイル
├── requirements.txt            # 依存ライブラリ
├── run.py                      # アプリ起動エントリポイント
├── README.md                   # プロジェクト概要
└── spec.md                     # 本仕様書ファイル
```

## 🗓️ 現在の進捗状況

- ✅ 仕様書作成
- ✅ アクセス制限・ログイン・ログアウト機能 完成
- ✅ 新規ユーザー作成・パスコード生成画面 完成
- 🔄 画面設計進行中（残りの画面を順次実装予定）
- ⏳ DB設計・API設計 着手予定
- ⏳ 実装フェーズ 継続中

> 詳細は [`spec.md`](./spec.md) を参照してください。

## 📌 注意事項

- 現時点ではローカル環境での動作確認用。
- `.env` ファイルに環境変数（パスコードや API キーなど）を適切に設定する必要があります。

## 📎 リンク

- [SwitchBotAPI ドキュメント](https://github.com/OpenWonderLabs/SwitchBotAPI)

---

> この `README.md` はプロジェクト進行に応じて随時更新予定です。
