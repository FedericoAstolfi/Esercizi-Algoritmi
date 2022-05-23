import unittest
import random

import viaggiatore
import math

class TestMyViaggiatore(unittest.TestCase):

    def setUp(self):
        print('before')

    def tearDown(self):
        print('after')

    def distance_test(self):
        '''testo la function distance senza dare una seconda ascissa e una seconda ordinata
        con cui fare la sottrazione, ma vedo solo se mi calcola bene la radice quadrata dell'input'''
        a=[random.random() for i in range(100)]
        c=[1+random.random() for i in range(100)]
        b=[math.sqrt(x**2-y**2) for x,y in zip(c,a)]
        d=[viaggiatore.distance(x,0,y,0) for x,y in zip(a,b)]
        for x,y in zip(c,d):
            self.assertEqual(x,y)

#    def roulette_test(self):
#       '''testo roulette sampling'''
#        pass

    def get_fitness_test(self):
        pass
        



if __name__ == '__main__':
    print('main')
    unittest.main()
    