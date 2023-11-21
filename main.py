#!/Users/hoangkhanh/anaconda3/envs/ds/bin/python3

from tqdm import tqdm
import requests
import pandas as pd
import os
from utils import COOKIES, HEADERS, create_backup_folder, save_json, load_json
from bs4 import BeautifulSoup


def get_data(backup=False):
    if backup:
        backup_file = input("Nhập tên file backup sử dụng: ")
        backup_file = f"./backup/{backup_file}"
        if not os.path.exists(backup_file):
            print("Không tìm thấy file backup")
            return []
        df = load_json(backup_file)
    else:
        df = []
    return df


def get_thread_content(source: BeautifulSoup):
    posts = []
    post_elements = source.select("li.message")
    for post_element in post_elements:
        post = dict()
        author = post_element.select_one("h3.userText")
        author = author.select_one("a.username") if author else None
        post["author"] = author.get_text() if author else None

        time = post_element.select_one("a.datePermalink")
        post["time"] = time.get_text() if time else None

        content = post_element.select_one("div.messageContent")
        post["content"] = content.get_text().strip() if content else None

        posts.append(post)
    return posts


def get_thread(thread_link):
    posts = []
    response = requests.get(
        thread_link,
        cookies=COOKIES,
        headers=HEADERS
    )
    first_page_source = BeautifulSoup(response.text, "html.parser")
    last_page = first_page_source.select_one("div.PageNav")
    last_page = last_page.get("data-last") if last_page else None
    last_page = int(last_page) if last_page else None

    posts += get_thread_content(first_page_source)

    if last_page:
        for page in tqdm(range(2, last_page + 1), ncols=75):
            response = requests.get(
                f"{thread_link}page-{page}",
                cookies=COOKIES,
                headers=HEADERS
            )
            page_source = BeautifulSoup(response.text, "html.parser")
            posts += get_thread_content(page_source)
    return posts


def get_threads(start, end, data):
    threads = []

    # GET THREADS
    for page in range(start, end + 1):
        url = f"https://f319.com/forums/thi-truong-chung-khoan.3/page-{page}"
        response = requests.get(
            url,
            cookies=COOKIES,
            headers=HEADERS
        )
        if response.status_code == 200:
            page_source = BeautifulSoup(response.text, "html.parser")
            print(f"========== TRANG {page} ==========")
            thread_elements = page_source.select("li.discussionListItem")
            for thread_element in thread_elements:
                thread = dict()
                thread["page"] = page

                name = thread_element.select_one("h3.title")
                thread["name"] = name.get_text().strip() if name else None

                url = name.find("a")
                thread["url"] = "https://f319.com/" + url.get("href").strip() if url else None

                print("Đang cào threads: ", thread["name"], thread["url"])

                date = thread_element.select_one(".posterDate").select_one("span.DateTime")
                thread["date"] = date.get_text().strip() if date else ""

                thread["author"] = thread_element.get("data-author")

                thread["posts"] = get_thread(thread["url"]) if thread["url"] else []

                threads.append(thread)

                data += threads

                # backup file after avery 50 pages
                if page % 50 == 0:
                    save_json(data, f"./backup/threads_start{start}_end{page}.json")

        else:
            print(f"Lỗi {response.status_code} tại trang {url}")

    save_json(data, f"./threads_all_start{start}_end{end}.json")
    return True


if __name__ == "__main__":
    while True:
        print("Bắt đầu cào dữ liệu, f319.com...")
        create_backup_folder()
        has_backup = input("Bạn có file backup? (y/[n]): ") or "n"
        df_all = get_data(backup=(has_backup == "y"))
        start_page = int(input("   - Bắt đầu cào từ trang bao nhiêu? [default=1]: ") or 1)
        max_page = int(input("   - Kết thúc cào tại trang bao nhiêu? [default=1000]: ") or 1000)
        done = get_threads(start_page, max_page, df_all)
        if done:
            break
