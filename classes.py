from sqlalchemy import Column, Integer, String,ForeignKey,Float,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Countries(Base):
    __tablename__ = 'countries'
    country_id = Column('country_id', Integer, autoincrement=True, primary_key=True)
    country = Column('country', String(100))
    country_code = Column('country_code', String(10))
    cities = relationship("Location", back_populates="country", cascade='all, delete, delete-orphan')

    def __init__(self, country, world_id):
        self.country = country
        self.world_id = world_id

class Location(Base):
    __tablename__ = 'positions'
    address_id = Column('address_id',Integer, autoincrement=True, primary_key=True)
    city = Column('city', String(100))
    latitude = Column('latitude',Integer)
    longitude = Column('longitude', Integer)
    country_id = Column('country_id',Integer,ForeignKey('countries.country_id'))
    country = relationship("Countries", back_populates="cities")
    indexes=relationship("Indexes",back_populates="city",cascade='all, delete, delete-orphan')

    def __init__(self, city,country_id,latitude,longitude):
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.country_id=country_id

class Indexes(Base):
    __tablename__ = 'indexes'
    mint=Column('min_temperature', Float)
    maxt = Column('max_temperature', Float)
    dew_point = Column('dew_point', Float)
    rel_hum = Column('relative_humidity', Float)
    wind_speed = Column('wind_speed', Float)
    wind_direction = Column('wind_direction', Float,nullable=True)
    precipitation=Column('precipitation', Float)
    city_id = Column('city_id',Integer, ForeignKey('positions.address_id'), primary_key=True)
    city = relationship("Location", back_populates="indexes")
    date_id = Column('date_id',Integer, ForeignKey('date_time.date_id'), primary_key=True)
    date = relationship("Date_weather", back_populates="indexes")

    def __init__(self, date_id,city_id,mint, maxt,dew_point,rel_hum,wind_speed,wind_direction,precipitation):
        self.mint = mint
        self.maxt = maxt
        self.dew_point = dew_point
        self.rel_hum = rel_hum
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation
        self.city_id = city_id
        self.date_id = date_id

class Date_weather(Base):
    __tablename__ = 'date_time'
    date_id= Column('date_id',Integer, autoincrement=True, primary_key=True)
    index_date = Column('index_date',TIMESTAMP)
    indexes = relationship("Indexes", back_populates="date", cascade='all, delete, delete-orphan')

    def __init__(self,index_date):
        self.index_date=index_date