from flask import Flask
from app import create_app

# Flaskアプリのファクトリ関数を使ってアプリを作成
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
