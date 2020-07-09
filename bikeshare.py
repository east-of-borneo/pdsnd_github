import time
import pandas as pd
import numpy as np

#global constants
CHICARGO = "chicago.csv"
WASHINGTON = "washington.csv"
NEW_YORK_CITY = "new_york_city.csv"

CITY_DATA = { 'chicago': CHICARGO,
              'new york city': WASHINGTON,
              'washington': NEW_YORK_CITY }

def get_filters():
    
    cities = {"1" : "chicago", '2' : "washington", '3' : "new york city"}
    months = {'1' : "january", '2' : "february", '3' : "march", '4' : "april",  '5' : "may", '6' : "jun", '7' : "all"}
    days = {'1' : "Monday", '2' : "Tuesday", '3' : "Wednesday",'4' : "Thursday", '5' : "Friday", '6' : "Saturday", '7' : "Sunday", '8' : "all"}
                
    def choose_from_list(value_list, parameter):
        status = True
        while status:
            print("Please enter the", parameter, "you would like to explore")
            for key in value_list:
                print(key, value_list[key])
            value = input("Enter valid number:")
            value = value_list.get(value, 0)
            if value != 0:
                status = False
            else:
                print("invalid", parameter)
        return value
    print('Hello! Let\'s explore some US bikeshare data!')

    city = choose_from_list(cities, "city")
    month = choose_from_list(months, "month")
    day = choose_from_list(days, "day")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = {'january' : 1, 'february' : 2, 'march' : 3, 'april' : 4, 'may' : 5, 'june' : 6}
        month = months[month]

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = {'1' : "january", '2' : "february", '3' : "march", '4' : "april",  '5' : "may", '6' : "june", '7' : "all"}
    common_month = df['month'].mode()[0]
    print('The most popular month to travel is:',months[str(common_month)].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most popular day to travel is:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most popular hour to travel is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most popular starting station is:', common_start)
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most popular ending station is:', common_end)

    # display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['start_end'].mode()[0]
    print('The most popular trip is:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total trip duration is:', total_travel_time, " seconds")
    print('This is equal to:', format((total_travel_time/3600), '.2f'), " hours")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean trip duration is:', format((mean_travel_time), '.2f'), " seconds")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('counts by user types:')
    print(user_type_count)
    print()
    # Display counts of gender

    if 'Gender' in df:
        print('counts by genders:')
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print('gender information not available')

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        min_dob = df['Birth Year'].min()
        print('\nThe earliest year of birth is:', int(min_dob))
        max_dob = df['Birth Year'].max()
        print('The most recent year of birth is:', int(max_dob))
        mode_dob = df['Birth Year'].mode()[0]
        print('The most common year of birth is:', int(mode_dob))
    else: 
        print('Birth Year information not available')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_data(df):
    status = True
    while status:
        num = 1
        cont = input('would you like to see raw data? (y/n):')
        if 'y' in cont.lower():
            status = True
            print(df.iloc[(num):(num+5)])
            num += 5
        else:
            status = False
        print
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        print_data(df)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()