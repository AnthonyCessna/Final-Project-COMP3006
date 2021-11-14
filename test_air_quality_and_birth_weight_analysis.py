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
  
class TestBirthObj(unittest.TestCase):

    def test_lt(self):
        high  = (2016,"Davis County", "UT", 7.9)
        low = (2016,"Davis County", "UT", 7.4)
        message = "high is not less than low"
        self.assertLess(low,high,message)

        high  = (2016,"Weber County", "UT", 9.9)
        low = (2016,"Weber County", "UT", 1.4)
        message = "high is not less than low"
        self.assertLess(low,high,message)

        high  = (2017,"Weber County", "UT", 9.9)
        low = (2016,"Weber County", "UT", 9.9)
        message = "high is not less than low"
        self.assertLess(low,high,message)

    def test_gt(self):
        high  = (2016,"Davis County", "UT", 7.9)
        low = (2016,"Davis County", "UT", 7.4)
        message = "high is not greater than low"
        self.assertGreater(high,low ,message)

        high  = (2016,"Weber County", "UT", 7.5)
        low = (2016,"Weber County", "UT", 7.49999)
        message = "high is not greater than low"
        self.assertGreater(high,low ,message)

        high  = (2018,"Weber County", "UT", 7.555)
        low = (2016,"Weber County", "UT", 7.555)
        message = "high is not greater than low"
        self.assertGreater(high,low ,message)

    def test_eq(self):
        ob1  = (2016,"Davis County", "UT", 7.9)
        ob2 = (2016,"Davis County", "UT", 7.9)
        message = "ob1 doest not equal ob2"
        self.assertEqual(ob1,ob2,message)

        ob1  = (2016,"Cool guy County", "UT", 7.999)
        ob2 = (2016,"Cool guy County", "UT", 7.999)
        message = "ob1 doest not equal ob2"
        self.assertEqual(ob1,ob2,message)
                
if __name__ == '__main__':
    unittest.main()

