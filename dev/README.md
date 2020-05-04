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

デフォルトのfigsize。設定ファイルの場所を調べる。
``` python
import matplotlib
matplotlib.matplotlib_fname()
```

~~figure.figsizeを設定する。~~ 
``` python
figure.figsize   : 3.2, 2.4   ## figure size in inches
```
↑ではだめっぽい？からrcsetup.pyを書き換える。


## git
`git add`前に(手動で😥)notebooksディレクトリ内で`..\dev\clean_all.bat`する。

## build html and pdf
notebooksディレクトリ内で`..\dev\execute_all.bat`する。