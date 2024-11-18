import undetected_chromedriver as uc
from util.get_chrome_version import get_chrome_version

def get_chrome(type):
    chrome_options = uc.ChromeOptions()
    #chrome_options.add_argument("--window-position=-32000,-32000")
    return uc.Chrome(options=chrome_options, version_main=get_chrome_version())