# sphttp-exp-sample

## 必要なもの

### ランタイムおよびツール
- git
- python 3.6
- pip (python のパッケージシステム 上記のpythonに紐付いているもの)

### pythonの外部パッケージ
- yarl: URL解析
- matplotlib: グラフ描画
- tqdm: 進捗バー表示

#### 一括インストール

```bash
$ pip install -r requirements.txt
```

## sphttpのインストール

```bash
$ pip install -U git+https://github.com/johejo/sphttp.git
$ pip install -U git+https://github.com/Lukasa/hyper.git
```

## ディレクトリ構成

.  
├── README.md  
├── exp  
│   ├── all_time_changes.py　<- 全試行の時間変化をプロット  
│   ├── analyze.py <- 基本的な解析  
│   ├── count_dup.py <- 重複再要求送信回数表示  
│   ├── exp.py <- 実験スクリプト  
│   └── head.py <- 初期遅延予測についてプロット  
├── requirements.txt  
└── tool  
    └── convert.py　<- ログ変換ツール  
    
    
## 連絡先
mitsuo_h@outlook.com
