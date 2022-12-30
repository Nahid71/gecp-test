
# [START functions_http_unit_test]
import unittest
from unittest.mock import Mock

import main

class TestMainApp(unittest.TestCase):
    def test_print_name(self):
        name = 'test'
        data = {'name': name}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # Call tested function
        self.assertEqual(main.hello_http(req), 'Hello {}!'.format(name))


    def test_print_hello_world(self):
        data = {}
        req = Mock(get_json=Mock(return_value=data), args=data)

        # Call tested function
        self.assertEqual(main.hello_http(req), 'Hello World!')
# [END functions_http_unit_test]


if __name__ == '__main__':
    unittest.main()