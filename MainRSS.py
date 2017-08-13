# import custom modules
import setup
import Web

# Setup Env
Tasks = setup.Tasks
CurEnv = setup.getWorkDict()
BasePath = CurEnv['OutPath']
print(BasePath)


# Main Loop
for key1 in Tasks:
    CurData = Tasks[key1]
    # name = key
    site_url = CurData['site_url']
    site_bbs = CurData['site_bbs']
    feed_url = CurData['feed_url']
    CurItem = CurData['rss_item']

    print('RSS Build Site: %s is Start' % key1)
    ctMax = len(CurItem)
    ctNow = 1
    for key2 in CurItem:
        CurHTM = key1 + '_' + key2
        CurRSS = CurItem[key2]
        CurBBS = CurRSS['bbs_list']
        CurDesc = CurRSS['rss_desc']
        CurPage = CurRSS['s_page'] - 1
        CurFeed = CurRSS['f_name']
        CurCond = CurRSS['r_cond']

        # print(' - RSS: ' + t_file)
        for key3 in CurBBS:
            u = site_url + site_bbs + key3
            # print('   - BBS: ' + u)
            for i in range(CurPage, -1, -1):
                try:
                    cur_u = u + '?&po=%d' % i
                    # print('   -- Pages: ' + cur_u)
                    Web.Parsing_BBS(key1, cur_u, CurCond, 0, site_url, CurHTM)
                except:
                    continue

        # Build RSS
        Web.Build_RSS(BasePath, CurHTM, site_url, CurDesc)
        print(" - %d/%d Done: %s" % (ctNow, ctMax, BasePath + "rss_" + CurHTM + ".htm"))
        # Ping Feedburner RSS Page
        Web.Read_Html(feed_url + CurFeed)
        print("       Ping: " + feed_url + CurFeed)
        ctNow += 1

    # Report Build Complete for One Site
    print('RSS Build Site: %s is Complete' % key1)
