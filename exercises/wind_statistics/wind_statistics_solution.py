"""
Wind Statistics
----------------

Topics: Using array methods over different axes, fancy indexing.

1. The data in 'wind.data' has the following format::

        61  1  1 15.04 14.96 13.17  9.29 13.96  9.87 13.67 10.25 10.83 12.58 18.50 15.04
        61  1  2 14.71 16.88 10.83  6.50 12.62  7.67 11.50 10.04  9.79  9.67 17.54 13.83
        61  1  3 18.50 16.88 12.33 10.13 11.17  6.17 11.25  8.04  8.50  7.67 12.75 12.71

   The first three columns are year, month and day.  The
   remaining 12 columns are average windspeeds in knots at 12
   locations in Ireland on that day.

   Use the 'loadtxt' function from numpy to read the data into
   an array.

2. Calculate the min, max and mean windspeeds and standard deviation of the
   windspeeds over all the locations and all the times (a single set of numbers
   for the entire dataset).

3. Calculate the min, max and mean windspeeds and standard deviations of the
   windspeeds at each location over all the days (a different set of numbers
   for each location)

4. Calculate the min, max and mean windspeed and standard deviations of the
   windspeeds across all the locations at each day (a different set of numbers
   for each day)

5. Find the location which has the greatest windspeed on each day (an integer
   column number for each day).

6. Find the year, month and day on which the greatest windspeed was recorded.

7. Find the average windspeed in January for each location.

You should be able to perform all of these operations without using a for
loop or other looping construct.

Bonus
~~~~~

1. Calculate the mean windspeed for each month in the dataset.  Treat
   January 1961 and January 1962 as *different* months.

2. Calculate the min, max and mean windspeeds and standard deviations of the
   windspeeds across all locations for each week (assume that the first week
   starts on January 1 1961) for the first 52 weeks.

Bonus Bonus
~~~~~~~~~~~

Calculate the mean windspeed for each month without using a for loop.
(Hint: look at `searchsorted` and `add.reduceat`.)

Notes
~~~~~

These data were analyzed in detail in the following article:

   Haslett, J. and Raftery, A. E. (1989). Space-time Modelling with
   Long-memory Dependence: Assessing Ireland's Wind Power Resource
   (with Discussion). Applied Statistics 38, 1-50.

"""
from __future__ import print_function
from numpy import (loadtxt, arange, searchsorted, add, zeros, unravel_index,
                   where)

wind_data = loadtxt('wind.data')

data = wind_data[:, 3:]

print('2. Statistics over all values')
print('  min:', data.min())
print('  max:', data.max())
print('  mean:', data.mean())
print('  standard deviation:', data.std())
print()

print('3. Statistics over all days at each location')
print('  min:', data.min(axis=0))
print('  max:', data.max(axis=0))
print('  mean:', data.mean(axis=0))
print('  standard deviation:', data.std(axis=0))
print()

print('4. Statistics over all locations for each day')
print('  min:', data.min(axis=1))
print('  max:', data.max(axis=1))
print('  mean:', data.mean(axis=1))
print('  standard deviation:', data.std(axis=1))
print()

print('5. Location of daily maximum')
print('  daily max location:', data.argmax(axis=1))
print()

daily_max = data.max(axis=1)
max_row = daily_max.argmax()
# Note: Another way to do this would be to use the unravel_index function
# which takes a linear index and convert it to a location given the shape
# of the array:
max_row, max_col = unravel_index(data.argmax(), data.shape)
# Or you could use "where", which identifies *all* the places where the max
# occurs, rather than just the first. Note that "where" returns two arrays in
# this case, instead of two integers.
max_row, max_col = where(data == data.max())


print('6. Day of maximum reading')
print('  Year:', int(wind_data[max_row, 0]))
print('  Month:', int(wind_data[max_row, 1]))
print('  Day:', int(wind_data[max_row, 2]))
print()

january_indices = wind_data[:, 1] == 1
january_data = data[january_indices]

print('7. Statistics for January')
print('  mean:', january_data.mean(axis=0))
print()

# Bonus

# compute the month number for each day in the dataset
months = (wind_data[:, 0] - 61) * 12 + wind_data[:, 1] - 1

# we're going to use the month values as indices, so we need
# them to be integers
months = months.astype(int)

# get set of unique months
month_values = set(months)

# initialize an array to hold the result
monthly_means = zeros(len(month_values))

for month in month_values:
    # find the rows that correspond to the current month
    day_indices = (months == month)

    # extract the data for the current month using fancy indexing
    month_data = data[day_indices]

    # find the mean
    monthly_means[month] = month_data.mean()

    # Note: experts might do this all-in one
    # monthly_means[month] = data[months==month].mean()

# In fact the whole for loop could reduce to the following one-liner
# monthly_means = array([data[months==month].mean() for month in month_values])


print("Bonus 1.")
print("  mean:", monthly_means)
print()

# Bonus 2.
# Extract the data for the first 52 weeks. Then reshape the array to put
# on the same line 7 days worth of data for all locations. Let Numpy
# figure out the number of lines needed to do so
weekly_data = data[:52 * 7].reshape(-1, 7 * 12)

print('Bonus 2. Weekly statistics over all locations')
print('  min:', weekly_data.min(axis=1))
print('  max:', weekly_data.max(axis=1))
print('  mean:', weekly_data.mean(axis=1))
print('  standard deviation:', weekly_data.std(axis=1))
print()

# Bonus Bonus : this is really tricky...

# compute the month number for each day in the dataset
months = (wind_data[:, 0] - 61) * 12 + wind_data[:, 1] - 1

# find the indices for the start of each month
# this is a useful trick - we use range from 0 to the
# number of months + 1 and searchsorted to find the insertion
# points for each.
month_indices = searchsorted(months, arange(months[-1] + 2))

# now use add.reduceat to get the sum at each location
monthly_loc_totals = add.reduceat(data, month_indices[:-1])

# now use add to find the sum across all locations for each month
monthly_totals = monthly_loc_totals.sum(axis=1)

# now find total number of measurements for each month
month_days = month_indices[1:] - month_indices[:-1]
measurement_count = month_days * 12

# compute the mean
monthly_means = monthly_totals / measurement_count

print("Bonus Bonus")
print("  mean:", monthly_means)

# Notes: this method relies on the fact that the months are contiguous in the
# data set - the method used in the bonus section works for non-contiguous
# days.
