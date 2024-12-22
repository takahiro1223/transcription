import sqlite3

## データベース START ##
# データベース接続
def get_db_connection():
    conn = sqlite3.connect('transcription-data.db')
    conn.row_factory = sqlite3.Row
    return conn

# データベース作成
def create_db():
    conn = get_db_connection()
    # id:識別番号、file_path:アップロード後のファイルパス、title:動画ファイル名、status:文字起こし完了のフラグ、zip_file_path:インストール時のzipファイルパス、created_at:タスク作成日時
    conn.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            title TEXT NOT NULL,
            status INTEGER NOT NULL CHECK (status IN (0,1,2,3,4)),
            zip_file_path TEXT,
            created_at DATETIME NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

## データベース END ##
