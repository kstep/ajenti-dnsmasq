# -*- encoding: utf-8 -*-

from ajenti.api import *  # noqa
from ajenti.ui import on
from ajenti.ui.binder import Binder
from ajenti.plugins import *  # noqa
from ajenti.plugins.main.api import SectionPlugin
from datetime import datetime

class DnsmasqLeases(object):
    leases = []

    class Lease:
        def __init__(self, lease_rec):
            now = datetime.now()
            self.expires = datetime.fromtimestamp(int(lease_rec[0]))
            self.expires_in = self.expires - now
            self.macaddr = lease_rec[1]
            self.ipaddr = lease_rec[2]
            self.hostname = lease_rec[3]
            self.hostid = lease_rec[4]

    def __init__(self, leases_file='/var/lib/misc/dnsmasq.leases'):
        if leases_file:
            self.load(leases_file)

    def update(self):
        self.load(self.leases_file)

    def load(self, leases_file):
        self.leases_file = leases_file
        self.leases = []

        with open(leases_file, 'r') as f:
            for line in f.readlines():
                self.leases.append(self.Lease(line.split()))

@plugin
class Dnsmasq(SectionPlugin):
    def init(self):
        self.icon = 'globe'
        self.title = 'Dnsmasq'
        self.category = _('Software')

        self.append(self.ui.inflate('dnsmasq:main'))
        self.leases = DnsmasqLeases()
        self.binder = Binder(self.leases, self.find('main'))
        self.binder.populate()


    @on('refresh', 'click')
    def refresh(self):
        self.leases.update()
        self.binder.populate()

