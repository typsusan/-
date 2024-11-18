import re
import subprocess

def get_chrome_version():
    """自动检测 Chrome 的主版本号"""
    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        ).decode('utf-8')
        version = re.search(r'(\d+)\.', output).group(1)
    except:
        output = subprocess.check_output(["google-chrome", "--version"]).decode("utf-8")
        version = re.search(r'(\d+)\.', output).group(1)
    return int(version)