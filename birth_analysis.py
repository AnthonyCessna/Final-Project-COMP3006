from dataclasses import dataclass
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

#needs logging, command line arguments and more bling on the charts

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
    BirthDataStats() loads the birth_data.csv, wrangles some of the dataclass
    since I am only using 4 fields: year, county, state, average_birth_weight.
    """

    def __init__(self):
        self.birth_data()

    def __repr__(self):
        return "AutoMPGData()"

    def __iter__(self):
        return iter(self.data)

    #default sort for now nit sure if we need it
    def sort(self):
        return self.data.sort()


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
        self.df = pd.DataFrame(self.data)
        return self.df

    def avg_bw_county(self):
        x = self.pandas_df().groupby("county").mean()
        plt.plot(x["average_birth_weight"],'pg')
        plt.show()

    def max_bw_county(self):
        x = self.pandas_df().groupby("county").max()
        plt.plot(x["average_birth_weight"],'pg')
        plt.show()

    def min_bw_county(self):
        x = self.pandas_df().groupby("county").max()
        plt.plot(x["average_birth_weight"],'pg')
        plt.show()

    def avg_bw_state(self):
        plt.plot(self.pandas_df().groupby("state").mean()["average_birth_weight"])
        plt.show()

    def max_bw_state(self):
        x = self.pandas_df().groupby("state").min()
        plt.plot(x["average_birth_weight"])
        plt.show()

    def min_bw_state(self):
        x = self.pandas_df().groupby("state").min()
        plt.plot(x["average_birth_weight"])
        plt.show()

    def avg_bw_year(self):
        x = self.pandas_df().groupby("year").mean()
        plt.plot(x["average_birth_weight"],'p')
        plt.show()

    def max_bw_year(self):
        x = self.pandas_df().groupby("year").max()
        plt.plot(x["average_birth_weight"],'p')
        plt.show()

    def min_bw_year(self):
        x = self.pandas_df().groupby("year").min()
        plt.plot(x["average_birth_weight"])
        plt.show()



def main():
    birth = BirthDataStats()
    birth.avg_bw_county()
    birth.avg_bw_state()
    birth.avg_bw_year()
    birth.max_bw_county()
    birth.max_bw_state()
    birth.max_bw_year()
    birth.min_bw_county()
    birth.min_bw_state()
    birth.min_bw_year()




main()
