********
環境構築
********
.. note::

   Windows10での環境構築方法です。

Anacondaのインストール
======================
`Anacondaのサイト <https://www.anaconda.com>`_ からインストーラーをダウンロードし実行。

チュートリアル用のenvを作成
===========================
.. code-block:: Bash

   conda create -n ai_tut python==3.7
   activate ai_tut

必要なパッケージをインストール
==============================
.. code-block:: Bash

   pip install -r requirements.txt


Tensorflow
==========
.. note::

   TensorFlow 2以降ではGPUを使う場合でもtensorflow-gpuをインストールする必要はない。

.. code-block:: Bash

   pip install tensorflow

GPUを使用するための追加作業
===========================
* Visual Studio Community
* Cuda
* cuDNN

Graphvizのインストール(Optional)
================================
.. note::

   Graphvizはネットワーク構造をグラフで表示する場合にのみ必要。

* `公式サイト <https://graphviz.gitlab.io/download/#executable-packages>`_ からインストーラーをダウンロードし実行。
* 環境変数を変更してパスを通すパスを通す。

   * [コントロールパネル] → [システム] → [システムの詳細設定]
   * ユーザー環境変数で[新規]をクリック
   * 変数名 ``Graphviz`` 、変数値 ``C:\graphviz\release\bin`` を入力して[OK]
   * ユーザー環境変数で ``Path`` を選択後[編集]をクリック
   * [新規]をクリック ``%Graphviz%`` を入力して[OK]

* バージョンを表示してインストールできているかを確認 ::

   dot -V