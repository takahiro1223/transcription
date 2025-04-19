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

### 画面



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
