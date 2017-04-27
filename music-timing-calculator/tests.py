import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TimingCalculatorTests(unittest.TestCase):
    INPUT_IDS = ('tempo', 'beats', 'measures', 'num-digits')
    OUTPUT_IDS = ('one-beat', 'one-measure', 'song-length', 'song-length-min')
    
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()
        current_dir = '/'.join(os.getcwd().split(os.sep))
        cls.browser.get('file:///{}/index.html'.format(current_dir))
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
    
    def tearDown(self):
        self.browser.refresh()
    
    def send_input(self, input_dict):
        for k, v in input_dict.items():
            self.browser.find_element_by_id(k).send_keys(v)
    
    def get_element_value(self, elem_id):
        return self.browser.find_element_by_id(elem_id).get_attribute('value')
    
    def assert_element_values(self, expected_dict):
        for k, v in expected_dict.items():
            self.assertEqual(self.get_element_value(k), v)
    
    def test_shows_placeholder_zeroes_on_start(self):
        self.assert_element_values({
            'one-beat': '0 sec',
            'one-measure': '0 sec',
            'song-length': '0 sec',
            'song-length-min': '0 min 0 sec',
        })
    
    def test_computes_expected_integral_calculations(self):
        self.send_input({
            'tempo': '60',
            'beats': '4',
            'measures': '8',
        })
        self.assert_element_values({
            'one-beat': '1 sec',
            'one-measure': '4 sec',
            'song-length': '32 sec',
            'song-length-min': '0 min 32 sec',
        })
    
    def test_blank_input_allowed(self):
        self.send_input({'tempo': '60'})
        self.assert_element_values({
            'one-beat': '1 sec',
            'one-measure': '0 sec',
            'song-length': '0 sec',
            'song-length-min': '0 min 0 sec',
        })
    
    def test_enter_key_submits(self):
        self.send_input({'tempo': '60'})
        self.send_input({'tempo': Keys.ENTER})
        self.assert_element_values({'one-beat': '1 sec'})
    
    def test_omitting_decimal_places_allows_mixed_precision(self):
        self.send_input({
            'tempo': '128',
            'beats': '6',
            'measures': '32',
        })
        self.assert_element_values({
            'one-beat': '0.46875 sec',
            'one-measure': '2.8125 sec',
            'song-length': '90 sec',
            'song-length-min': '1 min 30 sec',
        })
    
    def test_precision_enforced_when_decimal_places_specified(self):
        self.send_input({
            'tempo': '128',
            'beats': '6',
            'measures': '32',
            'num-digits': '3',
        })
        self.assert_element_values({
            'one-beat': '0.469 sec',
            'one-measure': '2.813 sec',
            'song-length': '90.000 sec',
            'song-length-min': '1 min 30.000 sec',
        })
    
    def test_reset_button_recreates_initial_state(self):
        field_ids = self.INPUT_IDS + self.OUTPUT_IDS
        initial_state = {k: self.get_element_value(k) for k in field_ids}
        self.test_precision_enforced_when_decimal_places_specified()
        self.browser.find_element_by_id('reset').click()
        current_state = {k: self.get_element_value(k) for k in field_ids}
        for elem_id in initial_state:
            self.assertEqual(initial_state[elem_id], current_state[elem_id])
    
    def test_can_enter_floats_as_input(self):
        self.send_input({
            'tempo': '67.5',
            'beats': '2.75',
            'measures': '16.0909',
            'num-digits': '4',
        })
        self.assert_element_values({
            'one-beat': '0.8889 sec',
            'one-measure': '2.4444 sec',
            'song-length': '39.3333 sec',
            'song-length-min': '0 min 39.3333 sec',
        })
    
    def test_negative_input_is_invalid(self):
        for input_id, output_id in zip(self.INPUT_IDS[:3], self.OUTPUT_IDS[:3]):
            self.send_input({input_id: '-1'})
            self.assert_element_values({output_id: '0 sec'})
            self.send_input({input_id: Keys.BACKSPACE * 2})
            self.send_input({input_id: '1'})
        self.send_input({'num-digits': '-1'})
        self.assert_element_values({'song-length-min': '1 min 0 sec'})
    
    def test_decimal_places_above_20_invalid(self):
        self.send_input({'num-digits': '21'})
        self.assert_element_values({'one-beat': '0.00 sec'})  # "2" seen first
    
    def test_tempo_of_0_bpm_is_invalid(self):
        self.send_input({'tempo': '0'})
        self.assert_element_values({'one-beat': '0 sec'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
