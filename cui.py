#menu function
from controller import Controller
from view import View as view
cont=Controller()   

def main_manu():
    while 1:
        try: 
            view.print_main_menu()
            command=int(input('Enter command: '))
            if(command==1):city_function_menu()
            elif(command==2):country_function_menu()
            elif(command==3):compare_city_function_menu()
            elif(command==4):compare_country_function_menu()
            elif(command==5):cont.enter_info()
            elif(command==6):cont.make_approximate_indexes()
            elif(command==7):cont.backup()
            elif(command==8):cont.sef.restore()
            elif(command==9):return 
        except Exception as s: print('You enter incorect format input data, try again.',s)

def city_function_menu():
    city=cont.select_city()
    while 1:
        if(city!=False and city!={}):
            try:
                view.print_city_menu()
                command=int(input('Enter command: '))
                if(command==1):cont.get_temperature_plot_for_period(city.address_id,'{}{}'.format(city.city,city.country.country),True)
                elif(command==2):cont.get_wind_plot_for_period(city.address_id,'{}{}'.format(city.city,city.country.country),True)
                elif(command==3):cont.get_rh_and_p_plot_for_period(city.address_id,'{}{}'.format(city.city,city.country.country),True)
                elif(command==4):return 
            except Exception as s: print('You enter incorect format input data, try again.',s)
        else: return

def country_function_menu():
    country=cont.select_country()
    while 1:
        if(country!=False and country!={}):
            try:
                view.print_country_menu()
                command=int(input('Enter command: '))
                if(command==1):cont.get_temperature_plot_for_period(country.country_code,'{} {}'.format(country.country,country.country_code),False)
                elif(command==2):cont.get_wind_plot_for_period(country.country_code,'{} {}'.format(country.country,country.country_code),False)
                elif(command==3):cont.get_rh_and_p_plot_for_period(country.country_code,'{} {}'.format(country.country,country.country_code),False)
                elif(command==4):return 
            except Exception as e: print('You enter incorect format input data, try again.',e)
        else: return

def compare_country_function_menu():
    view.print_border('Select first country')
    country1=cont.select_country()
    if(country1!=False and country1!={}):
        view.print_border('Select second country')
        country2=cont.select_country()
        if(country2!=False and country2!={}):
            while 1:
                try:
                    view.print_country_function_menu()
                    command=int(input('Enter command: '))
                    if(command==1):cont.get_temperature_compare_plot_for_period(country1.country_code,country2.country_code,'{} and {}'.format(country1.country,country2.country),False)
                    elif(command==2):cont.get_wind_compare_plot_for_period(country1.country_code,country2.country_code,'{} and {}'.format(country1.country,country2.country),False)
                    elif(command==3):cont.get_rh_and_p_compare_plot_for_period(country1.country_code,country2.country_code,'{} and {}'.format(country1.country,country2.country),False)
                    elif(command==4):return 
                except Exception as s: print('You enter incorect format input data, try again.',s)
        else:return
    else:return

def compare_city_function_menu():
    view.print_border('Select first city')
    city_1=cont.select_city()
    if(city_1!=False and city_1!=None):
        view.print_border('Select second city')
        city_2=cont.select_city()
        if(city_2!=False and city_2!=None):
            while 1:
                try:
                    view.print_city_function_menu()
                    command=int(input('Enter command: '))
                    if(command==1):cont.get_temperature_compare_plot_for_period(city_1.address_id,city_2.address_id,'{} and {}'.format(city_1.city,city_2.city),True)
                    elif(command==2):cont.get_wind_compare_plot_for_period(city_1.address_id,city_2.address_id,'{} and {}'.format(city_1.city,city_2.city),True)
                    elif(command==3):cont.get_rh_and_p_compare_plot_for_period(city_1.address_id,city_2.address_id,'{} and {}'.format(city_1.city,city_2.city),True)
                    elif(command==4):return 
                except:print('You enter incorect format input data, try again.')