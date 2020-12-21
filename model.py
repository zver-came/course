from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker
import classes

class Model:
    def __init__(self):
        self.session_s=None
        self.session_m=None

    def connect(self):
        engine1 = create_engine('postgresql://postgres:1111@192.168.1.113/course')
        engine2 = create_engine('postgresql://postgres:1111@192.168.1.109/course')
        try:
            engine2.connect()
            self.session_s = sessionmaker(bind=engine2)()
        except:
            print("Error connection with PostgreSQL replica, use of master power")
            try:self.session_s = sessionmaker(bind=engine1)()
            except:print('Master can`t work this operation')
        try:
            engine1.connect()
            self.session_m=sessionmaker(bind=engine1)()
        except:
            print("Error connection with PostgreSQL master, use of sleeve power make some settings")
            return False
        engine1.dispose()
        engine2.dispose()
        return True

    def close(self):
        try:
            if(self.session_m!=None):self.session_m.close()
            if(self.session_s!=None):self.session_s.close()
            print("Connection closed")
        except Exception as error:print("Error close connection with PostrgreSQL",error)

    #Master funtion
    def add_new_item(self, new_item):
        try:
            self.session_m.add(new_item)
            self.session_m.commit()
            return new_item
        except Exception as exp:
            print('You have problem with adding item. Detail info: %s' % exp)

    def update_item(self):
        try:
            self.session_m.commit()
        except Exception as exp:
            print('You have problem with update item. Detail info: %s' % exp)

    #Sleave function
    def select_location(self,value1,value2): return self.session_s.query(classes.Location).filter(classes.Location.latitude==value1,classes.Location.longitude==value2).first()

    def select_date(self,date):return self.session_s.query(classes.Date_weather).filter(classes.Date_weather.index_date==date).first()

    def cheack_index(self,location_id, date_id):return self.session_s.query(classes.Indexes).filter(classes.Indexes.city_id == location_id,classes.Indexes.date_id == date_id).first()

    def select_all_location(self):return self.session_s.query(classes.Location).all()

    def select_city_position(self,value1,value2):
        country_id=self.session_s.query(classes.Countries.country_id).filter(classes.Countries.country_code==value2).first()
        return self.session_s.query(classes.Location).filter(classes.Location.city==value1,classes.Location.country_id==country_id).first()
    
    def select_country_position(self,value1):return self.session_s.query(classes.Countries).filter(classes.Countries.country_code==value1).first()

    #Sleave function for analyze data
    def get_indexes_for_city_in_time_period(self,value1,value2,value3):
        array_date_id=self.session_s.query(classes.Date_weather.date_id).filter(classes.Date_weather.index_date>=value2,classes.Date_weather.index_date<=value3)
        return self.session_s.query(classes.Indexes).filter(classes.Indexes.city_id==value1,classes.Indexes.date_id.in_(array_date_id)).all()

    def get_indexes_for_country_in_time_period(self,value1,value2,value3):
        array_date_id=self.session_s.query(classes.Date_weather.date_id).filter(classes.Date_weather.index_date>=value2,classes.Date_weather.index_date<=value3)
        country_id=self.session_s.query(classes.Countries.country_id).filter(classes.Countries.country_code==value1).first()
        array_city_id=self.session_s.query(classes.Location.address_id).filter(classes.Location.country_id==country_id)
        return self.session_s.query(classes.Indexes).filter(classes.Indexes.city_id.in_(array_city_id),classes.Indexes.date_id.in_(array_date_id)).all()