from calendar import monthrange
from _datetime import datetime,timedelta,date
from time import time
import pandas as pd
import random
import os
import glob
from view import View as view
import classes
import api_data
import model

class Controller:
    def __init__(self):
        self.model=model.Model()
        self.connect_flag=self.model.connect()

    #input info in database
    def review_input_date(self,date):
        date_id = self.model.select_date(datetime.strptime(date, '%m/%d/%Y %H:%M:%S'))
        if (date_id == None):date_id = self.model.add_new_item(classes.Date_weather(datetime.strptime(date, '%m/%d/%Y %H:%M:%S')))
        return date_id.date_id

    def review_input_address(self,country,address,Latitude,Longitude):
        address = address.split(',')
        address_id = self.model.select_location("{0:.4f}".format(float(Latitude)),"{0:.4f}".format(float(Longitude)))
        if (address_id == None):
            country_id=self.review_input_country(country, address[1])
            address_id = self.model.add_new_item(classes.Location( address[0],country_id, "{0:.4f}".format(float(Latitude)),"{0:.4f}".format(float(Longitude))))
        return address_id.address_id

    def cheack_data(self,rows):
        if (rows['Minimum Temperature'] == ''): rows['Minimum Temperature'] = 1.1
        if (rows['Maximum Temperature'] == ''): rows['Maximum Temperature'] = 1.1
        if (rows['Dew Point'] == ''): rows['Dew Point'] = 1.1
        if (rows['Relative Humidity'] == ''): rows['Relative Humidity'] = 1.1
        if (rows['Wind Speed'] == ''): rows['Wind Speed'] = 1.1
        if (rows['Wind Direction'] == ''): rows['Wind Direction'] = 1.1
        if (rows['Precipitation'] == ''): rows['Precipitation'] = 1.1
        return rows

    def enter_info(self):
        if(self.connect_flag==True):
            county =self.cheack_input_data('Enter country:')
            city = self.cheack_input_data('Enter city:')
            country_wid = self.cheack_input_data('Enter world country code:')
            start_time = self.enter_date('start')
            finish_time = self.enter_date('finish')
            self.upload_data(county, city, country_wid, start_time, finish_time)
        else:print('You can`t make this operation, server not ready')
        return

    def review_input_index(self,location_id,date_id,rows):
        index=self.model.cheack_index(location_id, date_id)
        rows = self.cheack_data(rows)
        index_value=classes.Indexes(date_id, location_id,rows['Minimum Temperature'],
            rows['Maximum Temperature'],rows['Dew Point'],rows['Relative Humidity'],
            rows['Wind Speed'],rows['Wind Direction'],rows['Precipitation'])
        if (index== None):self.model.add_new_item(index_value)
        else:
            index=classes.Indexes(index.city_id, index.date_id,rows['Minimum Temperature'],
            rows['Maximum Temperature'],rows['Dew Point'],rows['Relative Humidity'],
            rows['Wind Speed'],rows['Wind Direction'],rows['Precipitation'])
            self.model.update_item()

    def upload_data(self,county, city, country_wid, start_time, finish_time):
        end_date = datetime(int(finish_time[0]), int(finish_time[1]),
                                     monthrange(int(finish_time[0]), int(finish_time[1]))[1]).isoformat()
        start_date=datetime(int(start_time[0]), int(start_time[1]),
                                     monthrange(int(start_time[0]), int(start_time[1]))[1]).isoformat()
        if(start_date>end_date):
            end_date=start_date
            start_time=finish_time

        steps = datetime(int(start_time[0]), int(start_time[1]), 1).isoformat()
        recuest_flag=True
        while (steps != end_date):
            if ((12 - int(start_time[1] + 3)) <= 0):
                starts = datetime(int(start_time[0]), int(start_time[1]), 1).isoformat()
                steps = datetime(int(start_time[0]), 12, 31).isoformat()
                start_time[0] += 1
                start_time[1] = 1
            else:
                starts = datetime(int(start_time[0]), int(start_time[1]), 1).isoformat()
                steps = datetime(int(start_time[0]), int(start_time[1]) + 3, 1).isoformat()
                if (steps < end_date):
                    start_time[1] += 3
                else:
                    steps = end_date
                    start_time[1] = int(finish_time[1])
            api_data.make_query_string("%s,%s" % (city, country_wid), starts, steps)
            recuest_flag =self.insert_data_in_database(county)
            if(recuest_flag!=True):
                print('Data not found.')
                return

    def review_input_country(self,country, country_code):
        country_id = self.model.select_country_position(country_code)
        if (country_id == None): country_id = self.model.add_new_item(classes.Countries(country,country_code))
        return country_id.country_id

    def insert_data_in_database(self,country):
        location_id = None
        data=api_data.upload_data()
        has_rows=False
        for line in data:
            has_rows = True
            break
        if(has_rows==True):
            for rows in data:
                if(location_id==None): location_id=self.review_input_address(country,rows['Address'],rows['Latitude'],rows['Longitude'])
                date_id=self.review_input_date(rows['Date time'])
                self.review_input_index(location_id,date_id,rows)
            return True
        else:return False

    def cheack_input_date(self,text, min, max):
        while 1:
            try:
                data = int(input(text))
                if (data >= min and data <= max):return data
                print('Enter normal value between %s and %s' % (min, max))
            except:print('Try again')

    def enter_date(self,type):
        dates = {}
        dates[0] = self.cheack_input_date('Enter %s year, more then 2010:' % type, 2010,datetime.today().year)
        dates[1] = self.cheack_input_date('Enter %s month:' % type, 1, 12)
        return dates

    def cheack_input_data(self,title):
        while 1:
            try:
                input_text=input(title).strip()
                if(len(input_text)!=0):
                    return input_text
                else:print('Please enter data: ')
            except Exception as e:print(e)

    def select_time_period(self):
        date={}
        date[0] = self.enter_date('start')
        date[1] = self.enter_date('finish')
        if(datetime(date[0][0],date[0][1],1)>datetime(date[1][0],date[1][1],1)):
            buff= date[1]
            date[1]= date[0]
            date[0]=buff
        if(datetime(date[0][0],date[0][1],1)==datetime(date[1][0],date[1][1],1)):
            if(date[0][1]!=12):date[1][1]+=1
            else:date[0][1]-=1
        return date

    #city function
    def make_location_list(self):
        try:
            location=self.model.select_all_location()
            df=pd.DataFrame({'city':[row.city for row in location],
                             'country':[row.country.country for row in location],
                             'county code':[row.country.country_code for row in location]})
            df=df.set_index('county code')
            df=df.sort_values(by=['country','city'])
            print(df)
        except Exception as s:print(s)

    def select_city(self):
        city={}
        while 1:
            try:
                view.print_select_city_command()
                command=int(input('Enter command: '))
                if(command==1):city=self.select_city_by_name_and_country_code()
                elif(command==2):self.make_location_list()
                elif(command==3):return city
                elif(command==4):return False
                else:print('Please don\'t enter this command: {}'.format(command))
            except Exception as s: print('You enter incorect format input data, try again.',s)

    def select_city_by_name_and_country_code(self):
        while 1:
            city=input('Enter city: ')
            country_code=input('Enter country_code: ')
            location=self.model.select_city_position(city,country_code)
            if(location!=None):return location
            else:print("Sorry but city ({}) or county_code ({}) not found".format(city,country_code))

    #country function
    def select_country(self):
        country={}
        while 1:
            try:
                view.print_select_country_command()
                command=int(input('Enter command: '))
                if(command==1):country=self.select_country_by_country_code()
                elif(command==2):self.make_location_list()
                elif(command==3):return country
                elif(command==4):return False
                else:print('Please don\'t enter this command: {}'.format(command))
            except Exception as s: print('You enter incorect format input data, try again.',s)

    def select_country_by_country_code(self):
        while 1:
            country_code=input('Enter country_code: ')
            location=self.model.select_country_position(country_code)
            if(location!=None):return location
            else:print("Sorry but country with county_code ({}) not found".format(country_code))

    #work with indexes
    def get_temperature_indexes(self,flag,address,start_time, finish_time):
        if(flag==True):return self.select_temperature_indexes(self.model.get_indexes_for_city_in_time_period(address,start_time, finish_time))
        return self.select_temperature_indexes(self.model.get_indexes_for_country_in_time_period(address,start_time, finish_time))

    def get_wind_indexes(self,flag,address,start_time, finish_time):
        if(flag==True):return self.select_wind_indexes(self.model.get_indexes_for_city_in_time_period(address,start_time, finish_time))
        return self.select_wind_indexes(self.model.get_indexes_for_country_in_time_period(address,start_time, finish_time))

    def get_rh_and_p_indexes(self,flag,address,start_time, finish_time):
        if(flag==True):return self.select_rh_and_p_indexes(self.model.get_indexes_for_city_in_time_period(address,start_time, finish_time))
        return self.select_rh_and_p_indexes(self.model.get_indexes_for_country_in_time_period(address,start_time, finish_time))

    def select_temperature_indexes(self,index_city):
        index_list=pd.DataFrame({'date':[row.date.index_date.date() for row in index_city],
                                 'mint':[(row.mint - 32) / 1.8 for row in index_city],
                                 'maxt':[(row.maxt- 32) / 1.8 for row in index_city],
                                 'dew point':[(row.dew_point- 32) / 1.8 for row in index_city],
                                 'avg':[((row.maxt+row.mint) / 2-32) / 1.8 for row in index_city]})
        index_list =index_list.groupby(['date']).mean()
        index_list['rounding avg temperature']=[round(float(row)) for row in index_list.avg]
        return index_list

    def select_wind_indexes(self,index_city):
        index_list=pd.DataFrame({'date':[row.date.index_date.date() for row in index_city],
                                'wind speed':[row.wind_speed for row in index_city],
                                'wind direction':[row.wind_direction for row in index_city]})
        index_list =index_list.groupby(['date']).mean()
        index_list['rounding avg wind speed']=[round(float(row)) for row in index_list['wind speed']]
        return index_list

    def select_rh_and_p_indexes(self,index_city):
        index_list=pd.DataFrame({'date':[row.date.index_date.date() for row in index_city],
                                'relative humidity':[row.rel_hum for row in index_city],
                                'precipitation':[row.precipitation for row in index_city]})
        index_list =index_list.groupby(['date']).mean()
        index_list['rounding avg relative humidity']=[round(float(row)) for row in index_list['relative humidity']]
        return index_list

    #get indexes plot
    def get_temperature_plot_for_period(self,item,params,flag):
        date=self.select_time_period()
        start_time=datetime(date[0][0],date[0][1],1)
        finish_time=datetime(date[1][0],date[1][1],1)
        index_list=self.get_temperature_indexes(flag,item,start_time, finish_time)
        count_index_value=pd.DataFrame(data=index_list.value_counts('rounding avg temperature'),columns=['count temperature index'])
        count_index_value=count_index_value.sort_index()
        view.print_avr_temp_params(index_list.drop(['rounding avg temperature'],axis=1),count_index_value,
        'Temperature index in {} in time period between {} and {}'.format((params),start_time.strftime('%d/%m/%Y'),finish_time.strftime('%d/%m/%Y')))
        return

    def get_wind_plot_for_period(self,item,params,flag):
        date=self.select_time_period()
        start_time=datetime(date[0][0],date[0][1],1)
        finish_time=datetime(date[1][0],date[1][1],1)
        index_list=self.get_wind_indexes(flag,item,start_time, finish_time)
        count_index_value=pd.DataFrame(data=index_list.value_counts('rounding avg wind speed'),columns=['count wind speed index'])
        count_index_value=count_index_value.sort_index()
        view.print_delta_temp(index_list.drop(['rounding avg wind speed'],axis=1),count_index_value,'Wind index in {} in time period between '
        '{} and {}'.format(params,start_time.strftime('%d/%m/%Y'),finish_time.strftime('%d/%m/%Y')),'Degrees')
        return

    def get_rh_and_p_plot_for_period(self,item,params,flag):
        date=self.select_time_period()
        start_time=datetime(date[0][0],date[0][1],1)
        finish_time=datetime(date[1][0],date[1][1],1)
        index_list=self.get_rh_and_p_indexes(flag,item,start_time, finish_time)
        count_index_value=pd.DataFrame(data=index_list.value_counts('rounding avg relative humidity'),columns=['count avg relative humidity'])
        count_index_value=count_index_value.sort_index()
        view.print_delta_temp(index_list.drop(['rounding avg relative humidity'],axis=1),count_index_value,'Auxiliary indexes in {} in time period between '
        '{} and {}'.format(params,start_time.strftime('%d/%m/%Y'),finish_time.strftime('%d/%m/%Y')),'mm')
        return

    #get indexes plot for two items
    def get_temperature_compare_plot_for_period(self,item1,item2,params,flag):
        date=self.select_time_period()
        start_time=datetime(date[0][0],date[0][1],1)
        finish_time=datetime(date[1][0],date[1][1],1)
        index_list=self.get_temperature_indexes(flag,item1,start_time, finish_time)
        index_city_2 = self.get_temperature_indexes(flag,item2,start_time, finish_time)
        index_list['mint2']=index_city_2['mint']
        index_list['maxt2']=index_city_2['maxt']
        index_list['avg2']=index_city_2['avg']
        index_list['delta min temperature']=index_list.apply(lambda row: abs(row.mint - row.mint2) ,axis=1)
        index_list['delta max temperature'] = index_list.apply(lambda row: abs(row.maxt - row.maxt2), axis=1)
        index_list['delta dew point'] = index_list.apply(lambda row: abs(row.avg - row.avg2), axis=1)
        index_list['round delta mint'] = index_list.apply(lambda row: round(float(row['delta min temperature'])), axis=1)
        index_list['round delta maxt'] = index_list.apply(lambda row: round(float(row['delta max temperature'])), axis=1)
        index_list['round delta dewp'] = index_list.apply(lambda row: round(float(row['delta dew point'])), axis=1)
        index_list2=pd.DataFrame({'count delta mint':index_list['round delta mint'].value_counts(),
                                  'count delta maxt':index_list['round delta mint'].value_counts(),
                                  'count delta dewp':index_list['round delta dewp'].value_counts()})
        index_list2=index_list2.sort_index()
        index_list.drop(index_list.iloc[:, 0:8], inplace = True, axis = 1)
        index_list.drop(index_list.iloc[:, 3:6], inplace = True, axis = 1)
        view.print_avr_temp_params(index_list,index_list2,'Delta temperature index between {} in time period between {} and {}'.
        format(params,start_time.strftime('%d/%m/%Y'),finish_time.strftime('%d/%m/%Y')))
        return

    def get_wind_compare_plot_for_period(self,item1,item2,params,flag):
        date=self.select_time_period()
        start_time=datetime(date[0][0],date[0][1],1)
        finish_time=datetime(date[1][0],date[1][1],1)
        index_list=self.get_wind_indexes(flag,item1,start_time, finish_time)
        index_city_2 = self.get_wind_indexes(flag,item2,start_time, finish_time)
        index_list['wind speed2']=index_city_2['wind speed']
        index_list['wind direction2']=index_city_2['wind direction']
        index_list['delta wind speed']=index_list.apply(lambda row: abs(row['wind speed'] - row['wind speed2']) ,axis=1)
        index_list['delta wind direction'] = index_list.apply(lambda row: abs(row['wind direction'] - row['wind direction2']), axis=1)
        index_list['round wind speed'] = index_list.apply(lambda row: round(float(row['delta wind speed'])), axis=1)
        index_list['round wind direction'] = index_list.apply(lambda row: round(float(row['delta wind direction'])), axis=1)
        index_list2=pd.DataFrame({'count delta wind speed':index_list['round wind speed'].value_counts(),
                                'count delta wind direction':index_list['round wind direction'].value_counts()})
        index_list2=index_list2.sort_index()
        index_list.drop(index_list.iloc[:, 0:5], inplace = True, axis = 1)
        index_list.drop(index_list.iloc[:, 2:4], inplace = True, axis = 1)
        view.print_delta_temp(index_list,index_list2,'Delta wind index between {} in time period between {} and {}'.
        format(params,start_time.strftime('%d/%m/%Y'),finish_time.strftime('%d/%m/%Y')),'Degrees')
        return

    def get_rh_and_p_compare_plot_for_period(self,item1,item2,params,flag):
        date=self.select_time_period()
        start_time=datetime(date[0][0],date[0][1],1)
        finish_time=datetime(date[1][0],date[1][1],1)
        index_list=self.get_rh_and_p_indexes(flag,item1,start_time, finish_time)
        index_city_2 = self.get_rh_and_p_indexes(flag,item2,start_time, finish_time)
        index_list['relative humidity2']=index_city_2['relative humidity']
        index_list['precipitation2']=index_city_2['precipitation']
        index_list['delta relative humidity']=index_list.apply(lambda row: abs(row['relative humidity'] - row['relative humidity2']) ,axis=1)
        index_list['delta precipitation'] = index_list.apply(lambda row: abs(row['precipitation'] - row['precipitation2']), axis=1)
        index_list['round relative humidity'] = index_list.apply(lambda row: round(float(row['delta relative humidity'])), axis=1)
        index_list['round precipitation'] = index_list.apply(lambda row: round(float(row['delta precipitation'])), axis=1)
        index_list2=pd.DataFrame({'count delta relative humidity':index_list['round relative humidity'].value_counts(),
                                'count delta precipitation':index_list['round precipitation'].value_counts()})
        index_list2=index_list2.sort_index()
        index_list.drop(index_list.iloc[:, 0:5], inplace = True, axis = 1)
        index_list.drop(index_list.iloc[:, 2:4], inplace = True, axis = 1)
        view.print_delta_temp(index_list,index_list2,'Delta auxiliary indexes between {} in time period between {} and {}'.
        format(params,start_time.strftime('%d/%m/%Y'),finish_time.strftime('%d/%m/%Y')),'mm')
        return

    #make prognoze
    def make_approximate_indexes(self):
        country=self.select_country()
        if(country!=False and country!=None):
            date=self.select_time_period()
            start_time=datetime(date[0][0],date[0][1],1)
            finish_time=datetime(date[1][0],date[1][1],1)
            index_list=self.get_temperature_indexes(False,country.country_code,start_time, finish_time)
            delta = timedelta((finish_time-start_time).days)
            index_list['mint'] = index_list.apply(lambda row: (row['mint']/2 + random.uniform(0, (row['mint']/2))), axis=1)
            index_list['maxt'] = index_list.apply(lambda row: (row['maxt']/2 + random.uniform(0, (row['maxt']/2))), axis=1)
            index_list['dew point'] = index_list.apply(lambda row: (row['dew point']/2 + random.uniform(0, (row['dew point']/2))), axis=1)
            index_list['avg'] = index_list.apply(lambda row: (row['mint']+row['maxt'])/2, axis=1)
            view.print_approximate_indexes(index_list.drop(['rounding avg temperature'],axis=1),
            "Approximate indexes for {} in next year based the enter data ({}->{})".format(country.country,datetime(datetime.today().year+1,date[0][1],1),datetime(datetime.today().year+1,date[0][1],1)+delta))
        return

    #backup restore
    def restore(self):
        os.chdir(r'D:\course\\backups\\')
        file_list=glob.glob('*.dump')
        file_list.append('close this window')
        files=pd.DataFrame(file_list,columns=['filename'])
        while 1:
            try:
                print(files)
                index_file=int(input('Enter file index: ').strip())
                if(index_file==len(file_list)-1):return
                if(index_file>=0 and index_file<len(file_list)):
                    os.system(f"""C:\\"Program Files"\PostgreSQL\\11\\bin\psql.exe -h 192.168.1.113 -U postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where datname=\'course\'""")
                    os.system(f"""C:\\"Program Files"\PostgreSQL\\11\\bin\psql.exe -h 192.168.1.113 -U postgres -c "DROP DATABASE IF EXISTS \"course\"""")
                    os.system(f"""C:\\"Program Files"\PostgreSQL\\11\\bin\psql.exe -h 192.168.1.113 -U postgres  -c "CREATE DATABASE \"course\"""")
                    start_time = time()
                    if(os.system(f"""C:\\"Program Files"\PostgreSQL\\11\\bin\psql.exe -h 192.168.1.113 -U postgres course < D:\course\\backups\\{files.loc[index_file,'filename']}""")==0):
                        print("Successful restore!, spend time:  {} seconds".format(time()-start_time))
                    else:print("You have problem with restore!")
                    return
                else:print('\nThis value is not included in the possible values, try again')
            except Exception as s:print('\nSorry but you enter incorect format date',s)

    def backup(self):
        today = datetime.today()
        name_of_file = ''
        try:
            name_of_file = input("Enter name file: ").strip()
        except:name_of_file='default'
        completeName = "{}_{}".format(name_of_file, today.strftime('%Y_%m_%d_%H_%M_%S'))
        start_time =time()
        backup_str = f"""C:\\"Program Files"\PostgreSQL\\11\\bin\pg_dump.exe -h 192.168.1.107 -U postgres course > D:\course\\backups\\{completeName}.dump"""
        if(os.system(backup_str)==0):
            print("Successful backup! File name {} \nspend time: {} seconds".format(completeName,time()-start_time))
        else:print("You have problem with backup!")
        return

    #menu function
    def main_manu(self):
        while 1:
            try:
                view.print_main_menu()
                command=int(input('Enter command: '))
                if(command == 1):self.city_function_menu()
                elif(command == 2):self.country_function_menu()
                elif(command == 3):self.compare_city_function_menu()
                elif(command == 4):self.compare_country_function_menu()
                elif(command == 5 and self.connect_flag==True):self.enter_info()
                elif(command == 6):self.make_approximate_indexes()
                elif(command == 7 and self.connect_flag==True):self.backup()
                elif(command == 8 and self.connect_flag==True):self.restore()
                elif (command == 9):
                    self.model.close()
                    self.connect_flag =self.model.connect()
                elif(command ==10):return
            except Exception as s: print('You enter incorect format input data, try again.',s)

    def city_function_menu(self):
        city=self.select_city()
        while 1:
            if(city!=False and city!={}):
                try:
                    view.print_city_menu()
                    command=int(input('Enter command: '))
                    if(command==1):self.get_temperature_plot_for_period(city.address_id,'{} {}'.format(city.city,city.country.country),True)
                    elif(command==2):self.get_wind_plot_for_period(city.address_id,'{} {}'.format(city.city,city.country.country),True)
                    elif(command==3):self.get_rh_and_p_plot_for_period(city.address_id,'{} {}'.format(city.city,city.country.country),True)
                    elif(command==4):return
                except Exception as s: print('You enter incorect format input data, try again.',s)
            else: return

    def country_function_menu(self):
        country=self.select_country()
        while 1:
            if(country!=False and country!={}):
                try:
                    view.print_country_menu()
                    command=int(input('Enter command: '))
                    if(command==1):self.get_temperature_plot_for_period(country.country_code,'{} {}'.format(country.country,country.country_code),False)
                    elif(command==2):self.get_wind_plot_for_period(country.country_code,'{} {}'.format(country.country,country.country_code),False)
                    elif(command==3):self.get_rh_and_p_plot_for_period(country.country_code,'{} {}'.format(country.country,country.country_code),False)
                    elif(command==4):return
                except Exception as e: print('You enter incorect format input data, try again.',e)
            else: return

    def compare_country_function_menu(self):
        view.print_border('Select first country')
        country1=self.select_country()
        if(country1!=False and country1!={}):
            view.print_border('Select second country')
            country2=self.select_country()
            if(country2!=False and country2!={}):
                while 1:
                    try:
                        view.print_country_function_menu()
                        command=int(input('Enter command: '))
                        if(command==1):self.get_temperature_compare_plot_for_period(country1.country_code,country2.country_code,'{} and {}'.format(country1.country,country2.country),False)
                        elif(command==2):self.get_wind_compare_plot_for_period(country1.country_code,country2.country_code,'{} and {}'.format(country1.country,country2.country),False)
                        elif(command==3):self.get_rh_and_p_compare_plot_for_period(country1.country_code,country2.country_code,'{} and {}'.format(country1.country,country2.country),False)
                        elif(command==4):return
                    except Exception as s: print('You enter incorect format input data, try again.',s)
            else:return
        else:return

    def compare_city_function_menu(self):
        view.print_border('Select first city')
        city_1=self.select_city()
        if(city_1!=False and city_1!=None):
            view.print_border('Select second city')
            city_2=self.select_city()
            if(city_2!=False and city_2!=None):
                while 1:
                    try:
                        view.print_city_function_menu()
                        command=int(input('Enter command: '))
                        if(command==1):self.get_temperature_compare_plot_for_period(city_1.address_id,city_2.address_id,'{} and {}'.format(city_1.city,city_2.city),True)
                        elif(command==2):self.get_wind_compare_plot_for_period(city_1.address_id,city_2.address_id,'{} and {}'.format(city_1.city,city_2.city),True)
                        elif(command==3):self.get_rh_and_p_compare_plot_for_period(city_1.address_id,city_2.address_id,'{} and {}'.format(city_1.city,city_2.city),True)
                        elif(command==4):return
                    except:print('You enter incorect format input data, try again.')