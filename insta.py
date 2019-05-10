# coding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import sys, json, re, os, io, requests
from datetime import datetime

PROFILE_PATH = "C:\\Users\\{0}\\AppData\\Local\\Google\\Chrome\\User Data".format(os.environ.get("USERNAME"))

userdata_dir = 'UserData'
os.makedirs(userdata_dir, exist_ok=True)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# tmp_tag = open("tag.txt", "r", encoding="utf-8")
# tag = tmp_tag.read()
# tmp_tag.close()
# os.remove("tag.txt")
#
# data = json.loads(sys.stdin.readline())
# act1 = data["act1"]
# times = int(data["times"])
# act2 = data["act2"]
# number = int(data["number"])
# opt1 = data["opt1"]
# opt2 = data["opt2"]
# opt3 = data["opt3"]
# opt4 = data["opt4"]
# opt5 = data["opt5"]
# opt6 = data["opt6"]
# opt7 = data["opt7"]
# opt8 = data["opt8"]
# num1 = int(data["num1"])
# num2 = int(data["num2"])
# num3 = int(data["num3"])

#テスト用

# tag = "カフェ"
# act1 = False
# times = 5
# act2 = False
# number = 5
# opt1 = True
# opt2 = True
# opt3 = True
# opt4 = False
# opt5 = True
# opt6 = True
# opt7 = True
# opt8 = True
# num1 = 1
# num2 = 1
# num3 = 1

line_notify_token = 'GXfWzNXa2GuTTU8MtfvbGT9tKmSpoTSAobPELTOO3SQ'
line_notify_api = 'https://notify-api.line.me/api/notify'

options = webdriver.ChromeOptions()
# driver_path = r"src/chromedriver.exe"

driver_path = r"../chromedriver.exe"

PROFILE_PATH = "C:\\Users\\{0}\\AppData\\Local\\Google\\Chrome\\User Data".format(os.environ.get("USERNAME"))

userdata_dir = 'UserData'
os.makedirs(userdata_dir, exist_ok=True)

good_user_list = []


def login_check():
    sleep(1)
    searches = driver.find_elements_by_xpath('//*[@placeholder="検索"]')
    if len(searches) != 0:
        return True
    else:
        URL = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        driver.get(URL)
        message = "<初回設定>\nログインした後、一度ブラウザーを閉じてもう一度実行ボタンを押して下さい。"
        print(json.dumps({"result":message}))
        return False


def make_driver():
    global driver

    options.add_argument('--user-data-dir=' + userdata_dir)

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    URL = "https://www.instagram.com/"
    driver.get(URL)
    driver.set_window_position(0, 0)
    driver.set_window_size(600, 660)
    if driver.current_url != URL:
        print(json.dumps({"result":"既に他のChromeが開かれています。\nすべて閉じてからもう一度実行してください。"}))


def headless():
    global driver

    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)


# falseだと0になる
def f(bool, num):
    if bool:
        return num

    return 0


# 〇〇千などを数値化
def num_to_int(num):
    if "," in num:
        parts = num.split(",")
        return int(parts[0])*1000 + int(parts[1])
    elif "千" in num:
        return int(float(num.split("千")[0])*1000)
    elif "百万" in num:
        return int(float(num.split("百万")[0])*1000000)
    else:
        return int(num)

# 文字列にひらがなorカタカナが入っていればTrue
def kana_in(word):
    kana_set = {chr(i) for i in range(12353, 12436)}
    for kana in {chr(i) for i in range(12449, 12533)}:
        kana_set.add(kana)
    word_set = set(word)
    if kana_set - word_set == kana_set:
        return False
    else:
        return True


# 韓国語または中国語特有の漢字が入っていればTrue
def asian_check(in_str):
    return (set(in_str) - set(in_str.encode('sjis','ignore').decode('sjis'))) != set([])


# タグ検索を無理やり行う、そのタグが存在しなければメインページに戻る
# 空の文字列の時はトレンドサーチになる
def tag_search(tag):
    if "1" in tag or "2" in tag or "3" in tag or "4" in tag or "5" in tag or "6" in tag or "7" in tag or "8" in tag or "9" in tag or "0" in tag:
        driver.get("https://www.instagram.com/explore/locations/{0}/".format(tag))
    else:
        driver.get("https://www.instagram.com/explore/tags/{0}/".format(tag))
    driver.set_page_load_timeout(10)
    if len(driver.find_elements_by_class_name("dialog-404")) != 0:
        print(json.dumps({"result":"検索したタグは存在しませんでした。\n検索タグに間違いがないかご確認ください。"}))
        driver.close()


# 投稿に対して、いいね！した人とコメントした人のIDをいっぱい取得する
def id_get():
    WebDriverWait(driver, 3)
    sleep(1)
    for i in range(20):
        liked_by = driver.find_elements_by_xpath('//button[@type="button"]/span')
        if len(liked_by) == 0:
            driver.back()
            sleep(2)
            driver.find_elements_by_xpath('//div[div[img[contains(@alt, "画像")]]]')[crawl_count].click()
            sleep(2)
        elif num_to_int(liked_by[0].text) >= 20:
            liked_by[0].click()
            break
        else:
            nexts = driver.find_elements_by_xpath('//a[text()="次へ"]')
            if len(nexts) != 0:
                nexts[0].click()
                sleep(3)
            else:
                break
    WebDriverWait(driver, 3)
    sleep(1)
    scrolls = driver.find_elements_by_xpath('//div[contains(@style, "flex-direction")]/div[11]')
    if len(scrolls) != 0:
        scroll = scrolls[0]
        actions = ActionChains(driver)
        actions.move_to_element(scroll)
        actions.perform()
        WebDriverWait(driver, 3)
        sleep(1)
    else:
        pass

    a_tags = driver.find_elements_by_tag_name('a')

    id_list = []
    WebDriverWait(driver, 3)
    for a_tag in a_tags:
        id = a_tag.get_attribute('title')
        if id == "":
            pass
        else:
            id_list.append(id)

    driver.find_element_by_xpath('//*[@aria-label="閉じる"]').click()
    WebDriverWait(driver, 3)
    return sorted(set(id_list), key=id_list.index)


# ユーザーページに移動し各種情報を取得
def get_id_info(id):
    driver.get("https://www.instagram.com/{0}/?hl=ja".format(id))
    driver.save_screenshot('screenshot.png')
    driver.set_page_load_timeout(10)
    id = id.lower()
    names = driver.find_elements_by_tag_name('h1')
    if len(names) == 1:
        name = ""
    elif len(names) != 0:
        name = names[1].text
    else:
        name = ""
    nums = driver.find_elements_by_xpath('//ul/li/*/span')
    post = num_to_int(nums[0].text)
    byfollow = num_to_int(nums[1].text)
    follow = num_to_int(nums[2].text)
    intros = driver.find_elements_by_xpath("//main/div/div[1]/span")
    section = driver.find_elements_by_xpath("//section/div/span")
    if len(intros) != 0:
        intro = intros[0].text
    elif len(section) > 0:
        intro = section[0].text
    else:
        intro = ""

    # ストップワード
    official = (len(driver.find_elements_by_xpath('//span[@title="認証済み"]')) != 0 or
                "official" in id or
                "circle" in id or
                "group" in id or
                "club" in id or
                "team" in id or
                "japan" in id or
                "shop" in id or
                "同好会" in name or
                "協会" in name or
                "公式" in name or
                "団体" in name or
                "日本" in name or
                "店" in name or
                "お問い合わせ" in intro or
                "プレゼント" in intro or
                "海外投資" in intro or
                "ご予約" in intro or
                "ご案内" in intro or
                "ご紹介" in intro or
                "お客様" in intro or
                "弊社" in intro or
                "開業" in intro or
                "公式" in intro or
                "公認" in intro or
                "開催" in intro or
                "無料" in intro or
                "投資" in intro or
                "稼ぎ" in intro
                )
    return {"id":id, "name":name, "post":post, "follow":follow, "byfollow":byfollow, "intro":intro, "official":official}


# jap=True:名前か説明文にひらがながないとはじく
# foreign=True:説明文に韓国語や中国語があるとはじく
# official=True:認証済みアカウントをはじく
# over_follow=True:フォローがフォロワーより三倍以上多いとはじく
# over_byfollow=True:フォロワーがフォローより三倍以上多いとはじく
# min_follow=int:フォローがint人以下ははじく
# min_byfollow=int:フォロワーがint人以下ははじく
# min_post=int:投稿がint件以下ははじく
def good_user(user, jap=True, foreign=False, official=True, over_follow=True, over_byfollow=True, min_follow=5, min_byfollow=5, min_post=1):
    flag = 0
    if jap==False or kana_in(user["intro"]) or kana_in(user["name"]):
        flag += 1
    if foreign==False or asian_check(user["intro"]):
        flag += 1
    if official==False or user["official"]==False:
        flag += 1
    if over_follow==False or (user["follow"] <= user["byfollow"]*3):
        flag += 1
    if over_byfollow==False or (user["byfollow"] <= user["follow"]*3):
        flag += 1
    if user["follow"] >= min_follow:
        flag += 1
    if user["byfollow"] >= min_byfollow:
        flag += 1
    if user["post"] >= min_post:
        flag += 1
    if len(driver.find_elements_by_xpath('//button[contains(text(), "フォロー中")]')) == 0:
        flag += 1

    if flag == 9:
        good_user_list.append(user["id"])
        return True
    return False


# 個人ページにいる状態でその人をフォローしたりその人の投稿をいいねしたりできる。
def do_action(like_flag=True, like=1, follow=True):
    if follow:
        follows = driver.find_elements_by_xpath('//button[contains(text(), "フォローする")]')
        if len(follows) != 0:
            follows[0].click()
        else:
            followbacks = driver.find_elements_by_xpath('//button[contains(text(), "フォローバックする")]')
            if len(followbacks) != 0:
                followbacks[0].click()

    if like_flag:
        WebDriverWait(driver, 5)
        likes = driver.find_elements_by_xpath('//div[a[contains(@href, "/p/")]]')
        if len(likes) != 0:
            likes[0].click()
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="コメント"]')))
        sleep(1)
        like_count = 0
        for i in range(100):
            WebDriverWait(driver, 3)
            likes = driver.find_elements_by_xpath('//*[contains(@aria-label, "いいね！")]')
            liked = driver.find_elements_by_xpath('//*[contains(@aria-label, "取り消す")]')
            if len(liked) != 0:
                pass
            elif len(likes) != 0:
                likes[0].click()
                WebDriverWait(driver, 2)
                sleep(1)
            else:
                pass
            like_count += 1
            if like_count >= like:
                break
            nexts = driver.find_elements_by_xpath('//a[text()="次へ"]')
            if len(nexts) != 0:
                nexts[0].click()
                sleep(1)
            else:
                break
            WebDriverWait(driver, 4)


# タグ検索で投稿に関連した人の中から目的ユーザーがnum人みつかるまでクローリングする
def post_crawl(words, act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3):
    WebDriverWait(driver, 2)
    tag_search(words)
    WebDriverWait(driver, 5)
    sleep(2)
    good_count = 0
    global crawl_count
    crawl_count = 0
    for i in range(100):
        posts = driver.find_elements_by_xpath('//a[contains(@href, "/p/")]/div')
        if len(posts) != 0:
            posts[crawl_count].click()
            crawl_count += 1
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="保存する"]')))

        # ↓--------この間にクローリング時の処理---------↓

        id_set = id_get()
        for id in id_set:
            user = get_id_info(id)
            if good_user(user, opt1, opt2, opt3, opt4, opt5, f(opt6, int(num1)), f(opt7, int(num2)), f(opt8, int(num3))):
                do_action(act1, times, act2)
                good_count += 1
            if good_count >= number:
                break
        if good_count >= number:
            print(json.dumps({"result":"目標人数に到達しました。\n(再実行する場合は一度ブラウザを閉じてから実行してください。)"}))

            message = "*実行詳細*\n実行者：{0}\n検索ワード：{1}\n獲得ユーザー：{2}\n実行日時：{3}".format(os.environ.get("USERNAME"), tag, good_user_list, datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            payload = {'message': message}
            headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
            requests.post(line_notify_api, data=payload, headers=headers)

            break

        # ↑--------この間にクローリング時の処理---------↑

        tag_search(words)
        WebDriverWait(driver, 4)
        sleep(2)


# おすすめに表示されたユーザーからグッドユーザーを選別
def extend_follow(act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3):
    driver.get("https://www.instagram.com/explore/people/suggested/")

    html01 = driver.page_source
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 3)
        sleep(3)
        html02 = driver.page_source
        if html01 != html02:
            html01 = html02
        else:
            break

    good_count = 0
    a_tags = driver.find_elements_by_tag_name('a')

    id_list = []
    WebDriverWait(driver, 3)
    for a_tag in a_tags:
        id = a_tag.get_attribute('title')
        if id == "":
            pass
        else:
            id_list.append(id)

    WebDriverWait(driver, 3)
    id_set = sorted(set(id_list), key=id_list.index)
    for id in id_set:
        user = get_id_info(id)
        if good_user(user, opt1, opt2, opt3, opt4, opt5, f(opt6, int(num1)), f(opt7, int(num2)), f(opt8, int(num3))):
            do_action(act1, times, act2)
            good_count += 1
        if good_count >= number:
            break

    if good_count >= number:
        print(json.dumps({"result": "目標人数に到達しました。\n(再実行する場合は一度ブラウザを閉じてから実行してください。)"}))

        message = "*実行詳細*\n実行者：{0}\n検索ワード：{1}\n獲得ユーザー：{2}\n実行日時：{3}"\
            .format(os.environ.get("USERNAME"), tag,good_user_list, datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
        requests.post(line_notify_api, data=payload, headers=headers)


# 検索タグに関連するロケーションのリストを作り、気になるロケーションを選択→クローリング→ユーザー獲得
def location_search(words, times):
    WebDriverWait(driver, 2)
    tag_search(words)
    WebDriverWait(driver, 5)
    sleep(2)
    catch_count = 0
    location_list = []
    posts = driver.find_elements_by_xpath('//div[div[img[contains(@alt, "画像")]]]')
    if len(posts) != 0:
        posts[0].click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="保存する"]')))

    for i in range(100):

        # ↓--------この間にクローリング時の処理---------↓

        locations = driver.find_elements_by_xpath('//a[contains(@href, "/explore/locations/")]')
        if len(locations) != 1:
            catch_count += 1
            location_list.append([locations[1].text, locations[1].get_attribute("href").split("/")[5]])

        if catch_count >= times:
            break

        # ↑--------この間にクローリング時の処理---------↑

        nexts = driver.find_elements_by_xpath('//a[text()="次へ"]')
        if len(nexts) != 0:
            nexts[0].click()
            sleep(1)
        WebDriverWait(driver, 4)
        sleep(2)

    message = "*獲得ロケーション*\n\n 気になる場所のIDを検索タグに入れて検索すると、ロケーション検索モードになります\n"
    for location in location_list:
        message += "\n{0}(ID:{1})".format(location[0], location[1])
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    requests.post(line_notify_api, data=payload, headers=headers)


# タグ名によるモードチェック
def mode_check(tag, act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3):
    if tag == "":
        extend_follow(act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3)
    elif act1 == False and act2 == False:
        location_search(tag, times)
    else:
        post_crawl(tag, act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3)


def unfollow(account, protect_list):
    driver.get("https://www.instagram.com/")
    driver.set_page_load_timeout(10)
    sleep(3)
    # driver.find_element_by_xpath('//span[@aria-label="プロフィール"]').click()
    driver.get("https://www.instagram.com/" + account + "/")
    print("https://www.instagram.com/" + account + "/")
    driver.set_page_load_timeout(10)
    sleep(2)
    driver.find_element_by_xpath('//a[contains(@href, "/followers/")]').click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="閉じる"]')))

    html01 = driver.page_source
    while True:
        driver.find_elements_by_tag_name("a")[-1].location_once_scrolled_into_view
        WebDriverWait(driver, 3)
        sleep(5)
        html02 = driver.page_source
        if html01 != html02:
            html01 = html02
        else:
            break

    follower_list = driver.find_elements_by_tag_name("a")

    driver.find_element_by_xpath('//span[@aria-label="閉じる"]').click()
    sleep(1)

    driver.find_element_by_xpath('//a[contains(@href, "/following/")]').click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="閉じる"]')))

    html01 = driver.page_source
    while True:
        driver.find_elements_by_tag_name("a")[-1].location_once_scrolled_into_view
        WebDriverWait(driver, 3)
        sleep(5)
        html02 = driver.page_source
        if html01 != html02:
            html01 = html02
        else:
            break

    following_list = driver.find_elements_by_tag_name("a")
    follow_button = driver.find_elements_by_tag_name("button")

    for i in range(len(following_list)):
        if following_list[i] in follower_list:
            continue
        elif following_list[i] in protect_list:
            continue
        else:
            follow_button[i].click()
            sleep(2)


# ココから下が実行部

# make_driver()

id = ""
headless()
print(get_id_info(id))


if login_check():

    account = ""
    unfollow(account, protect_list=[])

    #mode_check(tag, act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3)

    #extend_follow(act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3)

    #post_crawl(tag, act1, times, act2, number, opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, num1, num2, num3)

    #location_search(tag, times)
