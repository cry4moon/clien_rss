import mysql.connector as MySQLdb
import config
import setup

CurEnv = setup.getWorkDict()
MariaDB = CurEnv['db']
MariaTable = CurEnv['table']
# print(MariaDB)
# print(MariaTable)


def ReadSQL(rss_name):
    query = "SELECT * FROM " + MariaTable
    query += " WHERE file = %(rss_name)s order by pubdate DESC limit 80"
    data = {'rss_name': rss_name}
    return QuerySQL(query, data, True)


def DeleteSQL(deadline, t_file):
    query = "DELETE FROM " + MariaTable
    query += " WHERE pubdate < %(deadline)s AND file = %(file)s"
    data = {'deadline': deadline, 'file': t_file}
    QuerySQL(query, data, False)


def UpdateSQL(url, reply, recom):
    bFind = False
    # MariaDB Select by url
    query = "SELECT reply, recom FROM " + MariaTable
    query += " WHERE url = %(url)s"
    data = {'url': url}
    rows = QuerySQL(query, data, True)

    if len(rows) > 0:
        bFind = True
        row = rows[0]
        if (reply > row['reply']) or (recom > row['recom']):
            query = "UPDATE " + MariaTable
            query += " SET reply = %(reply)s, recom = %(recom)s"
            query += " WHERE url = %(url)s"
            data = {'reply': reply, 'recom': recom, 'url': url}
            # print(up_query % up_data)
            QuerySQL(query, data, False)
    return bFind


def InsertSQL(hfile, category, title, text, url, pubdate, author, rep, rec):
    query = "INSERT INTO " + MariaTable
    query += " (file, category, title, text, url, pubdate, author, reply, recom) VALUES "
    query += " ( %(file)s, %(category)s, %(title)s, %(text)s, %(url)s, %(pubdate)s, %(author)s, %(reply)s, %(recom)s)"
    data = {
        'file': hfile.encode('utf-8'),
        'category': category.encode('utf-8'),
        'title': title.encode('utf-8'),
        'text': text.encode('utf-8'),
        'url': url.encode('utf-8'),
        'pubdate': pubdate.encode('utf-8'),
        'author': author.encode('utf-8'),
        'reply': rep,
        'recom': rec
        }
    QuerySQL(query, data, False)


def QuerySQL(Query, Data, Return=False):
    conn = MySQLdb.connect(
        host=config.mysql_server, user=config.mysql_id,
        passwd=config.mysql_password, db=MariaDB, port=3307, charset='utf8')
    curs = conn.cursor(dictionary=True)
    curs.execute(Query, Data)
    result = None
    if Return:
        result = curs.fetchall()
    conn.commit()
    return result


# d1 = datetime.datetime.now()
# deadline = datetime.datetime.now() - datetime.timedelta(hours=8)
# DeleteSQL(deadline, 'clien_jirum')
# insert_bbs('f_1', 'c1', 't1', 'te1_텍스트</test>', 'url1', d1, 'a1', 1, 1)
# check_atom('url1', 10, 5)
# d2 = ReadSQL('f_1')[0]
# print(d2['text'])
