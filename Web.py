from bs4 import BeautifulSoup
import urllib.request as urllib3
import PyRSS2Gen
import re
import datetime
import MariaDB


def Build_RSS(r_path, r_filename, r_home, r_desc):
    # Setup RSS
    t_delta = datetime.timedelta(hours=9)
    rss = PyRSS2Gen.RSS2(
        title=r_filename,
        link=r_home,
        description=r_desc,
        lastBuildDate=datetime.datetime.utcnow(),
        items=[])

    # Read DB for Current RSS
    CurData = MariaDB.ReadSQL(r_filename)

    # Append Item to RSS
    for r in CurData:
        item = PyRSS2Gen.RSSItem(
            title=r['title'],
            link=r_home + r['url'],
            guid=PyRSS2Gen.Guid(r_home + r['url']),
            description=str(r['text']),
            pubDate=r['pubdate'] - t_delta,
            author=r['author'])
        rss.items.append(item)

    # Write RSS
    rss.write_xml(
        open(r_path + "rss_" + r_filename + ".htm", 'w', encoding='utf-8'),
        encoding="utf-8"
    )


def Parsing_BBS(site, link, rep_cond, rec_cond, t_home, rss_name):
    if site == 'clien':
        Parsing_BBS_Clien(link, rep_cond, rec_cond, t_home, rss_name)


def Parsing_BBS_Clien(link, rep_cond, rec_cond, t_home, rss_name):
    # Set deadline, clear old database
    deadline = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
    MariaDB.DeleteSQL(deadline, rss_name)

    # Parsing
    html = Read_Html(link)
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.findAll("div", {"class": "item"})

    for el in elements:
        # Pass notice item
        if el.encode('utf-8').find('<span>공지</span>'.encode('utf-8')) > -1:
            continue

        # check pub date, break for old posting, risky code
        pubdate = el.find("span", {"class": "timestamp"}).text.strip()
        if date(pubdate) < deadline and rep_cond == 0:
            break

        # Parsing html to data
        title = ' '.join(el.find("a").text.split())
        url = el.find('a')['href'].strip().split('?')[0]
        r_count = get_number(el.findAll("span", {"class": "badge-reply"}))
        s_count = get_number(el.findAll("div", {"class": "list-symph"}))
        category = link.split('/')[-1].split('?')[0]

        # If reply >= rep_cond Parsing Post
        if r_count >= rep_cond:
            # Dup post check by 'url'
            if not MariaDB.UpdateSQL(rss_name, url, r_count, s_count):
                html = Read_Html(t_home + url)
                soup = BeautifulSoup(html, "html.parser")
                elements = soup.findAll("body")
                text = elements[1]

                # Parsing Published Date
                # pdate = soup.findAll("div", {"class": "post-time"})
                # pub_date = pdate[0].text.strip()

                # Parsing Author
                auth1 = soup.findAll("button", {"class": "button-md button-report"})
                author = re.search("[\w]+(?=\')", str(auth1[0])).group()

                # Post Info Insert to DB
                MariaDB.InsertSQL(rss_name, category, title, text, url, pubdate, author, r_count, s_count)
        continue


def Read_Html(link):
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; "
    user_agent += "Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; "
    user_agent += ".NET CLR 3.5.30729)"
    req = urllib3.Request(
        link,
        data=None,
        headers={'User-Agent': user_agent})
    response = urllib3.urlopen(req)
    return response.read()


def date(datestr="", format="%Y-%m-%d %H:%M:%S"):
    if not datestr:
        return datetime.datetime.date()
    return datetime.datetime.strptime(datestr, format).date()


def get_number(elements):
    n1 = 0
    if len(elements) > 0:
        n1 = int(elements[0].text)
    return n1


# Module Test Code
# s1 = 'clien'
# u1 = 'https://www.clien.net/service/board/news?&po=0'
# Parsing_BBS(s1, u1, 0, 0, 'https://www.clien.net', 'test_rss')
