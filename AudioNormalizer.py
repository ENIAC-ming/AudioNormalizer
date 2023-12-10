import os
import subprocess
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from tqdm import tqdm

# 定义支持的后缀名列表
support_suffix = ['.mp3', '.wav', '.aac', '.ogg', '.m4a', '.flac', '.mp4', '.avi', '.mkv', '.wmv']
support_suffix += ['.aac', '.ac3', '.aiff', '.alaw', '.amr', '.ape', '.asf', '.au', '.caf', '.dts', '.eac3', '.f4v', '.flv', '.gsm', '.mka', '.mp2', '.mpc', '.mpeg', '.mts', '.mxf', '.oga', '.opus', '.ra', '.rm', '.rmvb', '.swf', '.ts', '.vob', '.w64', '.wma', '.webm']

ffmpeg_path = ''

def show_message(title, message):
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo(title, message)
    root.destroy()

def check_ffmpeg():
    global ffmpeg_path
    try:
        subprocess.run(["./ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_path = "./ffmpeg"
        return True
    except FileNotFoundError:
        pass
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_path = "ffmpeg"
        return True
    except FileNotFoundError:
        pass
    return False

# 弹出提醒对话框
def show_ffmpeg_download_message():
    show_message("找不到FFmpeg", "找不到FFmpeg。\n请从此处下载并安装 https://ffmpeg.org")

if not check_ffmpeg():
    show_ffmpeg_download_message()
    exit()


# 选择文件夹
root = Tk()
root.withdraw()  # 不显示主窗口
folder = filedialog.askdirectory()  # 显示文件夹选择框

if not folder:
    print('未选择文件夹，正在退出...')
    exit()

# 新建子文件夹music，若存在，则清空该文件夹
music_folder = os.path.join(folder, 'music')
if not os.path.exists(music_folder):
    os.makedirs(music_folder)
else:
    for file in os.listdir(music_folder):
        os.remove(os.path.join(music_folder, file))

# 遍历folder下的所有文件
files = []
for root, dirs, filenames in os.walk(folder):
    for filename in filenames:
        if any(filename.lower().endswith(suffix) for suffix in support_suffix):
            files.append(os.path.join(root, filename))

file_now = 0
print("识别到以下含音频的文件：")
for file in files:
    print(file)

# 定义转换函数
def convert_to_mp3(file):
    base_name = os.path.basename(file)
    new_name = os.path.splitext(base_name)[0] + '.mp3'
    output_path = os.path.join(music_folder, new_name)
    command = [
        ffmpeg_path,
        '-i', file,
        '-ar', '44100',
        '-b:a', '128k',
        '-filter:a', 'loudnorm=I=-14:TP=-1.5:LRA=11',
        '-acodec','libmp3lame',
        '-y',
        output_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"处理文件{file}时出错: {result.stderr}")

# 使用线程池执行转换
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    futures = [executor.submit(convert_to_mp3, file) for file in files]
    for _ in tqdm(as_completed(futures), total=len(files), desc="正在处理"):
        pass

# 调用资源管理器打开music文件夹
os.startfile(music_folder)

# nuitka --standalone --mingw64 --show-memory --show-progress --include-data-files=ffmpeg.exe=ffmpeg.exe --plugin-enable=tk-inter --output-dir=o AudioNormalizer.py
