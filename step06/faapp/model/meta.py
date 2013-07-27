from sqlalchemy import (
    Column, ForeignKey,
    Integer,
    String, Text, Unicode,

    engine_from_config,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    mapper,
    )

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    number = Column(Integer)
    address = Column(Integer, ForeignKey("address.id"))

    def __init__(self, name=""):
        self.name = name

    def __unicode__(self):
        return unicode(self.name)

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

def create_sessionmaker(settings, prefix):
    engine = engine_from_config(settings, prefix)
    return sessionmaker(bind=engine, extension=ZopeTransactionExtension())

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


