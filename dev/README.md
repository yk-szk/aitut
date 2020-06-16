# ドキュメント(htmlとpdf)の作成用
開発はdev/notebooksで行う。
Windowsで開発するため、makeとMakefileの代わりに[doit](https://pydoit.org/contents.html)とdodo.pyを使う

- notebooks/ : 配布用のnotebook置き場。`doit clear`で生成する。gitで管理する。実行しない。
- dev/notebooks/ : 開発用のnotebook置き場。gitで管理しない。実行する。
- docs/notebooks/ : documentation用のnotebook置き場。`doit execute`で生成する。gitで管理しない。実行しない。

## 初期設定

Dataはdev/notebooks内に置く。

``` bash
pip install -r dev/requirements.txt
```

### plot用の設定

``` bash
ipython profile create
```

`~/.ipython/profile_default/ipython_kernel_config.py`に以下を追加
``` python
c.InlineBackend.figure_formats = {'pdf', 'retina'}
```

## Initialize development
以下のコマンドを実行して、notebooks/からファイルをdev/notebooksにコピーする。
``` bash
doit init
```

## documentation用にexecuteする
``` bash
doit execute
```


## commit用にclearする
``` bash
doit clear
```

## pdfをbuild
WSLでdocs/_build/latexに移動してmake

## gh-pages
docs/_build/htmlでcommitしてpush
