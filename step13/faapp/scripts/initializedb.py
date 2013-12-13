import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..model.meta import (
    create_sessionmaker,
    Base,
    NonId,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    """
        Create the database and seed it with the initial data.
    """
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    sess = create_sessionmaker(settings, "sqlalchemy.")()
    Base.metadata.create_all(sess.bind)

    with transaction.manager:
        sess.add(NonId(pri1="one", pri2="p2", data="one"))
        sess.add(NonId(pri1="two", pri2="p2", data="two"))
        sess.add(NonId(pri1="three", pri2="p2", data="three"))
        sess.add(NonId(pri1="evil-things", pri2="p2", data="fantastic four"))
        sess.add(NonId(pri1="evil_things", pri2="p2", data="fantastic four"))
        sess.add(NonId(pri1="e!@#$%^&**s", pri2="p2", data="fantastic four"))

