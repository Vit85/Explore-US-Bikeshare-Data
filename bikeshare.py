import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to explore data for Chicago, New York City or Washington?\n").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("\nSorry, invalid input! Please enter a valid input: ['Chicago', 'New York City', 'Washington']")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month you would like to explore: January, February, March, April, May, June or All?\n").lower()
        if month in['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("\nSorry, invalid input! Please enter a valid input: ['January', 'February', 'March', 'April', 'May', 'June', 'All']")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day you would like to explore: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("\nSorry, invalid input! Please enter a valid input: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']")

    print("-"*45)
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
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(arg = df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    print("The most common month is:", df['Month'].value_counts().idxmax())
    print("The count is            :", df['Month'].value_counts().max())

    # display the most common day of week
    print("The most common day is  :", df['Day'].value_counts().idxmax())
    print("The count is            :", df['Day'].value_counts().max())

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print("The most common hour is :", df['Hour'].value_counts().idxmax())
    print("The count is            :", df['Hour'].value_counts().max())

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print("-"*45)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station is:", df['Start Station'].value_counts().idxmax())
    print("The count is                       :", df['Start Station'].value_counts().max())

    # display most commonly used end station
    print("Most commonly used end station is  :", df['End Station'].value_counts().idxmax())
    print("The count is                       :", df['End Station'].value_counts().max())

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + " ---> " + df['End Station']
    print("Most frequently combination of start station and end station trip is:\n",
          df['Start End Station'].value_counts().idxmax())
    print("The count is                       :",
          df['Start End Station'].value_counts().max())

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print("-"*45)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("Total travel time: ", round(df['Trip Duration'].sum()/3600, 2), " hours")

    # display mean travel time
    print("Mean travel time : ", round(df['Trip Duration'].mean()/60, 2), " minutes")

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print("-"*45)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    
    if 'Subscriber' in user_types:
        print("Count of user type       : Subscriber", user_types['Subscriber'])
    if 'Customer' in user_types:
        print("Count of user type       : Customer  ", user_types['Customer'])
    if 'Dependent' in user_types:
        print("Count of user type       : Dependent ", user_types['Dependent'])

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        if 'Male' in gender_count:
            print("Count of Gender          : Male  ", gender_count['Male'])
        if 'Female' in gender_count:
            print("Count of Gender          : Female", gender_count['Female'])
    else:
        print("There is no gender information for this city!")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest year of birth   :", int(df['Birth Year'].min()))
        print("Most recent year of birth:", int(df['Birth Year'].max()))
        print("Most common year of birth:", int(df['Birth Year'].value_counts().idxmax()))
    else:
        print("There is no birth year information for this city!")

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print("-"*45)

def display_raw_data(df):
    """Asks if the user would like to see some raw data from the filtered dataset."""

    line_count = 0
    user_input = input("Would you like to see some raw data from the filtered dataset? Enter yes or no!\n").lower()

    while True:
        if user_input == 'yes' and line_count+5 < df.shape[0]:
            print(df.iloc[line_count : line_count + 5])
            line_count += 5
            user_input = input("Would you like to display 5 more rows of raw data?? Enter yes or no!\n").lower()
        else:
            break

    print("-"*45)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()