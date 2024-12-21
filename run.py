from app.app import app
from db import create_db

# データベースの初期化
create_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)