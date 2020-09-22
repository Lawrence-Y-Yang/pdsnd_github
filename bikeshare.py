import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_list = ['chicago', 'new york city', 'washington']
month_list = ['all','january','february','march','april','may','june']
day_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Please select a city name from Chicago, New York City, or Washington: ')
    while city.lower() not in city_list:
        print ('Please enter a correct city name!\n')
        city = input('Please select a city name from Chicago, New York City, or Washington: ')
    # TO DO: get user input for month (all, january, february, ... , june)
    print('\n You selected {} to explore.\n'.format(city))
    month = input('Please choose a month name from january to june, or simply choose all: ')
    while month.lower() not in month_list:
        print ('Please enter a correct month name!\n')
        month = input('Please choose a month name from January to June, or simply choose all: ')
    print('\n Your month selection is', month, '.\n')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please choose a day of week from Monday to Sunday, or simply choose all: ')
    while day.lower() not in day_list:
        print ('Please enter a correct day name!\n')
        day = input('Please choose a day of week, from Monday to Sunday, or simply choose all: ')
    print('\n Your day of week selection is {}. \n'.format(day))
    print('-'*40)
    return city, month, day


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
    # Load relevant city csv file
    #convert the Start Time column to datetime
    city = city.lower()
    month = month.lower()
    day = day.lower()
    df = pd.read_csv(CITY_DATA[city])
    df['city'] = city
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #extract month, day of week, and hour from the Start Time Column
    # create new month, day_of_week, and hour columns with extracted data
    df['month']= df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']==month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is:', common_month)
    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is:', common_day_of_week)
    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is {}.'.format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print ('The most commonly used start station is {}.'.format(common_start_station))
    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print ('The most commonly used end station is {}.'.format(common_end_station))
    # TO DO: display most frequent combination of start station and end station trip
    #df['combination'] = df['Start Station'] + df['End Station']
    #most_frequent_combination = df['combination'].mode()[0]
    most_frequent = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print ('The most frequent combination of start and end station is {}.'.format(most_frequent))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print ('The total travel time is', total_travel_time/60, 'minutes')
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print ('The mean travel time is', mean_travel_time/60, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\n Counts of user types are displayed below. \n')
    print (user_types)

    # TO DO: Display counts of gender (Not available in the Washington file)
    if 'gender' in df.columns:
        print('\nThe gender count information is below\n')
        gender_display = df['Gender'].value_counts()


    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print ('\n The earliest year of birth is', earliest_birth_year, '\n')
        print ('\n The most recent year of birth is', most_recent_birth_year, '\n')
        print ('\n The most common year of birth is', most_common_birth_year, '\n')
    else:
        print ('Sorry, the gender and year of birth information is not available.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data = input('\n Would you like to see the first five rows of the raw data?\n Answer yes or no \n').lower()
        if raw_data == 'yes':
            i = 0
            while True:
                print (df.iloc[i:i+5])
                i += 5
                additional_data = input ('\n Do you want to see five more rows of data?  Answer yes or no \n').lower()
                if additional_data != 'yes':
                    break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
