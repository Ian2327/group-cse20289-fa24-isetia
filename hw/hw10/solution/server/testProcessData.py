import unittest
from processdata import match_time, match_date, match_filters, filter_data, process_data 

class TestProcessData(unittest.TestCase):
    def test_match_time(self):
        self.assertTrue(match_time("2024-12-05T14:00:00", "*"))
        self.assertTrue(match_time("2024-05-03T02:26:16-04:00", 2))
        self.assertFalse(match_time("2024-05-03T02:26:16-04:00", 1)) 
    def test_match_date(self):
        self.assertTrue(match_date("2024-12-05T14:00:00", "2024-12-05"))
        self.assertFalse(match_date("2024-12-05T14:00:00", "2024-12-06"))
        self.assertTrue(match_date("2024-12-05T14:00:00", "2024-*-05"))
        self.assertTrue(match_date("2024-12-05T14:00:00", "*-12-*"))
        self.assertFalse(match_date("2024-12-05T14:00:00", "2023-*-*"))
    def test_match_filters(self):
        record = {"user": "John", "action": "login", "status": "success"}
        self.assertTrue(match_filters(record, "user=John;action=login"))
        self.assertFalse(match_filters(record, "user=Jane;action=login"))
        self.assertTrue(match_filters(record, "user=John;status=success"))
        self.assertFalse(match_filters(record, "user=John;status=failure"))
    def test_filter_data(self):
        data = [
            {"timestamp": "2024-12-05T14:00:00", "user": "John", "action": "login"},
            {"timestamp": "2024-12-05T15:00:00", "user": "Jane", "action": "logout"},
            {"timestamp": "2024-12-06T14:00:00", "user": "John", "action": "update"},
        ]
        result = filter_data(data, "2024-12-05", "14", "user=John;action=login")
        self.assertEqual(result, [{"timestamp": "2024-12-05T14:00:00", "user": "John", "action": "login"}])
        
        result = filter_data(data, "2024-*-*", "*", "user=Jane")
        self.assertEqual(result, [{"timestamp": "2024-12-05T15:00:00", "user": "Jane", "action": "logout"}])
        
        result = filter_data(data, "*-*-*", "*", "user=John")
        self.assertEqual(result, [
            {"timestamp": "2024-12-05T14:00:00", "user": "John", "action": "login"},
            {"timestamp": "2024-12-06T14:00:00", "user": "John", "action": "update"},
        ])

    def test_process_data(self):
        data = [
            {"user": "John", "action": "login"},
            {"user": "Jane", "action": "logout"},
            {"user": "John", "action": "update"},
        ]
        filters = {"user": "John"}
        result = process_data(data, filters)
        self.assertEqual(result, [
            {"user": "John", "action": "login"},
            {"user": "John", "action": "update"},
        ])
        
        filters = {"action": "logout"}
        result = process_data(data, filters)
        self.assertEqual(result, [{"user": "Jane", "action": "logout"}])
        
        result = process_data(data, {})
        self.assertEqual(result, data)

        result = process_data(data, {"user": "Jane", "action": "login"})
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
