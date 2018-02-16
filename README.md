# sphttp-exp-sample

## 必要なもの

### ランタイムおよびツール
- git
- python 3.6
- pip (python のパッケージシステム 上記のpythonに紐付いているもの)

実行環境によってはコマンド名がpython3やpip3となっている場合もあるので適宜読み替える必要あり

### pythonの外部パッケージ
- yarl: URL解析
- matplotlib: グラフ描画
- tqdm: 進捗バー表示
- requests HTTPライブラリ

#### 一括インストール

```bash
$ pip install -r requirements.txt
```

## sphttpのインストール

```bash
$ pip install -U git+https://github.com/johejo/sphttp.git
$ pip install -U git+https://github.com/Lukasa/hyper.git
```

sphttpにログ解析用関数をいくつか定義済み

```python
from sphttp.analyze import open_pickled, get_invalid_block_log

log = open_pickled(filename)
send_log, recv_log, head_log = log
invalid_block_log = get_invalid_block_log(recv_log)
```

## ディレクトリ構成


    

## 実験

```bash
$ python exp.py
```

expディレクトリ内にXXXX.pickleという形式でログを保存


## 解析


### 基本的な解析

```bash
$ python analyze.py
```

ログ解析を行いグラフを出力
グラフの体裁はかなり汚いのでmatplotlibのパラメータで調整することが望ましい

### 非有効ブロック数および遅延時間の時間変化

```bash
$ python all_time_changes.py
```

大量のグラフが出力されるので注意

## ツール

### ログ変換ツール

(送信ログ, 受信ログ, 各ホストに対するHEADリクエストの応答時間ログ)の3つがまとまったログから各ログを二次元のテキスト形式のログに変換するツール

```bash
$ python convert.py -s hoge.pickle
```
この例ではhoge.pickleというログから送信ログのみを標準出力に表示  
-o オプションでファイル名を指定することでファイルへの書き出しも可能  
詳しくは--helpオプション参照

### 帯域測定ツール
帯域の事前調査のためのツール

```bash
$ python bandwidth_check.py
```
json形式で結果を出力ファイルに出力  
デフォルトのファイル名はISO-8601形式の日付と時刻.json  
-n オプションで試行回数の指定可能  
-o オプションでファイル名の指定可能  
帯域のSI接頭辞も変更可能  
詳しくは--helpオプション参照


## コメント
sphttpやサンプルスクリプトのpythonコードにはパフォーマンス向上目的で大量の内包表記が含まれているので
pythonの内包表記への理解を深めることが望ましい

## 連絡先
mitsuo_h@outlook.com
