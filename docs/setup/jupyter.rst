********************************
Jupyter Notebookの設定(Optional)
********************************
.. note::

   必須というわけではありません。

拡張機能をインストールする。 ::

   pip install jupyter-contrib-nbextensions jupyter_nbextensions_configurator

拡張機能を有効化する。 ::

   jupyter contrib nbextension install --user
   jupyter nbextensions_configurator enable --user

目次の追加
======================
`Table of Contents (2) <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/toc2/README.html>`_ 見出しをもとに目次を表示する。

* Jupyterを起動したときに最初に表示されるページでNbextensionsタブをクリック
* [Table of Contents (2)]をチェック
* [Parameters]の[Skip h1 headings...]をチェック
* Notebookに目次表示用のアイコンが追加される。

Code prettify
================
`Code prettify <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_code_prettify.html>`_ コードの自動成型を行う。

* 必要なパッケージをインストール。``pip install yapf``
* [Nbextensions]タブで[Code prettify]をチェック
* Notebookに自動整形実行用に小槌のアイコンが追加される。