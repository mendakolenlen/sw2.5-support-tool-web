import unittest
from unittest.mock import patch

from dice_logic import roll_check


class TestDiceLogic(unittest.TestCase):

    @patch("dice_logic.roll_2d6", return_value=(4, 3))
    def test_normal_success(self, mock_roll):
        result = roll_check(
            bonus=3,
            target=10,
        )

        self.assertEqual(result["dice1"], 4)
        self.assertEqual(result["dice2"], 3)
        self.assertEqual(result["dice_total"], 7)
        self.assertEqual(result["achievement"], 10)

        self.assertEqual(
            result["result_type"],
            "success",
        )

    @patch("dice_logic.roll_2d6", return_value=(2, 3))
    def test_normal_failure(self, mock_roll):
        result = roll_check(
            bonus=2,
            target=8,
        )

        self.assertEqual(result["dice_total"], 5)
        self.assertEqual(result["achievement"], 7)

        self.assertEqual(
            result["result_type"],
            "failure",
        )

    @patch("dice_logic.roll_2d6", return_value=(1, 1))
    def test_auto_failure(self, mock_roll):
        # ボーナスが非常に高くても1ゾロなら自動失敗
        result = roll_check(
            bonus=100,
            target=1,
        )

        self.assertEqual(result["dice_total"], 2)

        self.assertEqual(
            result["result_type"],
            "auto_failure",
        )

        self.assertEqual(
            result["result_text"],
            "自動失敗（1ゾロ）",
        )

    @patch("dice_logic.roll_2d6", return_value=(6, 6))
    def test_auto_success(self, mock_roll):
        # 達成値が目標値に届かなくても6ゾロなら自動成功
        result = roll_check(
            bonus=-100,
            target=100,
        )

        self.assertEqual(result["dice_total"], 12)

        self.assertEqual(
            result["result_type"],
            "auto_success",
        )

        self.assertEqual(
            result["result_text"],
            "自動成功（6ゾロ）",
        )


if __name__ == "__main__":
    unittest.main()
