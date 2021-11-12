import unittest

from air_quality_and_birth_weight_analysis import *

class TestAirQuality_obj(unittest.TestCase):
    
    def test_lt(self):
        
        better_air_quality = AirQuality_obj("Washington", "Spokane", 2018, 250, 20, 5, 0, 0, 100)
        worse_air_quality = AirQuality_obj("California", "LA", 2018, 100, 100, 50, 20, 10, 200)

      
        assert better_air_quality < worse_air_quality


class TestImport_AirQuality_Data(unittest.TestCase):

   pass
                
if __name__ == '__main__':
    unittest.main()

