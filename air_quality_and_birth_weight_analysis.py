# Written by Anthony Cessna and Aaron Hunsaker
# November 2021

import csv
from collections import namedtuple
from collections import defaultdict
import logging
import plotly.express as px
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import glob
from dataclasses import dataclass

class AirQuality_obj:
    """
    A class that represents different aspects of air quality for one county in the USA

    Attributes
    ----------
    state : str
        The state the county is located in
    county : str
        The county being examined
    year : int
        The year being examined
    good_days : int
        The number of days in the year with AQI considered good
    moderate_days : int
        The number of days in the year with AQI considered moderate
    unhealthy_days : int
        The number of days in the year with AQI considered unhealthy
    very_unhealthy_days : int
        The number of days in the year with AQI considered very unhealthy
    hazardous_days : int
        The number of days in the year with AQI considered hazardous
    max_aqi : int
        The max AQI observed on any day of the year

    """

    def __init__(self, state, county, year, good_days, moderate_days, unhealthy_days,
                very_unhealthy_days, hazardous_days, max_aqi):
        """
        Parameters
        ----------
        state : str
            The state the county is located in
        county : str
            The county being examined
        year : int
            The year being examined
        good_days : int
            The number of days in the year with AQI considered good
        moderate_days : int
            The number of days in the year with AQI considered moderate
        unhealthy_days : int
            The number of days in the year with AQI considered unhealthy
        very_unhealthy_days : int
            The number of days in the year with AQI considered very unhealthy
        hazardous_days : int
            The number of days in the year with AQI considered hazardous
        max_aqi : int
            The max AQI observed on any day of the year
        """
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
        """
        Enables use of the less than operator to determine which object has worse air quality

        Parameters
        ----------
        other : AirQuality-obj
            Object to compare to
        """
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
        """
        Enables use of the greater than operator to determine which object has worse air quality

        Parameters
        ----------
        other : AirQuality-obj
            Object to compare to
        """
        if type(self) is type(other):

            self_tuple = (self.hazardous_days, self.very_unhealthy_days, self.unhealthy_days, self.moderate_days)
            other_tuple = (other.hazardous_days, other.very_unhealthy_days, other.unhealthy_days, other.moderate_days)

            return self_tuple > other_tuple
        
        elif other is None:
            return True
        else:
            return NotImplemented

class Import_AirQuality_Data:
    """
    A class that loads in a whole air quality dataset in a year by county

    Attributes
    ----------
    numpy_arrays : np.array
        A numpy array that holds all the numerical data 
    dataframe  : pandas dataframe
        A data frame containing all the info from the original csv, and calculated columns for visualizations
    obj_list : list of AirQuality_obj
        A list of all the objects representing a row of data

    Methods
    -------
    _numpy_array()
        Creates numpy array of the data
    _pandas_data_frame()
        Creates pandas data frame of the data
    _load_data_object_list()
        Creates list of AirQuality_obj
    chloropleth_usa_map(column)
        Creates a chloropleth graphic assigning the value in column to its relevent state
    worst_air_quality_in_state(state)
        Returns the name of the county with the worst air quality in a given state
    best_air_quality_in_state(state)
        Returns the name of the county with the worst air quality in a given state
    """

    def __init__(self):
        """
        Parameters
        ----------
        none
        """
        self.numpy_arrays = self._numpy_array()
        self.dataframe = self._pandas_data_frame()
        self.obj_list = self._load_data_object_list()
        self.best_worst_dataframe = self.extreme_values_data_frame()
        logging.debug("Import_AirQuality_Data object successfully initialized")


    # The method numpy_array creates a numpy array of the numerical data in the air_quality data set for analysis
    def _numpy_array(self):
        """
        Creates numpy array of the numerical data found in the air quality data set

        Parameters
        ----------
        none
        """

        # Gets list of csv files in directory
        csv_files = glob.glob("annual_aqi_by_county_*.csv") # Finds dataset in directory
        logging.debug(f"Dataset files found by numpy_array method:{csv_files}")

        numpy_arrays = None

        for csv_file in csv_files:
            with open(csv_file) as csv_connection:

                logging.debug("CSV file opened in numpy_array method")

                count_rows = 0
                csv_reader = csv.reader(csv_connection, delimiter=",")
                
                array = []
                for row in csv_reader: 
                    count_token = 1
                    row_list = []
                    if count_rows == 0: # Skips header row
                        
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
        """
        Makes a pandas dataframe from the data and calculates summary statistics on the state level then creates an air quality
        by state score to be used in plotting

        Parameters
        ----------
        None
        """
        # Gets list of csv files in directory
        csv_file = glob.glob("annual_aqi_by_county_*.csv")
        logging.debug(f"Dataset files found by pandas_data_frame method:{csv_file}")
        
        # Dictionary that matches the state name to their abbreviation, to be used for mapping
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
        logging.debug("data file successfully read into pandas_data_frame method")

        # Creates column listing the state abbreviation, and removes rows that do not match a US state
        air_quality_df["state_abbrev"] = air_quality_df["State"].map(us_state_to_abbrev)
        air_quality_df = air_quality_df[air_quality_df["state_abbrev"].notna()]
        
        # Creates columns that averages the number of days with a given air quality by county, to get state averages
        air_quality_df["mean_hazardous_days_by_state"] = air_quality_df.groupby("State")["Hazardous Days"].transform("mean")
        air_quality_df["mean_very_unhealthy_days_by_state"] = air_quality_df.groupby("State")["Very Unhealthy Days"].transform("mean")
        air_quality_df["mean_unhealthy_days_by_state"] = air_quality_df.groupby("State")["Unhealthy Days"].transform("mean")
        air_quality_df["mean_moderate_days_by_state"] = air_quality_df.groupby("State")["Moderate Days"].transform("mean")
        air_quality_df["mean_good_days_by_state"] = air_quality_df.groupby("State")["Good Days"].transform("mean")

        # Weights days of a bad air quality more to create an air quality score over thw whole state
        air_quality_df["mean_hazardous_days_weighted"] = air_quality_df["mean_hazardous_days_by_state"].transform(lambda x: x*20)
        air_quality_df["mean_very_unhealthy_weighted"] = air_quality_df["mean_very_unhealthy_days_by_state"].transform(lambda x: x*10)
        air_quality_df["mean_unhealthy_weighted"] = air_quality_df["mean_unhealthy_days_by_state"].transform(lambda x: x*5)

        # Creates an air quality score metric for the whole state
        air_quality_score_list = []
        for index, row in air_quality_df.iterrows():
            air_quality_score_list.append(row["mean_hazardous_days_weighted"] + row["mean_very_unhealthy_weighted"] + row["mean_unhealthy_weighted"] + row["mean_moderate_days_by_state"])

        air_quality_df["air_quality_score"] = air_quality_score_list

        return air_quality_df

    # Method outputs data frame to csv file
    def air_quality_csv(self):
        """
        Out puts a csvfile of the Dataframe stored in the object

        Parameters
        ----------
        None
        """
        # Exports a csv of the dataframe
        self.dataframe.to_csv("Air_Quality_by_county.csv")
        logging.debug("Pandas dataframe created, and csv file created")

    # This method creates a chloropleth map giving values to states based on any column of data
    def chloropleth_usa_map(self, column, output):
        """
        Creates a US map graphic coloring the states by a metric specified in the column parameter

        Parameters
        ----------
        column : str
            Data to be used to color the states in the map
        output : str
            Output of the function either "pdf" or "web"
        """

        if output not in ["pdf", "web"]:
            raise TypeError("Argument must be either pdf or web")

        states = self.dataframe["state_abbrev"].unique() # Subsets data to keep one row for each state
        
        values = self.dataframe[column].unique()
       
        # Creates map graphic
        fig = px.choropleth(locations=states, locationmode="USA-states", color=values, 
                scope="usa", title="Air Quality by State", labels={"color": "Air Quality Score", "locations" : "State"})
        
        if output == "web":

            fig.show()
            logging.debug(f"chloropleth map output to web, created using column: {column}")

        elif output == "pdf":
            fig.write_image("Air_Quality_in_US_by_State.pdf")
            logging.debug(f"chloropleth map output to pdf, created using column: {column}")

    # This method loads each row into AirQuality_obj and creats a list of all the objects
    def _load_data_object_list(self):
        """
        Loads data into AirQuality_obj list

        Parameters
        ----------
        none
        """
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

                # Adds object to list
                air_quality_obj_list.append(AirQuality_obj(state, county, year, good_days,
                                            moderate_days, unhealthy_days, very_unhealthy_days,
                                            hazardous_days, max_aqi))

        return air_quality_obj_list

    # Method return the name of the county in the given state with the worst air quality
    # Bad air quality defined as most Hazardous days, then most Very Unhealthy days etc...
    def worst_air_quality_in_state(self, state):
        """
        Returns the name of the county in the given state with the worst air quality
        Bad air quality defined as most Hazardous days, then most Very Unhealthy days etc...

        Parameters
        ----------
        state : str
            State to check air quality
        """
        logging.debug(f"worst_air_quality_in_state method called for state: {state}")
        worst_air_quality = ""
        worst_air_obj = None

        for obj in self.obj_list:
            if worst_air_obj is None and obj.state == state:
                worst_air_obj = obj
            elif obj > worst_air_obj and obj.state == state:
                 worst_air_obj = obj

        if worst_air_obj is None:
            raise ValueError("Not a valid state in argument")
        else:
            worst_air_quality = worst_air_obj.county

        return worst_air_quality

    # Method return the name of the county in the given state with the best air quality
    # Good air quality defined as least Hazardous days, then least Very Unhealthy days etc...
    def best_air_quality_in_state(self, state):
        """
        Returns the name of the county in the given state with the best air quality
        Good air quality defined as least Hazardous days, then least Very Unhealthy days etc...

        Parameters
        ----------
        state : str
            State to check air quality
        """
        logging.debug(f"best_air_quality_in_state method called for state: {state}")
        best_air_quality = ""
        best_air_obj = None

        for obj in self.obj_list:
            if best_air_obj is None and obj.state == state:
                best_air_obj = obj
            elif obj < best_air_obj and obj.state == state:
                 best_air_obj = obj

        if best_air_obj is None:
            raise ValueError("Not a valid state in argument")
        else:
            best_air_quality = best_air_obj.county

        return best_air_quality

    # This method creates a data frame that contains the counties in every state with the best and worst air quality
    # and then also lists those counties max AQI experienced in a year
    def extreme_values_data_frame(self):
        """
        Returns a pandas DataFrame that contains the counties in every state with the best and worst air quality
        and then also lists those counties max AQI experienced in a year
        """
        
        df = self.dataframe

        new_df = pd.DataFrame()

        state_list = []
        county_list = []
        aqi_list = []

        for state in df["State"].unique():
            best = self.best_air_quality_in_state(state)
            worst = self.worst_air_quality_in_state(state)
            best_aqi = df.loc[df["County"] == best, 'Max AQI'].iloc[0]
            worst_aqi = df.loc[df["County"] == worst, 'Max AQI'].iloc[0]

            state_list.append(state)
            state_list.append(state)
            county_list.append(best)
            county_list.append(worst)
            aqi_list.append(best_aqi)
            aqi_list.append(worst_aqi)

        new_df["State"] = state_list
        new_df["County"] = county_list
        new_df["Max_AQI"] = aqi_list
        return new_df

    # This Method creates a sunburst graphic which displays counties in state with best and worst air quality and specifies maxc AQI values
    def extreme_aqi_values_sunburst(self, output):
        """
        Creates a sunburst graphic which displays counties in state with best and worst air quality and specifies maxc AQI values

        Parameters
        ----------
        output : str
            Output of the function either "pdf" or "web"
        """

        if output not in ["pdf", "web"]:
            raise TypeError("Argument must be either pdf or web")

        fig = px.sunburst(self.best_worst_dataframe, path=["State", "County"], values="Max_AQI", title="Air Quality by State", 
                                labels={"labels": "County", "Max_AQI" : "Max AQI", "parent" : "State"})

        if output == "web":

            fig.show()
            logging.debug("Starburst map output to web")

        elif output == "pdf":
            fig.write_image("Best_and_Worst_AQI_by_State.pdf")
            logging.debug("Starburst map output to pdf")

@dataclass(eq=True,order=True)
class BirthObject():
    """
    BirthObject is a data class that is configured to handle __eq__(),__lt__(),
    __gt__(), __sort__(),__hash __() and  __init__() implicitly
    or with configs in the decorater.

    It basically takes all the functionality in the AutoMPG()
    class but only needs like 6 lines of code
    pretty sweet
    """
    year: str
    county: str
    state: str
    average_birth_weight: float

class BirthDataStats():
    """ 
    data stats class that loasds data and creats visualizations for analyizing birth weigh
    data by state, and county
    """

    def __init__(self):
        self.birth_data()
        self.df = self.pandas_df()

    def __iter__(self):
        return iter(self.data)


    def birth_data(self):
        self.data = []
        Birth = namedtuple("Birth"," year, county_state, a,b,c,d,e, weight, f,g")


        with open("birth_data.csv","r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                birth = Birth(*[element for element in row])

                b = BirthObject(birth.year.split("-")[0],
                birth.county_state.split(',')[0],
                birth.county_state.split(',')[1],
                round(float(birth.weight)/453.592,2))

                self.data.append(b)


    def pandas_df(self):
        data_frame = pd.DataFrame(self.data)
        
        data_frame["avg_birth_weight_by_state"] = data_frame.groupby(["state", "year"])["average_birth_weight"].transform("mean")
        data_frame["min birth weight by state"] = data_frame.groupby(["state", "year"])["average_birth_weight"].transform("min")
        data_frame["idx_county_with_lowest_birthweight"]= data_frame.groupby(["state", "year"])["average_birth_weight"].transform("idxmin")
        data_frame["max birth weight by state"] = data_frame.groupby(["state", "year"])["average_birth_weight"].transform("max")
        data_frame["idx_county_with_highest_birthweight"]= data_frame.groupby(["state", "year"])["average_birth_weight"].transform("idxmax")
        
        data_frame["min birth weight by county"] = data_frame.groupby(["state", "year"])["average_birth_weight"].transform("min")
        data_frame["max birth weight by county"] = data_frame.groupby(["state", "year"])["average_birth_weight"].transform("max")

        county_lowest_list = []
        for index, row in data_frame.iterrows():
            county_lowest_list.append(data_frame.iloc[row["idx_county_with_lowest_birthweight"]]["county"])

        data_frame["county_in_state_lowest_birthweight_by_year"] = county_lowest_list

        county_highest_list = []
        for index, row in data_frame.iterrows():
            county_highest_list.append(data_frame.iloc[row["idx_county_with_highest_birthweight"]]["county"])

        data_frame["county_in_state_highest_birthweight_by_year"] = county_highest_list

        return data_frame


    def birth_csv(self):
        """
        Out puts a csvfile of the Dataframe stored in the object

        Parameters
        ----------
        None
        """
        # Exports a csv of the dataframe
        self.df.to_csv("Birth_data_by_county.csv")
        logging.debug("Pandas dataframe created, and csv file created")

    def yearly_bw_state(self,output):
        tst = self.df
        fig = px.scatter(tst, x = "state", y = "avg_birth_weight_by_state", color ="year",
            title = "2016-2018 Breakdown of Average Birthweight by State", labels={
                "year" : "Year", "avg_birth_weight_by_state" : "Average Birth Weight (lbs)",
                "state" : "State"
            }) 
       
        if output == "web":

            fig.show()
            logging.debug("yearly birth weight by state scatter plot to web")

        elif output == "pdf":
            fig.write_image("yearly_bw_state.pdf")
            logging.debug("scatter chart output to pdf")


    def lowest_weight_in_state(self,output, year):
        temp = self.df
        temp_year = temp[temp["year"] == year]
        temp_drop = temp_year.drop_duplicates(subset="state")
        
        fig = px.bar(temp_drop, x = "state", y ="min birth weight by county", title= "County with the Lowest Birth Weight in State", barmode='group',
                        log_y=True, text="county_in_state_lowest_birthweight_by_year", labels={
                            "average_birth_weight" : "Average Birth Weight in County (lbs)",
                            "state" : "State"
                        })
       
        if output == "web":

            fig.show()
            logging.debug("Lowest birth weight in state scatter chart to web")

        elif output == "pdf":
            fig.write_image("lowest_weight_in_state.pdf")
            logging.debug("Lowest weight in state scatter chart output to pdf")

    def highest_weight_in_state(self,output, year):
        temp = self.df
        temp_year = temp[temp["year"] == year]
        temp_drop = temp_year.drop_duplicates(subset="state")
        
        fig = px.bar(temp_drop, x = "state", y ="max birth weight by county", title= "County with the Highest Birth Weight in State", barmode='group',
                        log_y=True, text="county_in_state_highest_birthweight_by_year", labels={
                            "average_birth_weight" : "Average Birth Weight in County (lbs)",
                            "state" : "State"
                        })

        if output == "web":

            fig.show()
            logging.debug("Highest birth weight in state scatter chart to web")

        elif output == "pdf":
            fig.write_image("highest_weight_in_state.pdf")
            logging.debug("Highest weight in state scatter chart output to pdf")   

class BirthWeight_and_AirQuality():

    def __init__(self, air_quality_obj, birth_obj):
        self.air_quality_obj = air_quality_obj
        self.birth_obj = birth_obj
        self.merged_dataframe = self.combined_dataframe()

    def combined_dataframe(self):
        air_quality_df = self.air_quality_obj.dataframe
        birth_df = self.birth_obj.df
        birth_df = birth_df[birth_df["year"] == "2018"]
        birth_df = birth_df.drop_duplicates(subset=["county", "state"])
        

        counties = birth_df["county"].tolist()
        counties_list = [x[:x.find("County")-1] for x in counties]

        birth_df["County"] = counties_list

        abbrev = birth_df["state"].tolist()
        abbrev_list = [x.strip() for x in abbrev]
        birth_df["state_abbrev"] = abbrev_list

        merged_df = pd.merge(air_quality_df, birth_df, on=["County", "state_abbrev"])
        
        return merged_df

    def combined_csv(self):
        """
        Out puts a csvfile of the Dataframe stored in the object

        Parameters
        ----------
        None
        """
        # Exports a csv of the dataframe
        self.merged_dataframe.to_csv("Combined.csv")
        logging.debug("Pandas dataframe created, and csv file created") 
     
    def state_air_quality_bw_breakdown(self,output):

        """
        this breaks stats into 4 bins based on median air quality and median average birth wieght by state
        high ABW and high AQS quadratn 1, low ABW and high AQS, quadrant 2, low ABW and low ABW  quadrant 3, and high ABW and low AQS quadrant 4
        The boudaries of the bins are the medians of ABW and AQs, we def find a a pattern where out of 46 states in our combined data set
        we see 14 states in quadrant 2 (Low ABS High AQs) and 14 states in quadrant 4 (High ABS Low AQS).
        """

        breakdown = self.merged_dataframe[["State","air_quality_score","avg_birth_weight_by_state"]].drop_duplicates()
        breakdown["avg_birth_weight_by_state"] = breakdown["avg_birth_weight_by_state"].map(lambda x: round(x,3))
        breakdown["air_quality_score"] = breakdown["air_quality_score"].map(lambda x: round(x,3))



        # setting median values for quadrant boundaries
        median_bw = breakdown["avg_birth_weight_by_state"].median()
        median_aqs = breakdown["air_quality_score"].median()

        #setting qadrant boundries
        bw_below_median = breakdown["avg_birth_weight_by_state"] < round(median_bw,2)
        aqs_below_median = breakdown["air_quality_score"] < round(median_aqs,2)
        bw_above_median = breakdown["avg_birth_weight_by_state"] > round(median_bw,2)
        aqs_above_median =  breakdown["air_quality_score"] > round(median_aqs,2)

        #building quandrant data sets
        first_quadrant = breakdown.where(bw_above_median & aqs_above_median).dropna()
        second_quadrant = breakdown.where(bw_below_median & aqs_above_median).dropna()
        third_quadrant = breakdown.where(bw_below_median & aqs_below_median).dropna()
        fourth_quadrant = breakdown.where(bw_above_median & aqs_below_median).dropna()

        #chart that shows break down of all four quadrant
        fig = px.scatter(breakdown, x = "avg_birth_weight_by_state", y ="air_quality_score", color= "State", size = "avg_birth_weight_by_state",
        title ="Air Quality Score(AQS) and Average Birth Weight (ABW) by State. (median AQS = blue line, median ABW  = red line)",
        labels = {"avg_birth_weight_by_state" : 'Average Birth Weight(lbs)', 'air_quality_score': 'Air Quality Score', 'State':"State"})
        fig.add_vline(x= breakdown["avg_birth_weight_by_state"].median(), line_width = 2, line_dash = 'dash', line_color = "red")
        fig.add_hline(y= breakdown['air_quality_score'].median(),line_width = 2, line_dash = 'dash', line_color = "blue")



        #chart that shows the first quadrant breakdown, note it has 13 states
        fig1 = px.scatter(first_quadrant,x ="avg_birth_weight_by_state" , y ="air_quality_score", color= "State",size = "avg_birth_weight_by_state",
        title = "Quadrant 1 High ABW & High AQS (median AQS = blue line, median ABW = red line)",
        labels = {"avg_birth_weight_by_state" : 'Average Birth Weight(lbs)', 'air_quality_score': 'Air Quality Score', 'State':"State"})
        fig1.add_vline(x= breakdown["avg_birth_weight_by_state"].median(), line_width = 5, line_dash = 'dash', line_color = "red")
        fig1.add_hline(y= breakdown['air_quality_score'].median(),line_width = 5, line_dash = 'dash', line_color = "blue")



        #chart that shows the breakdown of the second quadrant
        fig2 = px.scatter(second_quadrant,x ="avg_birth_weight_by_state" , y ="air_quality_score", color= "State",size = "avg_birth_weight_by_state",
        title = "Quadrant 2 Low ABW & High AQS  (median AQS = blue line, median ABW = red line)",
        labels = {"avg_birth_weight_by_state" : 'Average Birth Weight(lbs)', 'air_quality_score': 'Air Quality Score', 'State':"State"})
        fig2.add_vline(x= breakdown["avg_birth_weight_by_state"].median(), line_width = 5, line_dash = 'dash', line_color = "red")
        fig2.add_hline(y= breakdown['air_quality_score'].median(),line_width = 5, line_dash = 'dash', line_color = "blue")


        #chart that shows tbe breakdown of the third quadrant
        fig3 = px.scatter(third_quadrant,x ="avg_birth_weight_by_state" , y ="air_quality_score", color= "State",size = "avg_birth_weight_by_state",
        title = "Quadrant 3 Low ABW & Low AQS (median AQS = blue line, median ABW = red line)",
        labels = {"avg_birth_weight_by_state" : 'Average Birth Weight(lbs)', 'air_quality_score': 'Air Quality Score', 'State':"State"})
        fig3.add_vline(x= breakdown["avg_birth_weight_by_state"].median(), line_width = 5, line_dash = 'dash', line_color = "red")
        fig3.add_hline(y= breakdown['air_quality_score'].median(),line_width = 5, line_dash = 'dash', line_color = "blue")


        #chart that shows the breakdown of the fourth quadrant
        fig4 = px.scatter(fourth_quadrant,x ="avg_birth_weight_by_state" , y ="air_quality_score", color= "State", size = "avg_birth_weight_by_state",
        title = "Quadrant 4 High ABW & Low AQS (median air quality score = blue line, median average birth weight = red line)",
        labels = {"avg_birth_weight_by_state" : 'Average Birth Weight(lbs)', 'air_quality_score': 'Air Quality Score', 'State':"State"})
        fig4.add_vline(x= breakdown["avg_birth_weight_by_state"].median(), line_width = 5, line_dash = 'dash', line_color = "red")
        fig4.add_hline(y= breakdown['air_quality_score'].median(),line_width = 5, line_dash = 'dash', line_color = "blue")

        if output == "web":

            fig.show()
            fig1.show()
            fig2.show()
            fig3.show()
            fig4.show()
            logging.debug("writng state AQS & ABW breakdown to web")

        elif output == "pdf":
            fig.write_image("all_quadrants.pdf")
            fig1.write_image("quadrant_1.pdf")
            fig2.write_image("quadrant_2.pdf")
            fig3.write_image("quadrant_3.pdf")
            fig4.write_image("quadrant_4.pdf")
            logging.debug("writng state AQS & ABW breakdown to pdf")

        
    
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

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Analyze air quality data and birth rate data to find trends"
    )

    #store is for pdf or csv, render is for web
    parser.add_argument(choices =["store", "render"], dest='command',
    action ="store", type =str, help= "required command to execute")


    # option for render comand
    parser.add_argument("-w", "--web_output",dest="WEB",  metavar = '<web output>', choices =["air_quality",
    "birth_weight","combined","all"])

    # option for store command
    parser.add_argument("-c", "--csv", dest="CSV",  metavar = '<csv output>', choices =["air_quality",
    "birth_weight","combined","all"])
    
    # option for store command
    parser.add_argument("-p","--pdf", dest="PDF", metavar= '<pdf output', choices = ["air_quality",
    "birth_weight","combined","all"])

    # Parse the arguments given
    args = parser.parse_args()
    
    # Creates objects of the air quality data, birth data and combined
    air_quality_obj = Import_AirQuality_Data()
   
    
    

    # command line argument logic checks
    if (args.WEB == "air_quality" or args.WEB == "all")  and args.command == 'render':
        air_quality_obj.chloropleth_usa_map("air_quality_score", "web")
        air_quality_obj.extreme_aqi_values_sunburst("web")
  
    if (args.PDF == "air_quality" or args.PDF == "all") and args.command == 'store':
        air_quality_obj.chloropleth_usa_map("air_quality_score", "pdf")
        air_quality_obj.extreme_aqi_values_sunburst("pdf")
    
    if (args.CSV == "air_quality" or args.CSV == "all") and args.command == 'store':
        air_quality_obj.air_quality_csv()
    
    ####################################################################################
    #birth weight data 
    birth = BirthDataStats()


    if (args.WEB == "birth_weight" or args.WEB == "all") and args.command == 'render':
        birth.yearly_bw_state("web")
        birth.lowest_weight_in_state("web", "2018")
        birth.highest_weight_in_state("web", "2018")
   

    if (args.PDF == "birth_weight" or args.PDF == "all") and args.command == 'store':
        birth.yearly_bw_state("pdf")
        birth.lowest_weight_in_state("pdf", "2018")
        birth.highest_weight_in_state("pdf", "2018")


    if (args.CSV == "birth_weight" or args.CSV == "all") and args.command == 'store':
        birth.birth_csv()
    
   
####################################################################################
#combined data
    combined = BirthWeight_and_AirQuality(air_quality_obj, birth)

    if (args.WEB == "combined" or args.WEB == "all") and args.command == "render":
        combined.state_air_quality_bw_breakdown("web")
    

    if (args.PDF == "combined" or args.PDF == "all") and args.command == "store":
        combined.state_air_quality_bw_breakdown("pdf")
   

    if (args.CSV == "combined" or args.CSV == "all") and args.command == "store":
        combined.combined_csv()
  ##################################################################################
 #check for wrong options woth comand line args
    if (args.CSV and args.command == "render") or (args.PDF and args.command == "render") or (args.WEB and args.command == "store":
        print(" please use right option with required command 'render' -w --web, 'store' -p -- pdf or -c --csv ")



if __name__ == '__main__':
    main()
