画像分類
--------
* :doc:`lung_nodule`

   * 問題：2クラス分類
   * 新規要素

      * 画像の読み込み・表示
      * 深層学習モデルを自分で作成
      * ホールドアウト検証
      * 学習
      * 混同行列
      * ROC曲線とAUC

* :doc:`lung_nodule_cv`

   * 問題：2クラス分類
   * 新規要素

      * K-Fold交差検証
      * DataAugmentation (ImageDataGenerator)

* :doc:`NBI_colonoscopy`

   * 問題：3クラス分類
   * 新規要素

      * 多クラス分類
      * 学習の早期終了(trainingセットを利用)
      * 事前学習されたモデルからの転移学習・ファインチューニング


* :doc:`dld`

   * 問題：6クラス分類
   * 新規要素

      * 教師データをtraining、validation、testの3つに分割
      * 学習の早期終了(validationセットを利用)

.. toctree::
   :maxdepth: 0
   :hidden:

   lung_nodule
   lung_nodule_cv
   NBI_colonoscopy
   dld
