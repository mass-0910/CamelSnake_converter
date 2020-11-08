# CamelSnake_converter

Pythonのソースコードをキャメルケースまたはスネークケースに変換できるツールです。  
キャメルケース派 vs スネークケース派の争いを終わらせるために作成しました。

## 特徴

クラス、関数、変数にそれぞれ当てはめるルールを設定できます。  
`src`以下にある`setting.json`内のそれぞれの値を変更してください。
```setting.json
{
    "class": "pascal",
    "var": "snake",
    "func": "camel"
}
```

## 使いかた

```bash
$ python cs.py convert hogehoge.py  
```
上記コマンドを実行すると`hogehoge.py.conv`という変換後のファイルが出力されます。