import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from maradmin_processor import MaradminProcessor

class TestMaradminProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MaradminProcessor()
        # Load contacts from the existing contacts.csv for realistic matching
        self.processor.contacts = [
            {'first_name': 'DOMINIC', 'last_name': 'DUARTE', 'full_name': 'DUARTE, DOMINIC', 'group': 'MFCC', 'mos': ''},
            {'first_name': 'STEVEN', 'last_name': 'VILLANUEVA', 'full_name': 'VILLANUEVA, STEVEN', 'group': 'MFCC', 'mos': ''}
        ]

    def test_search_enlisted_promotions_two_column(self):
        # Sample MARADMIN text snippet with two-column enlisted promotions
        maradmin_text = """
DUARTE        RL 0311/ 3579/BCD   TAYLOR         HK 0321/ 1357/EFG
THOMAS         SP 0331/ 2468/HIJ   MOORE          DM 0341/ 9876/KLM
DOMINIC       DUARTE  RL 0311/ 3579/BCD
STEVEN        VILLANUEVA  SP 0331/ 2468/HIJ
"""
        matches = self.processor.search_enlisted_promotions(maradmin_text, self.processor.contacts)
        matched_names = [m['contact']['full_name'] for m in matches]
        self.assertIn('DUARTE, DOMINIC', matched_names)
        self.assertIn('VILLANUEVA, STEVEN', matched_names)

    def test_search_1stlt_promotions(self):
        # Sample MARADMIN text snippet for officer promotions
        maradmin_text = """
THE FOLLOWING MARINES ARE PROMOTED TO THE GRADE OF 1STLT EFFECTIVE 1 JANUARY 2024

DOMINIC DUARTE
STEVEN VILLANUEVA
"""
        matches = self.processor.search_1stlt_promotions(maradmin_text, self.processor.contacts)
        matched_names = [m['contact']['full_name'] for m in matches]
        self.assertIn('DUARTE, DOMINIC', matched_names)
        self.assertIn('VILLANUEVA, STEVEN', matched_names)

if __name__ == '__main__':
    unittest.main()
