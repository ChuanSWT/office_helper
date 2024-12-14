import os
import yt_dlp
from config import Config
from threading import Thread
from datetime import datetime


class VideoDownload:
    def __init__(self, download_folder=Config.video_download_object_path):
        self.download_folder = download_folder
        os.makedirs(download_folder, exist_ok=True)

    def download_video(self, url):
        """
        使用 yt-dlp 下载视频
        :param url: 视频的 URL 链接
        """
        # 获取当前时间戳
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        ydl_opts = {
            'outtmpl': os.path.join(self.download_folder, '%(title)s_' + timestamp + '.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def start_download(self, url):
        """
        启动下载线程，异步下载视频
        :param url: 视频链接
        """
        download_thread = Thread(target=self.download_video, args=(url,))
        download_thread.start()
