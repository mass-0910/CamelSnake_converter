# CamelSnake_converter

Pythonのソースコードを"キャメルケース⇔スネークケース"変換できるツールです。  
キャメルケース派 vs スネークケース派の争いを終わらせるために作成しました。

## 特徴

クラス、関数、変数にそれぞれ当てはめるルールを設定できます。  
`src`以下にある`setting.json`内のそれぞれの値を変更してください。
```setting.json
{
    "class": "pascal", # クラスはパスカルケースに変換
    "var": "snake", # 変数はスネークケースに変換
    "func": "snake" # 関数はキャメルケースに変換
}
```

## 使いかた

```bash
$ python cs.py convert hogehoge.py  
```
上記コマンドを実行すると`hogehoge.py.conv`という変換後のファイルが出力されます。