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
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    sess = create_sessionmaker(settings, "sqlalchemy.")()
    Base.metadata.create_all(sess.bind)

#    with transaction.manager:
#        model = MyModel(name='one', value=1)
#        sess.add(model)


