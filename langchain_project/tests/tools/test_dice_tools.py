from ...tools.dice_tools import roll_dice


class TestDiceTools:
    def _extract_roll_value(self, result: str) -> int:
        """Extract the roll value from the dice result string."""
        return int(result.split()[1])

    def test_roll_dice(self):
        result = roll_dice.invoke({"sides": 6})
        assert isinstance(result, str)
        assert "rolled" in result.lower()
        assert "6" in result
        roll_value = self._extract_roll_value(result)
        assert 1 <= roll_value <= 6

    def test_roll_dice_invalid_sides(self):
        result = roll_dice.invoke({"sides": 0})
        assert "error" in result.lower() or "invalid" in result.lower()

    def test_roll_dice_randomness(self):
        results = []
        for _ in range(10):
            result = roll_dice.invoke({"sides": 20})
            roll_value = self._extract_roll_value(result)
            results.append(roll_value)
        # check that we get at least 3 different values (reasonable for 10 rolls on d20)
        unique_values = set(results)
        assert len(unique_values) >= 3, (
            f"Expected at least 3 unique values, got {unique_values}"
        )

    def test_roll_dice_different_sides(self):
        for sides in [4, 8, 12, 20]:
            result = roll_dice.invoke({"sides": sides})
            roll_value = self._extract_roll_value(result)
            assert 1 <= roll_value <= sides
            assert f"d{sides}" in result

    def test_roll_dice_minimum_sides(self):
        for _ in range(5):
            result = roll_dice.invoke({"sides": 2})
            roll_value = self._extract_roll_value(result)
            assert roll_value in [1, 2]
