from ConfigParser import RawConfigParser

parser = RawConfigParser()
f = file('stutter.ini', 'rt')
parser.readfp(f)
f.close()


class config(object):
    pass

def getSectionValues(section, keys):
    for key in keys:
        setattr(config, key, parser.get(section, key))

getSectionValues('main', 'username password url_base'.split())
getSectionValues('db', 'db_type connection'.split())

config.url_base = config.url_base.rstrip('/')

