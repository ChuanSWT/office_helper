from config import Config
import os
import subprocess

# 配置上传文件夹和允许的文件类型
ALLOWED_EXTENSIONS = {'pdf'}
# 打印机名称
PRINTER_NAME = Config.printer_name
UPLOAD_FOLDER = Config.printer_upload_folder


class Printer:

    UPLOAD_FOLDER = Config.printer_upload_folder

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


    # 判断文件扩展名是否有效
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # 使用 subprocess 调用外部程序来打印PDF
    def print_pdf_with_subprocess(file_path, print_mode):
        # SumatraPDF 的绝对路径
        sumatra_pdf_path = Config.pdf_opener_path

        # 根据用户选择的打印模式设置不同的命令
        if print_mode == "double":
            # 双面打印的命令
            print_command = [sumatra_pdf_path, '-print-to', PRINTER_NAME,file_path,'-print-settings', "Duplex"]
        else:
            # 默认单面打印的命令
            print_command = [sumatra_pdf_path, '-print-to', PRINTER_NAME, file_path]

        try:
            subprocess.run(print_command, check=True)
            print(f"成功打印文件: {file_path}，模式: {print_mode}")
            print('文件已成功打印！', 'success')
        except subprocess.CalledProcessError as e:
            print(f"打印失败: {e}")
            print(f'打印失败: {e}', 'danger')
