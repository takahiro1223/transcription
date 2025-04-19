## プロジェクトの概要
faster-whisperを使用した文字起こしWebアプリケーションです。
アップロードされた動画はデータベースに保存され、文字起こし結果はExcel形式でダウンロードできます。

### 機能一覧

- 動画のアップロードとデータベース保存
- 動画ごとの個別文字起こし処理
- 文字起こし結果のExcel形式でのダウンロード
- 文字起こし結果と元動画データの並列表示

### 使用技術

- **言語**: Python, HTML, CSS, JavaScript
- **フレームワーク**: Flask
- **データベース**: SQLite

## 画面

### トップ画面
![Image](https://github.com/user-attachments/assets/fbf0e6d6-2ee3-4312-a0df-ad6dafce1b6d)

### 動画をアップロード
ドラッグアンドドロップやファイル選択で画面上に動画を保持できる
アップロードボタンを押すことで、「動画一覧」へのアップロードが行える

![Image](https://github.com/user-attachments/assets/a5f72161-6ea5-4ac4-a2f8-fd9857c64d18)
![Image](https://github.com/user-attachments/assets/2557fa0e-a0ca-4541-9411-bf80cf8a61bf)

### 文字起こしを実行
文字起こしボタンを押すことでステータスが文字起こしが開始（ステータスが変更される）
完了したらステータスがダウンロードボタンに変わる

![Image](https://github.com/user-attachments/assets/1e841d34-b3b4-48e7-a7d9-da55533eec5b)
![Image](https://github.com/user-attachments/assets/db46e5ed-e230-44d7-8bc5-80576244bd85)

### 文字起こし結果のダウンロード
ダウンロードボタンを押すことでzip形式のフォルダが取得できる
中身はExcelと分割された音声ファイル

![Image](https://github.com/user-attachments/assets/fc62b4b3-10f7-4b72-8eba-89cf702289f2)
![Image](https://github.com/user-attachments/assets/6ee7dc17-cc79-4e10-97f0-c02a2d0ab228)

### 文字起こし結果の削除
削除ボタンを押すことで、文字起こし結果を削除することが可能

![Image](https://github.com/user-attachments/assets/fbf0e6d6-2ee3-4312-a0df-ad6dafce1b6d)

### インストール手順

1. このリポジトリをクローンします。
```
git clone https://github.com/takahiro1223/transcription
```

2. 仮想環境を作成し、必要なパッケージをインストールします。
```
python -m venv venv
```
```
.\venv\Script\activate
```
```
pip install -r requirements.txt
```
3. アプリケーションを起動します。
```
waitress-serve --host=0.0.0.0 --port=5000 app.app:app
```
http://localhost:5000 にアクセス

### 使い方

1. トップページから動画ファイルをアップロードします。
2. アップロードされた動画はデータベースに保存されます。
3. 保存された動画の一覧から、文字起こしを行いたい動画の「文字起こし」ボタンをクリックします。
4. 文字起こしが完了すると、結果をExcel形式でダウンロードできるボタンが表示されます。
5. ダウンロードしたExcelファイルで、文字起こし結果と元動画データを並べて確認できます。

### ライセンス

このプロジェクトは[クリエイティブ・コモンズ 表示-非営利-改変禁止 4.0 国際（CC BY-NC-ND 4.0）ライセンス](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ja)の下で公開されています。

### 作者情報

名前：Takahiro Furuya  
GitHub：takahiro1223
