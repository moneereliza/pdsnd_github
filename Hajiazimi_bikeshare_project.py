# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 15:18:41 2023

@author: Moneer Hajiazimi
"""

import time
import pandas as pd

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("\nWhich of the following cities would you like to view data for? New York City, Chicago or Washington?\n").lower()
    while city not in ('new york city', 'chicago', 'washington'):
        city = input("\nSorry, I don't recognize that input, please try again.\n").lower()

    # get user input for month (all, january, february, ... , june)

    month = input("\nWould you like to apply a month filter? If yes, enter one of the following: Jan, Feb, Mar, Apr, May, June, or type 'all' if you do not have any preference?\n").lower()
    while month not in ('jan', 'feb', 'mar', 'apr', 'may', 'june', 'all'):
        month = input("\nSorry, I don't recognize that input, please try again.\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("\nWould you like to apply a day filter? If yes, enter one of the following: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n").lower()
    while day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        day = input("\nSorry, I don't recognize that input, please try again.\n").lower()

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

    # load csv data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new columns to separate out month and day of week from 'Start Time' column

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Returns print statements for most commom day, month, and 
    start hour for trips."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is:', common_month)

    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print('The most common day is:', common_day)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
     Returns print statements for most commom start station, end
     station, and combined start/end station for trips. """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('\nThe most commonly used start station is:', Start_Station)


    # display most commonly used end station

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nThe most commonly used end station is:', End_Station)


    # display most frequent combination of start station and end station trip

    Combined_Station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nThe most commonly used combination of the start and end station of trips is:\n', Combined_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    Total_Travel_Time = sum(df['Trip Duration'])
    print('\nThe total travel time is:', Total_Travel_Time/86400, " days")


    # display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    print('\nThe average travel time is:', Mean_Travel_Time/60, " minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth

    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo data available for this month.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nNo data available for this month.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays the data 5 rows per press"""
    ask_data = input('Press the enter key to view the data 5 rows at a time, otherwise type "No"\n').lower()
    row = 0
    while ask_data!='no':
        print(df.iloc[row:row + 5])
        row += 5
        ask_again = input('Press the enter key to continue, otherwise type "No".\n ')
        if (ask_again == "no"):
            print('Done!')
            break

def main(): 
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
