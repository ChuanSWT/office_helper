from config import Config
import os
from flask import Flask, request, render_template, flash
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from printer import Printer
from videoDownload import VideoDownload


app = Flask(__name__)
socketio = SocketIO(app)
@app.route('/')
def index():
    return render_template('welcome.html')


@app.route('/printer', methods=['GET', 'POST'])
def printer():
    return render_template('app/printer.html')


@app.route('/printer/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('没有文件被上传', 'danger')
        return render_template('app/printer.html')

    file = request.files['file']
    print_mode = request.form.get('print_mode')  # 获取用户选择的打印模式

    if file.filename == '':
        flash('未选择文件', 'danger')
        return render_template('app/printer.html')

    if file and Printer.allowed_file(file.filename):
        # 使用 secure_filename 保证文件名的安全性
        filename = secure_filename(file.filename)
        file_path = os.path.join(Printer.UPLOAD_FOLDER, filename)
        file.save(file_path)

        # 调用打印功能
        Printer.print_pdf_with_subprocess(file_path, print_mode)
        return render_template('app/printer.html')
    else:
        flash('仅支持 PDF 文件', 'danger')
        return render_template('app/printer.html')


@app.route('/videoDownload', methods=['GET','POST'])
def videoDownload():
    return render_template('app/videoDownload.html')


@app.route('/videoDownload/upload', methods=['POST'])
def videoDownloadUpload():
    url = request.form['url']
    if not url:
        return render_template('app/videoDownload.html', message="没有提供链接，请重新输入!")

    # 创建 VideoDownloader 实例并启动下载
    downloader = VideoDownload()
    downloader.start_download(url)

    return render_template('app/videoDownload.html', message="已提交下载任务！请查看共享文件夹")


if __name__ == '__main__':
    app.run(host=Config.my_ip, port=Config.my_port, debug=True)
