********
環境構築
********
.. note::

   Windows10での環境構築方法です。

Anacondaのインストール
======================
`Anacondaのページ <https://www.anaconda.com/products/individual>`_ からインストーラーをダウンロードし実行。

チュートリアル用のenvを作成
===========================
Anaconda Promptで以下のコマンドを実行する。

.. code-block:: shell-session

   $ conda create -n aitut python==3.8
   $ activate aitut

必要なパッケージをインストール
==============================
notebooksディレクトリに移動し以下のコマンドを実行する。

.. code-block:: shell-session

   $ pip install -r requirements.txt


GPUを使用するための準備(Optional)
==================================
.. note::

   必須ではありませんが、可能ならGPUが利用できる環境を用意することをお勧めします。

* Visual Studio Community

   * C++によるデスクトップ開発を選択

* CUDA

   * `PyTorchのページ <https://pytorch.org/get-started/locally/>`_ で対応しているCUDAのバージョンを確認する。
   * `インストーラー <https://developer.nvidia.com/cuda-toolkit-archive>`_ をダウンロードしインストールする。

* cuDNN

   * `cuDNN公式サイト <https://developer.nvidia.com/cudnn>`_ からインストーラーをダウンロードし実行。登録が必要。


PyTorchのインストール
=====================
`PyTorchのページ <https://pytorch.org/get-started/locally/>`_ に従い、自分の環境に合った方法でインストールする。

Graphvizのインストール(Optional)
================================
.. note::

   Graphvizはネットワーク構造をグラフで表示する場合にのみ必要。

* `公式サイト <https://graphviz.gitlab.io/download/#executable-packages>`_ からインストーラーをダウンロードし実行。
* 環境変数を変更してパスを通す。

   * :menuselection:`[コントロールパネル] --> [システム] --> [システムの詳細設定]`
   * ユーザー環境変数で[新規]をクリック
   * 変数名 ``Graphviz`` 、変数値 :file:`C:\Program Files (x86)\Graphviz2.38\bin` を入力して[OK]
   * ユーザー環境変数で ``Path`` を選択後[編集]をクリック
   * [新規]をクリック ``%Graphviz%`` を入力して[OK]

* コマンドプロンプトにて以下のコマンドを実行することで、バージョンを表示してインストールできているかを確認

.. code-block:: shell-session

   $ dot -V

*******************
Google Colaboratory
*******************
準備中

Google Driveのマウント

.. code-block:: python

   from google.colab import drive
   drive.mount('/content/drive')

データをコピー(Google Driveから直接ファイルを読み込むと遅いため事前にコピーしておく)

.. code-block:: bash

   !rsync -ahv --progress '/content/drive/My Drive/tutorial/chest_xray.zip' .
   !mkdir -p ./Data/Images
   !unzip -nq chest_xray.zip -d Data/Images

左のフォルダアイコンで:file:`Data/Images/...` ができていればOK.