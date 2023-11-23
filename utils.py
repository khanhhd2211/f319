import json
import os

COOKIES = {
    'f319_isMobile': '0',
    'xf_vim|mudim-settings': '26',
    'f319_user': '826465%2Cc34bbec6f77ffc2060e6319956071c2f69b4a85b',
    'f319_session': '8d14b7c95d1cf2d7649ec65c36c2a2c4',
}

HEADERS = {
    'authority': 'f319.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://f319.com/',
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def create_folder(folder_name = "data"):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def save_json(data, f_path):
    with open(f_path, "w") as fp:
        # fp.write(json.dumps(data, indent=4, sort_keys=True, default=str, ensure_ascii=False).encode("utf8"))
        json.dump(data, fp, indent=4, sort_keys=True, default=str, ensure_ascii=False)


def load_json(f_path):
    with open(f_path, "r") as fp:
        return json.load(fp)
