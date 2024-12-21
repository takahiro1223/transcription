import os
from flask import Blueprint, render_template, request, redirect, url_for, abort, send_file, jsonify
from datetime import datetime
from db import get_db_connection
from transcription.task_manager import task_control
from transcription.delete import delete_all_file

# Blueprintを設定
my_blueprint = Blueprint('my_blueprint', __name__)

## ルート（URL）の定義
# top画面の表示
@my_blueprint.route('/')
def top():
    conn = get_db_connection()
    cursor = conn.cursor()
    # resultsの内容取得
    results = cursor.execute('SELECT * FROM results').fetchall()
    
    cursor.close()
    conn.close()
    return render_template('top.html', results=results)

@my_blueprint.route('/upload', methods=['POST'])
def upload():
    # ファイルの受け取り
    file = request.files['file']
    # ファイルをアップロード
    if file:
        title = file.filename
        file_path = os.path.join(os.getcwd(), 'upload_data', title)
        file.save(file_path)
        created_at = datetime.now()
        # ファイルパスをDBに保管
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO results (file_path, title, status, created_at) VALUES (?, ?, ?, ?)',(file_path, title, 0, created_at))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('my_blueprint.top'))

# 文字起こし実行
@my_blueprint.route('/transcription/<int:id>', methods=['POST'])
def transcription(id):
    # 文字起こし管理を実行
    task_control(id)
    return redirect(url_for('my_blueprint.top'))

# zip_fileのダウンロード
@my_blueprint.route('/download/<int:id>', methods=['GET'])
def download(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.execute('SELECT zip_file_path FROM results WHERE id = ?', (id,)).fetchone()
    results_path = result[0]
    # ZIPファイルをダウンロードとして提供
    return send_file(results_path, as_attachment=True)

# データの削除
@my_blueprint.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_all_file(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM results WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('my_blueprint.top'))