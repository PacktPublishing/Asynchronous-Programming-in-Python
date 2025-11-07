import unittest
import solution1

class TestSolution1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = {"name":'New York','lat':40.6943,'lng':-73.9249}
        cls.dest = {"name":'Los Angeles','lat':34.1141,'lng':-118.4068}
        cls.dest2 = {"name":'Tokio','lat':35.6897,'lng':139.6922}
        
    def test_distance(self):
        self.assertEqual(solution1.great_circle_distance((self.source, self.dest,)), 2133.3450848571965)
        
    def test_cities_into_tuples(self):
        cities = [self.source, self.dest, self.dest2]
        tuples = [(self.source, self.dest,),(self.dest, self.dest2)]
        self.assertEqual(solution1.cities_into_tuples(cities), tuples)

if __name__ == '__main__':
    unittest.main()