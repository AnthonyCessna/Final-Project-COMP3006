import unittest

from air_quality_and_birth_weight_analysis import *

class TestAirQuality_obj(unittest.TestCase):
    
    def test_lt(self):
        
        better_air_quality = AirQuality_obj("Washington", "Spokane", 2018, 250, 20, 5, 0, 0, 100)
        worse_air_quality = AirQuality_obj("California", "LA", 2018, 100, 100, 50, 20, 10, 200)
      
        assert better_air_quality < worse_air_quality

    def test_gt(self):

        better_air_quality = AirQuality_obj("Washington", "Spokane", 2018, 250, 20, 5, 0, 0, 100)
        worse_air_quality = AirQuality_obj("California", "LA", 2018, 100, 100, 50, 20, 10, 200)
      
        assert worse_air_quality > better_air_quality 

class TestImport_AirQuality_Data(unittest.TestCase):

    def test_worst_air_quality_in_state(self):
        obj = Import_AirQuality_Data()
        worst_air_washington = obj.worst_air_quality_in_state("Washington")

        self.assertRaises(ValueError, obj.worst_air_quality_in_state, "Japan") 

        assert worst_air_washington == "Chelan"

    def test_best_air_quality_in_state(self):
        obj = Import_AirQuality_Data()
        best_air_washington = obj.best_air_quality_in_state("Washington")
        self.assertRaises(ValueError, obj.best_air_quality_in_state, "Japan")

        assert best_air_washington == "Clark"
                
if __name__ == '__main__':
    unittest.main()

