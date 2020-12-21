import matplotlib.pyplot as plt

class View:
    @staticmethod
    def print_delta_temp(index,index2,name,title):
        index.plot(rot=0,colormap='jet',subplots=True,grid=True)
        plt.suptitle(name)
        plt.ylabel(title)
        plt.xticks(fontsize=8)
        plt.xticks(rotation=60)
        index2.plot.bar(rot=0,colormap='jet',subplots=True,grid=True,legend=None)
        plt.show()

    @staticmethod
    def print_avr_temp_params(index1,index2,title):
        index1.plot(rot=0,colormap='jet',grid=True)
        plt.title(title)
        plt.ylabel('Celsius')
        plt.xticks(fontsize=8)
        plt.xticks(rotation=60)
        index2.plot.bar(rot=0,colormap='jet',subplots=True,grid=True,legend=None)
        plt.show()
    
    @staticmethod
    def print_approximate_indexes(index,title):
        index.plot(figsize=(10, 10), subplots=True, sharex=True,grid=True,alpha=.7)
        plt.suptitle(title)
        plt.xlabel('old date')
        plt.xticks(fontsize=8)
        plt.xticks(rotation=60)
        plt.show()    

    @staticmethod
    def print_border(text):
        print("-------------------------------------------------------\n{}\n"
        "-------------------------------------------------------\n".format(text))

    @staticmethod
    def print_main_menu():
        View.print_border("1) Work with some city\n2) Work with some country\n3) Compare some city\n4) Compare some country\n"
        "5) Chenge info\n6) Make prognoze indexes\n7) Make database backup\n8) Restore database\n9) Reconnect\n10) Exit")

    @staticmethod
    def print_city_menu():
        View.print_border("1) Get temperature plot by period\n2) Get wind plot by period\n"
        "3) Get relative humidity and precipitation by period\n4) Exit")
    
    @staticmethod
    def print_country_menu():
        View.print_border("1) Get temperature plot by period\n2) Get wind plot by period\n"
        "3) Get relative humidity and precipitation by period\n4) Exit")

    @staticmethod
    def print_country_function_menu():
        View.print_border("1) Get compare temperature plot by period\n2) Get compare wind plot by period\n"
        "3) Get compare relative humidity and precipitation by period\n4) Exit")
    
    @staticmethod
    def print_city_function_menu():
        View.print_border("1) Get compare temperature plot by period\n2) Get compare wind plot by period\n"
        "3) Get compare relative humidity and precipitation by period\n4) Exit")
    
    @staticmethod
    def print_select_city_command():
        View.print_border("1) Select city by name and country_code\n2) View all location\n3) Confirm city\n4) Exit")
    
    @staticmethod
    def print_select_country_command():
        View.print_border("1) Select country by country_code\n2) View all location\n3) Confirm country\n4) Exit")