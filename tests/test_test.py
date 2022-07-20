from unittest import TestCase
from bs4 import BeautifulSoup

from test import closest_product_result


class Test(TestCase):
    def test_closest_product_result(self):
        ml = """
        <button>
        <div>Gala Apple</div>
        <div class='css-1kh7mkb'>$1.29/lb</div>
        </button>
        """

        mock_soup = BeautifulSoup(ml, 'html.parser')

        expected_result = (['Gala Apple'], ['$1.29'])

        actual_result = closest_product_result('Gala Apple', mock_soup)

        assert actual_result == expected_result