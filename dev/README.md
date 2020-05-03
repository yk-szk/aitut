# ドキュメント(htmlとpdf)の作成用

``` bash
pip install -r dev/requirements.txt
```

## 設定
``` bash
    ipython profile create
```

`~/.ipython/profile_default/ipython_kernel_config.py`に以下を追加
``` python
    c.InlineBackend.figure_formats = {'pdf', 'retina'}
```

## git
`git add`前に(手動で😥)notebooksディレクトリ内で`../dev/clean_all.bat`する。

## build html and pdf
notebooksディレクトリ内で`../dev/execute_all.bat`する。