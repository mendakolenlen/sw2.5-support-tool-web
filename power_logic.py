import random

from power_table import POWER_TABLE


MIN_CRITICAL = 8
MAX_CRITICAL = 13


def validate_power(power: int):
    """
    指定された威力が現在のPOWER_TABLEに存在するか確認する。
    """
    if power not in POWER_TABLE:
        available = ", ".join(str(value) for value in sorted(POWER_TABLE))

        raise ValueError(
            f"威力{power}は現在の威力表に存在しません。"
            f"使用可能な威力: {available}"
        )


def validate_critical(critical: int):
    """
    現在のツールで扱うC値の範囲を確認する。
    C値13は「クリティカルなし」として使用する。
    """
    if not MIN_CRITICAL <= critical <= MAX_CRITICAL:
        raise ValueError(
            f"C値は{MIN_CRITICAL}～{MAX_CRITICAL}で指定してください。"
        )


def roll_2d6():
    """
    2D6を振る。
    """
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    return dice1, dice2, dice1 + dice2


def get_power_value(power: int, dice_total: int):
    """
    2D6の出目に対応した威力表の値を取得する。

    出目2（1ゾロ）は通常の威力表参照を行わないため、
    この関数では受け付けない。
    """
    validate_power(power)

    if not 3 <= dice_total <= 12:
        raise ValueError(
            "威力表を参照できる出目は3～12です。"
        )

    return POWER_TABLE[power][dice_total - 2]


def roll_power(power: int, critical: int):
    """
    SW2.5の基本的な威力表ロールを行う。

    ・初回1ゾロ
        → 自動失敗

    ・出目がC値以上
        → クリティカルして振り足し

    ・振り足し中の1ゾロ
        → それまでの威力表結果を残して終了

    ・出目がC値未満
        → 終了

    戻り値には各ロールの履歴も含める。
    """

    validate_power(power)
    validate_critical(critical)

    history = []

    power_total = 0
    critical_count = 0
    roll_number = 1

    while True:
        dice1, dice2, dice_total = roll_2d6()

        # -------------------------
        # 1ゾロ
        # -------------------------
        if dice_total == 2:
            history.append(
                {
                    "roll_number": roll_number,
                    "dice1": dice1,
                    "dice2": dice2,
                    "dice_total": dice_total,
                    "power_value": None,
                    "is_critical": False,
                    "is_fumble": True,
                }
            )

            # 最初の威力表ロールで1ゾロ
            if roll_number == 1:
                end_reason = "auto_failure"

            # クリティカル後の振り足しで1ゾロ
            else:
                end_reason = "followup_fumble"

            break

        # -------------------------
        # 通常の威力表参照
        # -------------------------
        power_value = get_power_value(
            power=power,
            dice_total=dice_total,
        )

        is_critical = dice_total >= critical

        history.append(
            {
                "roll_number": roll_number,
                "dice1": dice1,
                "dice2": dice2,
                "dice_total": dice_total,
                "power_value": power_value,
                "is_critical": is_critical,
                "is_fumble": False,
            }
        )

        power_total += power_value

        # -------------------------
        # クリティカル
        # -------------------------
        if is_critical:
            critical_count += 1
            roll_number += 1
            continue

        # -------------------------
        # C値未満なので終了
        # -------------------------
        end_reason = "below_critical"
        break

    # -------------------------
    # 最終結果
    # -------------------------
    if end_reason == "auto_failure":
        result_type = "auto_failure"
        result_text = "自動失敗（1ゾロ）"

    elif end_reason == "followup_fumble":
        result_type = "success"
        result_text = "振り足し終了（1ゾロ）"

    else:
        result_type = "success"
        result_text = "威力表ロール終了"

    return {
        "power": power,
        "critical": critical,
        "history": history,
        "power_total": power_total,
        "critical_count": critical_count,
        "end_reason": end_reason,
        "result_type": result_type,
        "result_text": result_text,
    }
