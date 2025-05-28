# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy as np

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    array_list = []
    for i in degs:
        array_list.append(pylab.polyfit(x, y, i))
    return array_list

#print(generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2]))


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = np.mean(y)
    numerator = (y - estimated)**2
    denom = (y - mean)**2
    #print(denom)
    
    num_float = 0
    denom_float = 0
    
    for i in numerator:
        num_float += i 
        
    for j in denom:
        denom_float += j
        
    r_squared = 1 - (num_float)/(denom_float)

    return r_squared

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #note: degree of a model is one if length is one im assuming???
    estimated_list = []

    for i in models:
        #for each model we simply want to follow the instructions detailed
        #above in the docstring
        estimated = pylab.polyval(i, x)
        estimated_list.append(estimated)
        model_r_squared = r_squared(y, estimated)
        model_deg = len(i) - 1
        
        title = "Degree =" + str(model_deg) + ", R squared =" + str(model_r_squared) 

        
        if model_deg == 1:
            se_over = se_over_slope(x, y, estimated, i)
            title = title + ", \n" + "se over slope =" + str(se_over)

        pylab.scatter(x, y, label='Training', marker='o')
        pylab.plot(x, estimated, label='Model', color='red')
        pylab.xlabel('X axis')
        pylab.ylabel('Y axis')
        pylab.title(title)
        #pylab.legend()
        pylab.legend(loc='upper left')
        # Note: is it possible to make the legend draggable?
        pylab.grid(True)
        pylab.show()
    
    return None
     
'''
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([1,4,8,17,23,32,51,64,83,99])
degs = [1,2,3]
models = generate_models(x,y,degs)
print(models)
evaluate_models_on_training(x,y,models)
'''

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    average_temp = []
    for year in years:
        year_avg = []
        for city in multi_cities:
            avg_temp = np.mean(climate.get_yearly_temp(city, year))
            year_avg.append(avg_temp)
        average_temp.append(np.mean(year_avg))
            
    return np.array(average_temp)



def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    mov_avg_vals = []

    for i in range(len(y)):
        mov_avg = 0
        j = i - window_length + 1

        if j < 0:
            j = 0
            
        for val in range(j, i+1):
            mov_avg += y[val]
        
        mov_avg = mov_avg/((i-j) + 1)
        mov_avg_vals.append(mov_avg)
    
    return np.array(mov_avg_vals)
    
    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    rmse = (sum(((y - estimated)**2)/(len(y))))**0.5
    return rmse






def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_arr = []


    year_avg_data = []


    for year in years:
        year_data = []
        total_data = []
        for city in multi_cities:
            
            city_data = list(climate.get_yearly_temp(city, year))
            year_data.append(city_data)
            
        length = len(year_data[0])
        
        for i in range(length):
            avg = 0
            for data in year_data:
                avg += data[i]
            avg = avg/len(year_data)
            total_data.append(avg)
        year_avg_data.append(total_data)
        
        
            
    for data in year_avg_data:
        std_arr.append(np.std(data))
        
    return std_arr
        

        
                
                
            
            
    




def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #note: degree of a model is one if length is one im assuming???
    estimated_list = []

    for i in models:
        #for each model we simply want to follow the instructions detailed
        #above in the docstring
        estimated = pylab.polyval(i, x)
        estimated_list.append(estimated)
        model_rmse = rmse(y, estimated)
        model_deg = len(i) - 1
        
        title = "Degree =" + str(model_deg) + ", RMSE =" + str(model_rmse)

        pylab.scatter(x, y, label='Testing', marker='o')
        pylab.plot(x, estimated, label='Model', color='red')
        pylab.xlabel('X axis')
        pylab.ylabel('Y axis')
        pylab.title(title)
        #pylab.legend()
        pylab.legend(loc='upper left')
        # Note: is it possible to make the legend draggable?
        pylab.grid(True)
        pylab.show()
    
    return None




if __name__ == '__main__':

    pass 

    # Part A.4
    
    '''
    # Part 4.I
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []
    y_data = []

    for year in TRAINING_INTERVAL:
        x_data.append(year)
        temp = climate.get_daily_temp('NEW YORK', 1, 10, year)
        y_data.append(temp)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1]
    #print(x_data)
    models = generate_models(x_data, y_data, degs)
    evaluate_models_on_training(x_data, y_data, models)
    '''
    
    '''
    # Part 4.II
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []
    y_data = []

    for year in TRAINING_INTERVAL:
        x_data.append(year)
        temp = np.mean(climate.get_yearly_temp('NEW YORK', year))
        y_data.append(temp)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1]
    #print(x_data)
    models = generate_models(x_data, y_data, degs)
    evaluate_models_on_training(x_data, y_data, models)
    '''
    
    
    # Part B
    '''
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []
    multi_cities = CITIES
    years = TRAINING_INTERVAL
    y_data = gen_cities_avg(climate, multi_cities, years)

    for year in TRAINING_INTERVAL:
        x_data.append(year)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1]
    #print(x_data)
    models = generate_models(x_data, y_data, degs)
    evaluate_models_on_training(x_data, y_data, models)
    '''

    # Part C
    '''
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []
    multi_cities = CITIES
    years = TRAINING_INTERVAL
    y_data = gen_cities_avg(climate, multi_cities, years)

    for year in TRAINING_INTERVAL:
        x_data.append(year)
        
    window_length = 5
    y_data = moving_average(y_data, window_length)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1]
    models = generate_models(x_data, y_data, degs)
    evaluate_models_on_training(x_data, y_data, models)
    '''
    

    # Part D.2
    # Part 2.I
    '''
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []
    multi_cities = CITIES
    years = TRAINING_INTERVAL
    y_data = gen_cities_avg(climate, multi_cities, years)

    for year in TRAINING_INTERVAL:
        x_data.append(year)
        
    window_length = 5
    y_data = moving_average(y_data, window_length)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1, 2, 20]
    models = generate_models(x_data, y_data, degs)
    evaluate_models_on_training(x_data, y_data, models)
    '''
    
    
    # Part 2.II
    '''
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []
    multi_cities = CITIES
    years = TRAINING_INTERVAL
    y_data = gen_cities_avg(climate, multi_cities, years)

    for year in TRAINING_INTERVAL:
        x_data.append(year)
        
    window_length = 5
    y_data = moving_average(y_data, window_length)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1, 2, 20]
    models = generate_models(x_data, y_data, degs)
    
    test_years = TESTING_INTERVAL
    x_test_data = []
    for year in TESTING_INTERVAL:
        x_test_data.append(year)
        
    y_test_data = gen_cities_avg(climate, multi_cities, test_years)
    y_test_data = moving_average(y_test_data, window_length)
    evaluate_models_on_testing(x_test_data, y_test_data, models)
    '''
    
    

    # Part E
    '''
    filename = "data.csv"
    climate = Climate(filename)
    x_data = []

    multi_cities = CITIES
    years = TRAINING_INTERVAL
    
    y_data = gen_std_devs(climate, multi_cities, years)

    for year in TRAINING_INTERVAL:
        x_data.append(year)
        
    window_length = 5
    y_data = moving_average(y_data, window_length)
    
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    degs = [1]
    models = generate_models(x_data, y_data, degs)
    evaluate_models_on_training(x_data, y_data, models)
    '''
