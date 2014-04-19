from ajenti.api import *  # noqa
from ajenti.plugins import *  # noqa

info = PluginInfo(
        title='dnsmasq',
        icon='globe',
        dependencies=[
            PluginDependency('main')
            ],
        )

def init():
    import main
