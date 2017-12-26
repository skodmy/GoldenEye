"""

"""
import os
import random

PKG_BASE_DIR = os.path.dirname(__file__)

RESOURCES_BASE_DIR = os.path.join(PKG_BASE_DIR, 'res')

DEBUG = False

SSL_VERIFY = True

METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_RAND = 'random'

JOIN_TIMEOUT = 1.0

DEFAULT_WORKERS = 10
DEFAULT_SOCKETS = 500

PLATINUM_EYE_BANNER = 'GoldenEye v2.1 by Jan Seidl <jseidl@wroot.org>' # TODO change contents

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': [ 'Linux x86_64', 'Linux i386' ],
            'ext': [ 'X11' ]
        },
        'windows': {
            'name': [ 'Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 'Windows NT.6.2' ],
            'ext': [ 'WOW64', 'Win64; x64' ]
        },
        'mac': {
            'name': [ 'Macintosh' ],
            'ext': [ 'Intel Mac OS X %d_%d_%d' % (random.randint(10, 11), random.randint(0, 9), random.randint(0, 5)) for i in range(1, 10) ]
        },
    },
    'platform': {
        'webkit': {
            'name': [ 'AppleWebKit/%d.%d' % (random.randint(535, 537), random.randint(1,36)) for i in range(1, 30) ],
            'details': [ 'KHTML, like Gecko' ],
            'extensions': [ 'Chrome/%d.0.%d.%d Safari/%d.%d' % (random.randint(6, 32), random.randint(100, 2000), random.randint(0, 100), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 30) ] + [ 'Version/%d.%d.%d Safari/%d.%d' % (random.randint(4, 6), random.randint(0, 1), random.randint(0, 9), random.randint(535, 537), random.randint(1, 36)) for i in range(1, 10) ]
        },
        'iexplorer': {
            'browser_info': {
                'name': [ 'MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0' ],
                'ext_pre': [ 'compatible', 'Windows; U' ],
                'ext_post': [ 'Trident/%d.0' % i for i in range(4, 6) ] + [ '.NET CLR %d.%d.%d' % (random.randint(1, 3), random.randint(0, 5), random.randint(1000, 30000)) for i in range(1, 10) ]
            }
        },
        'gecko': {
            'name': [ 'Gecko/%d%02d%02d Firefox/%d.0' % (random.randint(2001, 2010), random.randint(1,31), random.randint(1,12) , random.randint(10, 25)) for i in range(1, 30) ],
            'details': [],
            'extensions': []
        }
    }
}
