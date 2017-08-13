import platform
import sys

Envs = {
   'PCName': {
       'OutPath': 'YourOutPath/',
       'db': 'YourDBname',
       'table': 'YourTableNameForPC'
   },
   'NasName': {
       'OutPath': '/YourOutPath/',
       'db': 'YourDBname',
       'table': 'YourTableNameForNas'
   }
}

Tasks = {
    'clien': {
        'site_url': 'https://www.clien.net',
        'site_bbs': '/service/board/',
        'feed_url': 'http://feeds.feedburner.com/',
        'rss_item': {
            'hot50': {
                'bbs_list': {
                    'park',
                    'news',
                    'jirum',
                    'coupon',
                    'lecture',
                    'use',
                    'cm_iphonien',
                    'cm_car',
                    'cm_bike',
                    'cm_havehome',
                    'cm_nas'
                    },
                'rss_desc': 'Clien: Hot 50',
                'r_cond': 50,
                's_page': 4,
                'f_name': 'your_feedburner_feed_name'
            },
            'news': {
                'bbs_list': {'news'},
                'rss_desc': 'Clien: News',
                'r_cond': 0,
                's_page': 1,
                'f_name': 'your_feedburner_feed_name'
            },
            'jirum': {
                'bbs_list': {'jirum'},
                'rss_desc': 'Clien: Good Shoping',
                'r_cond': 0,
                's_page': 1,
                'f_name': 'your_feedburner_feed_name'
            },
            'coupon': {
                'bbs_list': {'coupon'},
                'rss_desc': 'Clien: Counpon',
                'r_cond': 0,
                's_page': 1,
                'f_name': 'your_feedburner_feed_name'
            }
        }
    }
}


def getWorkDict():
    run_loc = platform.node()
    # print(run_loc)
    if run_loc in Envs:
        WorkEnv = Envs[run_loc]
    else:
        # WorkEnv = Envs['others']
        print('Unexpected Location: <%s>, Script Stoped' % run_loc)
        sys.exit(...)
    return WorkEnv


# atom1 = getWorkDict()
# print(atom1['OutPath'])
