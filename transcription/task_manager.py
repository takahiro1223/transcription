import threading
from db import get_db_connection
from .speech_to_text import transcription_work

# イベントオブジェクトの作成
signal = threading.Event()
lock = threading.Lock()

def work(id):
    # ロックを使用して並列処理を防ぐ
    if signal.is_set():
        # 文字起こし実行中ならstatusを1に更新して終了
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE results SET status = 1 WHERE id = ?', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return
    else:
        while True:
            with lock:
                try:
                    # イベントをセット
                    signal.set()
                    # DBを更新＆filepath取得
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE results SET status = 2 WHERE id = ?', (id,))
                    DB_file_path = cursor.execute('SELECT file_path FROM results WHERE id = ?', (id,)).fetchone()
                    file_path = DB_file_path[0]
                    conn.commit()
                    cursor.close()
                    conn.close()
                    # 文字起こし実行
                    zip_file_path = transcription_work(file_path)
                    # zip_file_pathをDBに保管
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE results SET zip_file_path = ?, status = 3 WHERE id = ?',(zip_file_path, id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                except Exception as e:
                    # エラーが発生した場合、ステータスをエラー状態に更新
                    print(e)
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('UPDATE results SET status = 4 WHERE id = ?', (id,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                finally:
                    # イベントをクリア（文字起こし中のエラー対策のためこの位置）
                    signal.clear()
                    # 次のタスクを探す
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    next_task = cursor.execute('SELECT id FROM results WHERE status = 1 ORDER BY created_at LIMIT 1').fetchone()
                    cursor.close()
                    conn.close()
                    if next_task:
                        # タプル表記を修正
                        id = next_task[0]
                        continue
                    else:
                        break

def task_control(id):
    # スレッドの作成と開始
    thread = threading.Thread(target=work, args=(id,))
    thread.start()