import sys
from classes import AppManager

def run_app():

    app = AppManager()

    print(app.menu)
    user_input = input('Enter an option: ')
    try:
        if int(user_input) == 1:
            app.show_top10_imdb()
        elif int(user_input) == 2:
            app.show_top10_rotten_tomatoes()
        elif int(user_input) == 3:
            app.show_random_movie()
        elif int(user_input) == 4:
            app.show_random_movie('imdb')
        elif int(user_input) == 5:
            app.show_random_movie('rt')
        
        
        elif int(user_input) == 8:
            sys.exit()
    except ValueError as e:
        print('Invalid input, enter a number')
        
if __name__ == '__main__':
    while True:
        run_app()