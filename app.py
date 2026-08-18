import streamlit as st

from dice_logic import roll_check
from power_logic import roll_power
from power_table import POWER_TABLE


# -------------------------
# ページ設定
# -------------------------
st.set_page_config(
    page_title="SW2.5 Support Tool",
    page_icon="🎲",
    layout="centered",
)


# -------------------------
# 判定用ダイス
# -------------------------
def show_check_dice():
    st.header("判定用ダイス")

    st.caption(
        "2D6にボーナスを加え、目標値に対する判定を行います。"
    )

    col1, col2 = st.columns(2)

    with col1:
        bonus = st.number_input(
            "ボーナス",
            value=0,
            step=1,
            key="check_bonus",
        )

    with col2:
        target = st.number_input(
            "目標値",
            value=10,
            step=1,
            key="check_target",
        )

    if st.button(
        "🎲 判定する",
        key="check_roll",
        use_container_width=True,
        type="primary",
    ):
        result = roll_check(
            bonus=bonus,
            target=target,
        )

        st.subheader("判定結果")

        st.write(
            f"**出目：{result['dice1']} + {result['dice2']} "
            f"= {result['dice_total']}**"
        )

        st.write(
            f"達成値："
            f"{result['dice_total']} "
            f"{result['bonus']:+} "
            f"= **{result['achievement']}**"
        )

        st.write(
            f"目標値：**{result['target']}**"
        )

        result_type = result["result_type"]

        if result_type == "auto_failure":
            st.error(result["result_text"])

        elif result_type == "auto_success":
            st.success(result["result_text"])

        elif result_type == "success":
            st.success(result["result_text"])

        else:
            st.error(result["result_text"])


# -------------------------
# 威力表ダイス
# -------------------------
def show_power_dice():
    st.header("威力表ダイス")

    st.caption(
        "威力とC値を指定して威力表をロールします。"
        "C値以上の出目でクリティカルします。"
    )

    col1, col2 = st.columns(2)

    with col1:
        power = st.selectbox(
            "威力",
            options=sorted(POWER_TABLE.keys()),
            index=10,
            key="power_value",
        )

    with col2:
        critical = st.number_input(
            "C値",
            min_value=8,
            max_value=13,
            value=10,
            step=1,
            key="critical_value",
            help="C値13では通常クリティカルしません。",
        )

    damage_bonus = st.number_input(
        "追加ダメージ",
        value=0,
        step=1,
        key="damage_bonus",
        help="威力表の最終結果に加算する追加ダメージです。",
    )

    if st.button(
        "🎲 威力表を振る",
        key="power_roll",
        use_container_width=True,
        type="primary",
    ):
        result = roll_power(
            power=power,
            critical=critical,
            damage_bonus=damage_bonus,
        )

        st.subheader("威力表結果")

        # 初回1ゾロ
        if result["result_type"] == "auto_failure":
            roll = result["history"][0]

            st.write(
                f"**{roll['dice1']} + {roll['dice2']} "
                f"= {roll['dice_total']}**"
            )

            st.error("自動失敗（1ゾロ）")
            return

        # ロール履歴
        for roll in result["history"]:
            if roll["is_fumble"]:
                st.write(
                    f"**{roll['roll_number']}回目：** "
                    f"{roll['dice1']} + {roll['dice2']} "
                    f"= {roll['dice_total']} "
                    f"→ 1ゾロ（振り足し終了）"
                )
                continue

            text = (
                f"**{roll['roll_number']}回目：** "
                f"{roll['dice1']} + {roll['dice2']} "
                f"= {roll['dice_total']} "
                f"→ 威力表 **{roll['power_value']}**"
            )

            if roll["is_critical"]:
                text += "　🎯 **クリティカル**"

            st.write(text)

        st.divider()

        if result["critical_count"] > 0:
            st.write(
                f"クリティカル："
                f"**{result['critical_count']}回**"
            )

        st.write(
            f"威力表合計：**{result['power_total']}**"
        )

        st.write(
            f"追加ダメージ：**{result['damage_bonus']:+}**"
        )

        st.success(
            f"算出ダメージ：{result['final_damage']}"
        )


# -------------------------
# メイン
# -------------------------
def main():
    st.title("🎲 SW2.5 Support Tool")

    st.caption(
        "ソード・ワールド2.5用 非公式サポートツール"
    )

    check_tab, power_tab = st.tabs(
        [
            "⚔️ 判定用ダイス",
            "💥 威力表ダイス",
        ]
    )

    with check_tab:
        show_check_dice()

    with power_tab:
        show_power_dice()

    st.divider()

    st.caption(
        "このツールは個人制作の非公式ツールです。"
    )


if __name__ == "__main__":
    main()
