import os
import yt_dlp
import re

def download_video(url, output_folder="downloads", format_type="mp3"):
    resolution = "1080"  # デフォルト解像度
    
    if format_type == "mp4":
        resolution_options = ["360", "720", "1080"]
        resolution = input(f"解像度を選択してください {resolution_options}: ").strip()
        
        if resolution not in resolution_options:
            print("無効な解像度が選択されました。デフォルトの1080を使用します。")
            resolution = "1080"

    ydl_opts = {
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'format': 'bestaudio/best' if format_type == "mp3" else f"bestvideo[height<={resolution}]+bestaudio/best/best",
        'merge_output_format': 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }
        ] if format_type == "mp3" else [
            {
                'key': 'FFmpegVideoConvertor',
                'preferredformat': 'mp4'
            },
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac'
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"\nダウンロード完了: {url}")

if __name__ == "__main__":
    youtube_input = input("YouTubeのURLを入力（複数可）: ")
    format_type = input("ダウンロード形式（mp4/mp3）: ").strip().lower()
    
    url_list = re.findall(r'https?://[\w./?=+-]+', youtube_input)
    
    for url in url_list:
        download_video(url, format_type=format_type)
    
    print("\nすべてのダウンロードが完了しました。")
