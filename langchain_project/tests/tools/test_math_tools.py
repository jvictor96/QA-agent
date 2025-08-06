from ...tools.math_tools import calculate_square_root, calculate_power


class TestMathTools:
    def test_calculate_square_root(self):
        result = calculate_square_root.invoke({"number": 16})
        assert isinstance(result, str)
        assert "4.0" in result or "4" in result

    def test_calculate_square_root_negative(self):
        result = calculate_square_root.invoke({"number": -1})
        assert "error" in result.lower() or "invalid" in result.lower()

    def test_calculate_power(self):
        result = calculate_power.invoke({"base": 2, "exponent": 3})
        assert isinstance(result, str)
        assert "8" in result

    def test_calculate_power_zero_exponent(self):
        result = calculate_power.invoke({"base": 5, "exponent": 0})
        assert "1" in result
