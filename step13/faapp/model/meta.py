from sqlalchemy import (
    Column, ForeignKey,
    Integer,
    String, Text, Unicode,

    engine_from_config,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    mapper
    )

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()

def _(t):
    """
        Only used to mark strings to extract for translation.
        Does not really perform any translation.
    """
    pass

class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    number = Column(Integer)
    address = Column(Integer, ForeignKey("address.id"))

    def __init__(self, name="", number=0):
        self.name = name
        self.number = number

    def __unicode__(self):
        return unicode(self.name)

[ _("Name"), _("Number"), _("Address"), ]

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    line1 = Column(Unicode(100))
    line2 = Column(Unicode(100))
    city = Column(Unicode(100))
    postcode = Column(Unicode(100))
    country = Column(Unicode(100))

    persons = relationship("Person", backref="addr")

    def __init__(self, line1="", line2="", city="", postcode="", country=""):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.postcode = postcode
        self.country = country

    def __unicode__(self):
        return unicode("%s/%s %s %s" % (self.line1, self.line2, self.city, self.country))

[ _("Line1"), _("Line2"), _("City"), _("Postcode"), _("Country"), _("Persons"), ]


class NonId(Base):
    __tablename__ = "nonid"
    pri1 = Column(String(10), primary_key=True)
    pri2 = Column(String(10), primary_key=True)
    data = Column(Unicode(50))
    def __init__(self, pri1 = "", pri2="", data=""):
        self.pri1 = pri1
        self.pri2 = pri2
        self.data = data
    def __unicode__(self):
        return unicode("%s-%s:%s" % (self.pri1, self.pri2, self.data))

[ _("Pri1"), _("Pri2"), _("Data"), ]

def create_sessionmaker(settings, prefix):
    """
        Returns a session factory.
    """
    engine = engine_from_config(settings, prefix)
    return sessionmaker(
        bind=engine,
        extension=ZopeTransactionExtension(),
    )

def get_pk_map(instance):
    """
        Returns a map column_name --> value with the instance's primary keys.

        Note: This probably won't work for strangely named columns (that
        cannot act as python identifiers).
    """
    ret = {}
    for column in instance.__table__.columns:
        if column.primary_key:
            ret[column.name] = getattr(instance, column.name)

    return ret

model_names = []

for (name, ent) in locals().items():
    if name.startswith("_"):
        continue
    if "Base"==name:
        continue
    try:
        if issubclass(ent, Base):
            model_names.append(name)
    except:
        pass
