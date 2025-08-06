from unittest.mock import Mock, patch

from ...tools.weather_tools import get_current_weather


class TestWeatherTools:
    @patch.dict("os.environ", {"WEATHERSTACK_API_KEY": "test_api_key"})
    @patch("langchain_project.tools.weather_tools.requests.get")
    def test_get_current_weather(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "current": {
                "temperature": 20,
                "humidity": 60,
                "weather_descriptions": ["clear sky"],
                "observation_time": "12:00 PM",
            },
            "location": {"name": "Test City", "country": "Test Country"},
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        result = get_current_weather.invoke({"location": "Test City"})
        assert isinstance(result, str)
        assert "Test City" in result
        assert "20" in result

    @patch.dict("os.environ", {"WEATHERSTACK_API_KEY": "test_api_key"})
    @patch("langchain_project.tools.weather_tools.requests.get")
    def test_get_current_weather_not_found_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = get_current_weather.invoke({"location": "Nonexistent City"})
        assert "error" in result.lower()

    def test_get_current_weather_no_api_key_error(self):
        with patch.dict("os.environ", {}, clear=True):
            result = get_current_weather.invoke({"location": "Test City"})
            assert "WEATHERSTACK_API_KEY" in result
            assert "not found" in result.lower()
