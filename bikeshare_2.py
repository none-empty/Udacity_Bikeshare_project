import time
import pandas as pd
import numpy as np
import calendar as cal
 
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS= list(map(lambda month:month.lower(),cal.month_name[1:]))  + ['all']
DAYS=list(map(lambda day:day.lower(),cal.day_name))+['all']

# validate a filter parameter
# the parameters are : city,month and day
def validate_input(input_type,valid_group):
    input_data=input(f'enter the {input_type} \n').lower().strip()
    
    while input_data not in valid_group:
        input_data=input(f'invalid {input_type} , please enter a valid {input_type} \n').lower().strip()
    return input_data

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    user_city=validate_input('city',list(CITY_DATA.keys()))
    # get user input for month (all, january, february, ... , june)
    user_month=validate_input('month',MONTHS)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    user_day=validate_input('day',DAYS)

    print('-'*40)
    return [user_city, user_month, user_day]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    data=pd.read_csv(CITY_DATA[city])  
    data['Start Time']=pd.to_datetime(data['Start Time'])
    df=data[( (data['Start Time'].dt.month_name().str.lower() ==month) | (month=='all') ) & 
            ((data['Start Time'].dt.day_name().str.lower() ==day) | (day=='all'))]
    
    return df


def time_stats(df:pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month=df.groupby(df['Start Time'].dt.month_name().str.lower())['Start Time'].count().idxmax()
    
    print(f'the most common month for travel is {common_month} ')
    # display the most common day of week
    common_day=df.groupby(df['Start Time'].dt.day_name().str.lower())['Start Time'].count().idxmax()
    print(f'the most common day of the week for travel is {common_day} ')

    # display the most common start hour
    common_hour=df.groupby(df['Start Time'].dt.hour)['Start Time'].count().idxmax()
    print(f'the most common hour to start travel is  {common_hour} ')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# a helper method for station_stats method only
def most_common(coloumns:list,df:pd.DataFrame):
    most=df.groupby(coloumns)[coloumns[0]].count().idxmax()
    if len(coloumns)==1:
        print(f'The most common {coloumns[0]} is {most}')
    else:
        response=f'''The most frequent combination of {', '.join(coloumns)} are : 
         {most}'''
        print(response)

def station_stats(df:pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common(['Start Station'],df)
    
    # display most commonly used end station
    most_common(['End Station'],df)

    # display most frequent combination of start station and end station trip
    most_common(['Start Station','End Station'],df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    avg=df['Trip Duration'].sum()
    print(f'average travel time = {avg}')
    # display mean travel time
    mn=df['Trip Duration'].mean()
    print(f'the mean = {mn}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df:pd.DataFrame,city:str):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types_counts=df.groupby('User Type').size().reset_index(name='Count')
    
    print(user_types_counts)
    print('\n' + (10*'-'))
    # Display counts of gender
    if city.lower()=='washington':return
    gender_count=df.groupby('Gender').size().reset_index(name='Count')
    print(gender_count)
    print('\n' + (10*'-'))
    # Display earliest, most recent, and most common year of birth
    earliest_year_of_birth=df['Birth Year'].min()
    print(f'The earliest year of birth is {int(earliest_year_of_birth)}')
    most_recent_year_of_birth=df['Birth Year'].max()
    print(f'The most recent year of birth is {int(most_recent_year_of_birth)}')
    most_common_year_of_birth=df.groupby('Birth Year')['Birth Year'].count().idxmax()
    print(f'The most common year of birth is {int(most_common_year_of_birth)}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def validate_yes_no_question(value,initial_message:str):
    if initial_message != None:
        value=input(initial_message).lower()

    while value not in ['yes','no']:
       value=input('invalid value, please enter yes or no..\n').lower()
    return value

def display_row_data(df:pd.DataFrame):
    size,start,display=len(df),0,None
    display=validate_yes_no_question(display,'Would you like to see the data ?\n')

    while display=='yes':
        if start+5 >=size:
            print('No more data to display\n')
            break

        print(df.iloc[start:start+5]) 
        start+=5
        display=validate_yes_no_question(display,'Would you like to continue ?\n')
        
    
def main():
    
    while True:
         
        print('available data on cities :'+ ', '.join(list(CITY_DATA.keys())) )
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # if no data matches the specified criteria then don't perform any operation
        if df.empty:
            print('No data available')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            display_row_data(df)

        restart=None
        restart = validate_yes_no_question(restart,'\nWould you like to restart? Enter yes or no.\n')

        if restart=='no':
            break
        
        



if __name__ == "__main__":
	main()
