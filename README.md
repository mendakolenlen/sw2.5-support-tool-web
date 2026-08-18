# SW2.5 Support Tool

「ソード・ワールド2.5」のセッションを補助するために個人制作している非公式Webツールです。

Python / Streamlitの学習も兼ねて開発しています。

## Web版

以下のURLからブラウザ上で利用できます。

https://sw25-support-tool-mendakolenlen.streamlit.app

## 現在の機能

### 判定用ダイス

2D6による基本的な行為判定を行います。

* ボーナスを指定
* 目標値を指定
* 達成値を自動計算
* 成功 / 失敗を判定
* 1ゾロによる自動失敗
* 6ゾロによる自動成功

### 威力表ダイス

SW2.5の威力表を使用した算出を行います。

* 威力0～50に対応
* C値8～13に対応
* クリティカルによる振り足し
* 複数回のクリティカル
* 初回1ゾロの自動失敗
* クリティカル後の1ゾロ処理
* 追加ダメージ
* 各ロールの履歴表示
* 最終的な算出ダメージの表示

## 使用技術

* Python
* Streamlit
* unittest
* Git / GitHub

## テスト

ダイス判定や威力表処理について、自動テストを用意しています。

```bash
python -m unittest discover -s tests -v
```

## プロジェクト構成

```text
sw2.5-support-tool-web/
├─ app.py
├─ dice_logic.py
├─ power_logic.py
├─ power_table.py
├─ requirements.txt
├─ README.md
└─ tests/
   ├─ test_dice_logic.py
   ├─ test_power_logic.py
   └─ test_power_table.py
```

### 主なファイル

`app.py`
StreamlitによるWeb画面を担当します。

`dice_logic.py`
2D6による判定処理を担当します。

`power_logic.py`
威力表、クリティカル、追加ダメージなどの処理を担当します。

`power_table.py`
威力0～50の威力表データを保持します。

`tests/`
各処理の自動テストを格納しています。

## ローカルでの実行

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

その後、以下を実行します。

```bash
streamlit run app.py
```

ブラウザでローカル版のアプリが起動します。

## 注意事項

このツールは個人制作の非公式ツールです。

「ソード・ワールド2.5」および関連する名称・ルール等の権利は、それぞれの権利者に帰属します。

ルール処理については正確性を重視して実装していますが、本ツールの結果が公式ルールや公式裁定を保証するものではありません。
