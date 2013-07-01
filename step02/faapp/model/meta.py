from sqlalchemy import (
    Column, ForeignKey,
    Integer,
    Text, Unicode,

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
        return unicode(self.line1 + "/" + self.line2 + " " + self.city + " " + self.country)

def create_session(settings, prefix):
    engine = engine_from_config(settings, prefix)

    dbsession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    dbsession.configure(bind=engine)

    return dbsession

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


