import os
import shutil
from db import get_db_connection


# 関係するファイルを削除
def delete_all_file(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    paths_tuple = cursor.execute('SELECT file_path, zip_file_path FROM results WHERE id = ?', (id,)).fetchall()
    cursor.close()
    conn.close()
    
    # タプル型をリスト型に変換
    paths = [path for row in paths_tuple for path in row]
    
    for p in paths:
        if not p:
            continue
        # ファイルが存在するのか確認
        if os.path.exists(p):            
            if p.endswith('.zip'):
                file_path, _ = os.path.splitext(p)
                os.remove(p)
                shutil.rmtree(file_path)
            else:
                os.remove(p)
        else:
            continue