// 定義
let dropArea = document.getElementById('drop-area')
let fileInput = document.getElementById('fileElem')
let fileNameDisplay = document.getElementById('fileName')
let uploadButton = document.getElementById('uploadButton')
let progressBar = document.getElementById('progress-bar-inner')
let progressText = document.getElementById('progress-text')

let file

// ドラッグ時の動画再生を禁止（デフォルト機能OFF）
;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
})

// ハイライト表示
;['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false)
})
;['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false)
})

// ドロップされたファイルの処理
dropArea.addEventListener('drop', handleDrop, false)

// ファイル選択時の処理
fileInput.addEventListener('change', handleFiles, false)

// アップロードボタンのクリックイベント
uploadButton.addEventListener('click', uploadFile, false)

function preventDefaults(e) {
    e.preventDefault()
    e.stopPropagation()
}

function highlight(e) {
    dropArea.classList.add('highlight')
}

function unhighlight(e) {
    dropArea.classList.remove('highlight')
}

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files

    handleFiles({ target: {files: files } })
}

function handleFiles(e) {
    let files = e.target.files
    if (files.length > 0) {
        file = files[0]
        fileNameDisplay.textContent = `選択されたファイル：${file.name}`
        uploadButton.disabled = false
    }
}

// ファイルのアップロード処理
function uploadFile() {
    let url = '/upload'
    let formData = new FormData();
    formData.append('file', file);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);

    // 進捗イベントの処理
    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            let percentComplete = Math.round((e.loaded / e.total) * 100);
            progressBar.style.width = percentComplete + '%';
            progressText.textContent = `アップロード中 ${percentComplete}% 完了までお待ちください。`;
        }
    });

    // アップロード完了時の処理
    xhr.addEventListener('load', function() {
        if (xhr.status === 200) {
            progressBar.style.width = '0%'
            fileNameDisplay.textContent = ''
            uploadButton.disabled = true
            // アップロードが完了したら画面をリロード
            location.reload();
        } else {
            alert('アップロードに失敗しました')
        }
    });

    // アップロードの開始
    xhr.send(formData);
}