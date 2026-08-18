import random


def roll_2d6():
    """2D6を振り、それぞれの出目を返す。"""
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    return dice1, dice2


def roll_check(bonus: int, target: int):
    """
    SW2.5の基本的な判定を行う。

    1ゾロ → 自動失敗
    6ゾロ → 自動成功
    その他 → 達成値 >= 目標値なら成功
    """

    dice1, dice2 = roll_2d6()

    dice_total = dice1 + dice2
    achievement = dice_total + bonus

    # 1ゾロ：自動失敗
    if dice_total == 2:
        result_type = "auto_failure"
        result_text = "自動失敗（1ゾロ）"

    # 6ゾロ：自動成功
    elif dice_total == 12:
        result_type = "auto_success"
        result_text = "自動成功（6ゾロ）"

    # 通常判定
    elif achievement >= target:
        result_type = "success"
        result_text = "成功"

    else:
        result_type = "failure"
        result_text = "失敗"

    return {
        "dice1": dice1,
        "dice2": dice2,
        "dice_total": dice_total,
        "bonus": bonus,
        "achievement": achievement,
        "target": target,
        "result_type": result_type,
        "result_text": result_text,
    }
