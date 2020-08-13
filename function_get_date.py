# REDACTED
# REDACTED
# May 2019


from pandas.tseries.offsets import BDay
import pandas as pd
import datetime as dt
import time

def get_date_function(default_initial_date, default_final_date):
    # Variables
    previous_bday = pd.datetime.today() - BDay(1)
    earliest_date = dt.datetime(2015, 8, 8)     # Earliest date with
    initial_date = default_initial_date         # data available
    final_date = default_final_date


    # Lists for understanding user input
    affirmation_list = ['Y', 'y', 'Yes', 'YES', 'yes']
    negation_list = ['N', 'n', 'No', 'NO', 'no']
    valid_answers = ['Y', 'y', 'Yes', 'YES', 'yes',
                     'N', 'n', 'No', 'NO', 'no']


    '''
    ###################
    ## REQUEST INPUT ##
    ###################
    '''
    def input_date():
        date_is_valid = False
        new_date = ""
        while not date_is_valid:
            new_date = input("Remember to use d/m/yy format:")
            try:
                # strptime will return an error if the input is incorrect
                new_date = dt.datetime.strptime(new_date, "%d/%m/%y")
                date_is_valid = True
            except ValueError:
                print("There seems to be an error!")
        return new_date


    '''
    ######################################
    ## ASK FOR CHANGES FOR INITIAL DATE ##
    ######################################
    '''
    print("The default initial date is " +
          str(dt.datetime.strftime(initial_date, "%d/%m/%y")))
    time.sleep(0.75)
    print("Would you like to change it? (Enter Y/N)")
    change_date = input()


    '''
    ###########################################
    ## CHECK INPUT VALIDITY FOR INITIAL DATE ##
    ###########################################
    '''
    while change_date not in valid_answers:     # Checks if input is valid
        change_date = input("I didn't understand that. "
                            "Would you like to change it? (Enter Y/N)")

    if change_date in affirmation_list:         # Conditionals to change date
        print("Enter the new initial date.")    # and check for date validity
        initial_date = input_date()
        while initial_date < earliest_date:
            print("Invalid date. Initial date can't be earlier than "
                  "8/8/15. There's not enough data before this date. "
                  "Try again")
            initial_date = input_date()
            if initial_date >= earliest_date:
                break
        print("The new initial date is: " +
              initial_date.strftime('%d/%m/%y'))
    elif change_date in negation_list:
        print("OK. The initial date will remain as " +
              initial_date.strftime('%d/%m/%y'))


    '''
    ####################################
    ## ASK FOR CHANGES FOR FINAL DATE ##
    ####################################
    '''
    time.sleep(0.75)
    print("The default final date is " +
          str(dt.datetime.strftime(final_date, "%d/%m/%y")))
    time.sleep(0.75)
    print("Would you like to change it? (Enter Y/N)")
    change_date = input()


    '''
    #########################################
    ## CHECK INPUT VALIDITY FOR FINAL DATE ##
    #########################################
    '''
    while change_date not in valid_answers:     # Checks if input is valid
        change_date = input("I didn't understand that. "
                            "Would you like to change it? (Enter Y/N)")

    if change_date in affirmation_list:         # Conditionals to change date
        print("Enter the new final date.")      # and check for date validity
        final_date = input_date()
        while final_date > previous_bday:
            print("Invalid date. The latest final date can only be the "
                  "previous business day.")
            print("Remember the initial date is " +
                  initial_date.strftime('%d/%m/%y') + ". Try again.")
            final_date = input_date()
            if final_date == previous_bday:
                break
        while final_date <= initial_date:
            print("Invalid date. The final date can't be equal or less "
                  "than the initial date")
            print("Remember the initial date is " +
                  initial_date.strftime('%d/%m/%y') + ". Try again.")
            final_date = input_date()
            if final_date > initial_date:
                break
        print("The new final date is: " + final_date.strftime('%d/%m/%y'))
    else:
        print("OK. The final date will remain as " +
              final_date.strftime('%d/%m/%y'))

    return initial_date, final_date
