import shutil
import subprocess
import os
import sys

def package_exe(script_name):
    # 确保 PyInstaller 已安装
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller 未安装，正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 打包命令
    command = [
        "pyinstaller",
        "--onefile",             # 打包成一个单独的文件
        "--name=start",          # 输出文件名为 start.exe
        script_name              # 要打包的 Python 文件
    ]

    print("正在打包中...")
    subprocess.run(command)
    print("打包完成")

if __name__ == "__main__":
    package_exe("start.py")
