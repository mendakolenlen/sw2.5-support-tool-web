import unittest
from unittest.mock import patch

from power_logic import (
    get_power_value,
    roll_power,
)


class TestPowerLogic(unittest.TestCase):

    @patch(
        "power_logic.roll_2d6",
        return_value=(1, 1, 2),
    )
    def test_initial_fumble(self, mock_roll):
        """
        最初の威力表ロールで1ゾロ。
        → 自動失敗
        """

        result = roll_power(
            power=25,
            critical=10,
        )

        self.assertEqual(
            result["result_type"],
            "auto_failure",
        )

        self.assertEqual(
            result["end_reason"],
            "auto_failure",
        )

        self.assertEqual(
            result["power_total"],
            0,
        )

        self.assertEqual(
            result["critical_count"],
            0,
        )

        self.assertTrue(
            result["history"][0]["is_fumble"]
        )

    @patch(
        "power_logic.roll_2d6",
        return_value=(5, 4, 9),
    )
    def test_normal_power_roll(self, mock_roll):
        """
        威力25
        出目9
        → 威力表8
        C値10未満なので終了
        """

        result = roll_power(
            power=25,
            critical=10,
        )

        self.assertEqual(
            result["power_total"],
            8,
        )

        self.assertEqual(
            result["critical_count"],
            0,
        )

        self.assertEqual(
            result["end_reason"],
            "below_critical",
        )

    @patch(
        "power_logic.roll_2d6",
        side_effect=[
            (5, 6, 11),
            (5, 4, 9),
        ],
    )
    def test_single_critical(self, mock_roll):
        """
        威力25 / C値10

        11 → 威力表9 → クリティカル
        9  → 威力表8 → 終了

        合計17
        """

        result = roll_power(
            power=25,
            critical=10,
        )

        self.assertEqual(
            result["power_total"],
            17,
        )

        self.assertEqual(
            result["critical_count"],
            1,
        )

        self.assertEqual(
            len(result["history"]),
            2,
        )

        self.assertTrue(
            result["history"][0]["is_critical"]
        )

        self.assertFalse(
            result["history"][1]["is_critical"]
        )

    @patch(
        "power_logic.roll_2d6",
        side_effect=[
            (6, 6, 12),
            (5, 5, 10),
            (3, 4, 7),
        ],
    )
    def test_multiple_criticals(self, mock_roll):
        """
        威力20 / C値10

        12 → 10 → クリティカル
        10 → 8  → クリティカル
         7 → 5  → 終了

        合計23
        """

        result = roll_power(
            power=20,
            critical=10,
        )

        self.assertEqual(
            result["power_total"],
            23,
        )

        self.assertEqual(
            result["critical_count"],
            2,
        )

        self.assertEqual(
            len(result["history"]),
            3,
        )

    @patch(
        "power_logic.roll_2d6",
        side_effect=[
            (5, 6, 11),
            (1, 1, 2),
        ],
    )
    def test_fumble_after_critical(self, mock_roll):
        """
        クリティカル後の振り足しで1ゾロ。

        最初に得た威力表9は残り、
        振り足しだけ終了する。
        """

        result = roll_power(
            power=25,
            critical=10,
        )

        self.assertEqual(
            result["power_total"],
            9,
        )

        self.assertEqual(
            result["critical_count"],
            1,
        )

        self.assertEqual(
            result["end_reason"],
            "followup_fumble",
        )

        self.assertEqual(
            len(result["history"]),
            2,
        )

        self.assertTrue(
            result["history"][1]["is_fumble"]
        )

    @patch(
        "power_logic.roll_2d6",
        return_value=(6, 6, 12),
    )
    def test_critical_13_never_critical(self, mock_roll):
        """
        C値13なら2D6ではクリティカルしない。
        """

        result = roll_power(
            power=50,
            critical=13,
        )

        self.assertEqual(
            result["power_total"],
            15,
        )

        self.assertEqual(
            result["critical_count"],
            0,
        )

        self.assertFalse(
            result["history"][0]["is_critical"]
        )

    def test_invalid_power(self):
        with self.assertRaises(ValueError):
            roll_power(
                power=51,
                critical=10,
         )

    def test_invalid_critical_low(self):
        with self.assertRaises(ValueError):
            roll_power(
                power=20,
                critical=7,
            )

    def test_invalid_critical_high(self):
        with self.assertRaises(ValueError):
            roll_power(
                power=20,
                critical=14,
            )

    def test_power_table_cannot_lookup_fumble(self):
        """
        出目2を通常の威力表値として取得できないことを確認。
        """

        with self.assertRaises(ValueError):
            get_power_value(
                power=20,
                dice_total=2,
            )


    @patch(
        "power_logic.roll_2d6",
        return_value=(5, 4, 9),
    )
    def test_damage_bonus(self, mock_roll):
        """
        通常の威力表結果に追加ダメージが
        1回だけ加算されることを確認する。

        威力25・出目9
        → 威力表8

        追加ダメージ7
        → 最終ダメージ15
        """

        result = roll_power(
            power=25,
            critical=10,
            damage_bonus=7,
        )

        self.assertEqual(
            result["power_total"],
            8,
        )

        self.assertEqual(
            result["damage_bonus"],
            7,
        )

        self.assertEqual(
            result["final_damage"],
            15,
        )


    @patch(
        "power_logic.roll_2d6",
        side_effect=[
            (5, 6, 11),
            (5, 4, 9),
        ],
    )
    def test_damage_bonus_added_once_after_critical(
        self,
        mock_roll,
    ):
        """
        クリティカルしても、
        追加ダメージは最後に1回だけ加える。

        威力25 / C値10

        11 → 威力表9 → クリティカル
         9 → 威力表8 → 終了

        威力表合計17
        追加ダメージ5

        最終ダメージ22
        """

        result = roll_power(
            power=25,
            critical=10,
            damage_bonus=5,
        )

        self.assertEqual(
            result["power_total"],
            17,
        )

        self.assertEqual(
            result["critical_count"],
            1,
        )

        self.assertEqual(
            result["damage_bonus"],
            5,
        )

        self.assertEqual(
            result["final_damage"],
            22,
        )


    @patch(
        "power_logic.roll_2d6",
        return_value=(1, 1, 2),
    )
    def test_fumble_does_not_calculate_damage(
        self,
        mock_roll,
    ):
        """
        初回1ゾロの場合は、
        追加ダメージがあってもダメージを算出しない。
        """

        result = roll_power(
            power=25,
            critical=10,
            damage_bonus=100,
        )

        self.assertEqual(
            result["result_type"],
            "auto_failure",
        )

        self.assertEqual(
            result["power_total"],
            0,
        )

        self.assertEqual(
            result["damage_bonus"],
            100,
        )

        self.assertIsNone(
            result["final_damage"]
        )


if __name__ == "__main__":
    unittest.main()
