import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence
from faster_whisper import WhisperModel
from .generate_output import create_workspace, export_transcription_excel, apply_excel_styles

# 無音部分の除去 ★２
def remove_silence(audio):
    chunks = split_on_silence(
        audio,
        min_silence_len=500,  # 無音とみなす最小の無音長さ (ms)
        silence_thresh=audio.dBFS - 14,  # 無音とみなす閾値 (デフォルトは音声のdBFSより少し下)
        keep_silence=100  # 無音部分の一部を残す (ms)
    )
    # 再結合
    output_audio = AudioSegment.empty()
    for chunk in chunks:
        output_audio += chunk
    return output_audio

# 文字起こししやすいよう動画を編集 ★１
def audio_file_section(file_path, file_name, audio_folder_path):
    audio = AudioSegment.from_file(file_path)
    # 無音除去 ★２
    remove_silence_audio = remove_silence(audio)
    split_time = 1 * 29 * 1000
    split_audio_file = []
    # 音声ファイルを分割
    for i, start_time in enumerate(range(0, len(remove_silence_audio), split_time)):
        end_time = start_time + split_time
        split_audio = remove_silence_audio[start_time:end_time]
        audio_file_name = f"音声ファイル{i+1}.mp3"
        split_audio_file_path = os.path.join(audio_folder_path, audio_file_name)
        split_audio.export(split_audio_file_path, format="mp3")

# フォルダ内にある音声ファイルの数を取得 ★３
def get_audio_file_count(audio_folder_path):
    files = os.listdir(audio_folder_path)
    audio_files = [f for f in files if f.endswith('.mp3') and f.startswith('音声ファイル')]
    return len(audio_files)

# 文字起こし実施 ★３
def transcribe_audio(audio_folder_path):
    transcription_results = []
    # 保管されている音声ファイルの数を取得 ★３
    file_count = get_audio_file_count(audio_folder_path)
    model = WhisperModel("tiny", device="cpu", compute_type="int8", download_root=r"./app/models")
    
    ## モデルの種類 ##
    # large-v3、large-v2、large、medium、small、base、tiny
    ####
    
    # 分割した音声ファイルごとに文字起こし
    for i in range(1, file_count + 1):
        split_audio_files_name = f"音声ファイル{i}.mp3"
        split_audio_files_path = os.path.join(audio_folder_path, split_audio_files_name)
        # エラー時には次のファイルに移行する
        try:
            segments, info = model.transcribe(split_audio_files_path, beam_size=5, vad_filter=True, without_timestamps=True)
            transcription_results.append([segment.text for segment in segments])
            print(f"総ファイル：{file_count} 文字起こし済：{i}")
        except Exception as e:
            # 文字起こしにてエラー発生時、メッセージを追加
            transcription_results.append("エラーにより文字起こしができませんでした")
    return transcription_results

# メイン処理
def transcription_work(file_path):
    # パスを設定
    file_name = os.path.basename(file_path)
    current_dir = os.getcwd()
    working_folder_path = os.path.join(current_dir, 'zip_result')
    # 新しいフォルダパスを作成
    transcription_folder_path = os.path.join(working_folder_path, f"{file_name}_文字起こし結果")
    audio_folder_path = os.path.join(transcription_folder_path, f"{file_name}_音声ファイル")
    result_excel_path = os.path.join(transcription_folder_path, f"{file_name}_文字起こし.xlsx")
    # zipファイルのパスを設定
    zip_file_path = transcription_folder_path + ".zip"
    
    # 作業スペース作成
    create_workspace(transcription_folder_path, audio_folder_path, result_excel_path)
    
    # 字起こししやすいよう動画を編集 ★１
    audio_file_section(file_path, file_name, audio_folder_path)
    # 文字起こし実施 ★３
    transcription_results = transcribe_audio(audio_folder_path)
    
    # 文字起こし結果をExcelに入力
    export_transcription_excel(transcription_results, result_excel_path, audio_folder_path)
    apply_excel_styles(result_excel_path)
    
    # zip化
    shutil.make_archive(transcription_folder_path, 'zip', transcription_folder_path)
    
    return zip_file_path