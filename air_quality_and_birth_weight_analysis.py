# Written by Anthony Cessna and Aaron Hunsaker
# November 2021

import csv
from collections import namedtuple
from collections import defaultdict
import logging
import plotly.express as px
import os
import argparse
import statistics
import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import glob

class AirQuality_obj:

    def __init__(self, state, county, year, good_days, moderate_days, unhealthy_days,
                very_unhealthy_days, hazardous_days, max_aqi):
        
        self.state = str(state)
        self.county = str(county)
        self.year = int(year)
        self.good_days = int(good_days)
        self.moderate_days = int(moderate_days)
        self.unhealthy_days = int(unhealthy_days)
        self.very_unhealthy_days = int(very_unhealthy_days)
        self.hazardous_days = int(hazardous_days)
        self.max_aqi = int(max_aqi)


    # String representation of the object, human friendly display
    def __str__(self):
        string = f"{str(self.state)}     {str(self.county)}     {str(self.year)} \n\nGood days: {str(self.good_days)}\n"\
                 f"Moderate days: {str(self.moderate_days)}\nUnhealthy days: {str(self.unhealthy_days)}\n"\
                 f"Very unhealthy days: {str(self.very_unhealthy_days)}\nHazardous days: {str(self.hazardous_days)}\n"\
                 f"Max AQI: {str(self.max_aqi)}"

        return string

    # String representation of the object
    def __repr__(self):
        return "AirQuality_obj(" + str(self.state) + ", " + str(self.county) + ", " + str(self.year) + ", " + str(self.good_days) \
                + ", " + str(self.moderate_days) + ", " + str(self.unhealthy_days) + ", " + str(self.very_unhealthy_days) + ", " \
                + str(self.hazardous_days) + ", " + str(self.max_aqi) + ")"

    # Enables use of less than operator for two AirQuality_obj objects
    def __lt__(self, other):
        if type(self) is type(other):

            self_tuple = (self.hazardous_days, self.very_unhealthy_days, self.unhealthy_days, self.moderate_days)
            other_tuple = (other.hazardous_days, other.very_unhealthy_days, other.unhealthy_days, other.moderate_days)

            return self_tuple < other_tuple
        elif other is None:
            return False
        else:
            return NotImplemented

    # Enables use of greater than operator for two AirQuality_obj objects
    def __gt__(self, other):
        if type(self) is type(other):

            self_tuple = (self.hazardous_days, self.very_unhealthy_days, self.unhealthy_days, self.moderate_days)
            other_tuple = (other.hazardous_days, other.very_unhealthy_days, other.unhealthy_days, other.moderate_days)

            return self_tuple > other_tuple
        
        elif other is None:
            return True
        else:
            return NotImplemented

class Import_AirQuality_Data:

    def __init__(self):
        self.numpy_arrays = self._numpy_array()
        self.dataframe = self._pandas_data_frame()
        self.obj_list = self._load_data_object_list()

    # The method numpy_array creates a numpy array of the numerical data in the air_quality data set for analysis
    def _numpy_array(self):

        # Gets list of csv files in directory
        csv_files = glob.glob("annual_aqi_by_county_*.csv")
        logging.debug(csv_files)

        numpy_arrays = None

        for csv_file in csv_files:
            with open(csv_file) as csv_connection:
                count_rows = 0
                csv_reader = csv.reader(csv_connection, delimiter=",")
                
                array = []
                for row in csv_reader: 
                    count_token = 1
                    row_list = []
                    if count_rows == 0: # Skips header row
                        logging.debug(row)
                        
                        count_rows+=1
                    else:
                        
                        for token in row:
                            if count_token not in [1,2]: # Skips string data
                                row_list.append(int(token))
                            
                            count_token += 1
                        
                        array.append(row_list)

                numpy_arrays = np.array(array)
                logging.debug("numpy array created")

        return numpy_arrays
                    
    # The method _pandas_data_frame reads in Airquality data and turns it into a dataframe for visualization
    def _pandas_data_frame(self):
        
        # Gets list of csv files in directory
        csv_file = glob.glob("annual_aqi_by_county_*.csv")

        us_state_to_abbrev = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC",
            "American Samoa": "AS",
            "Guam": "GU",
            "Northern Mariana Islands": "MP",
            "Puerto Rico": "PR",
            "United States Minor Outlying Islands": "UM",
            "U.S. Virgin Islands": "VI",
        }

        air_quality_df = pd.read_csv(csv_file[0])

        air_quality_df["state_abbrev"] = air_quality_df["State"].map(us_state_to_abbrev)
        print(air_quality_df.head())

        logging.debug("Pandas dataframe created")

    # This method loads each row into AirQuality_obj and creats a list of all the objects
    def _load_data_object_list(self):
        air_quality_obj_list = []
        
        # Gets list of csv files in directory
        csv_file = glob.glob("*annual_aqi_by_county_*.csv")

        with open(csv_file[0]) as csv_connection:
            count_rows = 0
            csv_reader = csv.reader(csv_connection, delimiter=",")

            for row in csv_reader:
                state = ""
                county = ""
                year = 0
                good_days = 0
                moderate_days = 0
                unhealthy_days = 0
                very_unhealthy_days = 0
                hazardous_days = 0
                max_aqi = 0

                if count_rows == 0: # Skips header row
                        
                    count_rows+=1
                else:
                    count_token = 1
                    for token in row:
                        if count_token == 1:
                            state = str(token)
                        elif count_token == 2:
                            county = str(token)
                        elif count_token == 3:
                            year = int(token)
                        elif count_token == 5:
                            good_days = int(token)
                        elif count_token == 6:
                            moderate_days = int(token)
                        elif count_token == 8:
                            unhealthy_days = int(token)
                        elif count_token == 9:
                            very_unhealthy_days = int(token)
                        elif count_token == 10:
                            hazardous_days = int(token)
                        elif count_token == 11:
                            max_aqi = int(token)
                        elif count_token > 11:
                            continue
                        count_token += 1

                air_quality_obj_list.append(AirQuality_obj(state, county, year, good_days,
                                            moderate_days, unhealthy_days, very_unhealthy_days,
                                            hazardous_days, max_aqi))

        return air_quality_obj_list

    # Method return the name of the county in the given state with the worst air quality
    # Bad air quality defined as most Hazardous days, then most Very Unhealthy days etc...
    def worst_air_quality_in_state(self, state):
        
        worst_air_quality = ""
        worst_air_obj = None

        for obj in self.obj_list:
            if worst_air_obj is None and obj.state == state:
                worst_air_obj = obj
            elif obj > worst_air_obj and obj.state == state:
                 worst_air_obj = obj

        worst_air_quality = worst_air_obj.county
        return worst_air_quality

    # Method return the name of the county in the given state with the best air quality
    # Good air quality defined as least Hazardous days, then least Very Unhealthy days etc...
    def best_air_quality_in_state(self, state):
        
        best_air_quality = ""
        best_air_obj = None

        for obj in self.obj_list:
            if best_air_obj is None and obj.state == state:
                best_air_obj = obj
            elif obj < best_air_obj and obj.state == state:
                 best_air_obj = obj

        best_air_quality = best_air_obj.county
        return best_air_quality

def main():
    # sets root logger to DEBUG
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    # Creates log file to include all logs
    fh = logging.FileHandler("air_quality.log", "w")
    fh.setLevel(logging.DEBUG)
    rootLogger.addHandler(fh)

    # Stream Handler at level of INFO
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    rootLogger.addHandler(sh)


    ############### Test Area ####################
    obj = Import_AirQuality_Data()
    
    state = "Washington"

    print(obj.worst_air_quality_in_state(state))
    print(obj.best_air_quality_in_state(state))
    
    


if __name__ == '__main__':
    main()