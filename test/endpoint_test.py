import datetime
from unittest import (main, TestCase)

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymvlapi.endpoint import (MarketingVillasApi)


class EndpointTestCase(TestCase):
    def setUp(self):
        self.mvlapi = MarketingVillasApi("", "")

    def sneaky_mock_function(self, *args, **kwargs):
        return self.sample_response_bytes


class EndpointConstructionTestCase(EndpointTestCase):
    def test_constructs_simple_endpoint(self):
        result = self.mvlapi._construct_endpoint( endpoint=("TestEndpoint", [],) )
        self.assertEqual("http://ws.marketingvillas.com/partners.asmx/TestEndpoint", result)

    def test_constructs_simple_endpoint_with_leading_slash(self):
        result = self.mvlapi._construct_endpoint( endpoint=("/TestEndpointLeadingSlash",[],) )
        self.assertEqual("http://ws.marketingvillas.com/partners.asmx/TestEndpointLeadingSlash", result)

    def test_constructs_endpoint_with_query(self):
        result = self.mvlapi._construct_endpoint( endpoint=("TestEndpointWithQuery", [],), get_params={ "key": "value" })
        self.assertEqual("http://ws.marketingvillas.com/partners.asmx/TestEndpointWithQuery?key=value", result)


class GetTimeTokenTestCase(EndpointTestCase):
    def setUp(self):
        super(GetTimeTokenTestCase, self).setUp()
        self.sample_response_token = "1e8046523db8ad1d376df5e1447f3b4a"
        self.sample_response_bytes = b'<?xml version="1.0" encoding="utf-8"?>\r\n<string xmlns="http://ws.marketingvillas.com/partners/">1e8046523db8ad1d376df5e1447f3b4a</string>'

    def test_converts_time_bytes_xml_to_string(self):
        self.mvlapi._get_time_token = self.sneaky_mock_function

        self.assertEqual(self.mvlapi._get_time_token(), self.sample_response_bytes, "Did not call mock function")
        self.assertEqual(self.mvlapi.get_time_token(), self.sample_response_token, "Did not convert XML to token string")


class GetMd5TokenTestCase(EndpointTestCase):
    def setUp(self):
        super(GetMd5TokenTestCase, self).setUp()
        self.sample_response_token = "0c959320c1e7804cbd91c9125b1c1d21"
        self.sample_response_bytes = b'<?xml version="1.0" encoding="utf-8"?>\r\n<string xmlns="http://ws.marketingvillas.com/partners/">0c959320c1e7804cbd91c9125b1c1d21</string>'

    def test_converts_md5_bytes_xml_to_string(self):
        self.mvlapi._get_md5_token = self.sneaky_mock_function

        self.assertEqual(self.mvlapi._get_md5_token(), self.sample_response_bytes, "Did not call mock function")
        self.assertEqual(self.mvlapi.get_md5_token(), self.sample_response_token, "Did not convert XML to token string")


class GetVillaListTestCase(EndpointTestCase):
    def setUp(self):
        super(GetVillaListTestCase, self).setUp()
        self.sample_response_list = [
            {
                "villa_id": "39LightHouse",
                "sort_name": "39 Galle Fort",
                "base_url": "39-galle-fort",
                "name": "No. 39 Galle Fort"
            },
            {
                "villa_id": "Adasa",
                "sort_name": "Adasa",
                "base_url": "laksmana-estate-villa-adasa",
                "name": "Villa Adasa"
            }
        ]
        self.sample_response_bytes = b'<?xml version="1.0" encoding="utf-8"?>\r\n<Villas>\r\n  <Villa villaid="39LightHouse" sortname="39 Galle Fort" baseurl="39-galle-fort">No. 39 Galle Fort</Villa>\r\n  <Villa villaid="Adasa" sortname="Adasa" baseurl="laksmana-estate-villa-adasa">Villa Adasa</Villa>\r\n</Villas>'

    def test_converts_villa_list_correctly(self):
        self.mvlapi._get_villa_list = self.sneaky_mock_function

        self.assertEqual(self.mvlapi._get_villa_list(), self.sample_response_bytes, "Did not call mock function")
        self.assertEqual(self.mvlapi.get_villa_list(), self.sample_response_list, "Failed to convert XML bytes to list")


class GetVillaRatesTestCase(EndpointTestCase):
    def setUp(self):
        super(GetVillaRatesTestCase, self).setUp()
        self.sample_response_dict = {
            "villa_id": "Arnalaya",
            "rate_name": "Standard Rate",
            "rates": [
                {
                    "from": datetime.datetime(2017, 2, 5),
                    "to": datetime.datetime(2017, 3, 31),
                    "amount": 1895.00,
                    "min_stay": 2,
                    "percent_tax": 10.00,
                    "percent_rate": 5.00
                },
                {
                    "from": datetime.datetime(2017, 4, 1),
                    "to": datetime.datetime(2017, 4, 12),
                    "amount": 2095.00,
                    "min_stay": 2,
                    "percent_tax": 10.00,
                    "percent_rate": 5.00
                }
            ]
        }
        self.sample_response_bytes = b'<?xml version="1.0" encoding="utf-8"?>\r\n<Villa villaid="Arnalaya">\r\n  <Rates ratenameid="983">\r\n    <RateName><![CDATA[Standard Rate]]></RateName>\r\n    <Rate>\r\n      <From>2017-02-05T00:00:00</From>\r\n      <To>2017-03-31T00:00:00</To>\r\n      <Amount>1895.00</Amount>\r\n      <MinimumNightStay>2</MinimumNightStay>\r\n      <PercentTax>10.00</PercentTax>\r\n      <PercentRate>5.00</PercentRate>\r\n    </Rate>\r\n    <Rate>\r\n      <From>2017-04-01T00:00:00</From>\r\n      <To>2017-04-12T00:00:00</To>\r\n      <Amount>2095.00</Amount>\r\n      <MinimumNightStay>2</MinimumNightStay>\r\n      <PercentTax>10.00</PercentTax>\r\n      <PercentRate>5.00</PercentRate>\r\n    </Rate>\r\n  </Rates>\r\n</Villa>'

    def test_converts_villa_rates_correctly(self):
        self.mvlapi._get_villa_rates = self.sneaky_mock_function

        self.assertEqual(self.mvlapi._get_villa_rates("Arnalaya"), self.sample_response_bytes, "Did not call mock function")
        self.assertEqual(self.mvlapi.get_villa_rates("Arnalaya"), self.sample_response_dict, "Did not parse XML to dictionary")


class GetVillaUnavailabilityTestCase(EndpointTestCase):
    def setUp(self):
        super(GetVillaUnavailabilityTestCase, self).setUp()
        self.sample_response_dict = {
            "unavailable_dates": [
                {
                    "from": datetime.datetime(2017, 2, 24),
                    "to": datetime.datetime(2017, 3, 3)
                },
                {
                    "from": datetime.datetime(2018, 2, 14),
                    "to": datetime.datetime(2018, 2, 19)
                }
            ]
        }
        self.sample_response_bytes = b'<?xml version="1.0" encoding="utf-8"?>\r\n<Availability>\r\n  <UnavailableDates villaid="arnalaya">\r\n    <UnavailableDate>\r\n      <From>2017-02-24</From>\r\n      <To>2017-03-03</To>\r\n    </UnavailableDate>\r\n    <UnavailableDate>\r\n      <From>2018-02-14</From>\r\n      <To>2018-02-19</To>\r\n    </UnavailableDate>\r\n  </UnavailableDates>\r\n</Availability>'

    def test_converts_villa_availability_correctly(self):
        self.mvlapi._get_villa_unavailable_dates = self.sneaky_mock_function

        self.assertEqual(self.mvlapi._get_villa_unavailable_dates("Arnalaya"), self.sample_response_bytes, "Did not call mock function")
        self.assertEqual(self.mvlapi.get_villa_unavailable_dates("Arnalaya"), self.sample_response_dict, "Did not parse XML to dictionary")


if __name__ == "__main__":
    main()

