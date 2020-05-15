概観
****

* :doc:`pulmonary_nodule`

   * 問題：2クラス分類
   * 新規要素

      * 画像の読み込み・表示
      * 深層学習モデルを自分で作成
      * ホールドアウト検証
      * 学習
      * 混同行列
      * ROC曲線とAUC

* :doc:`pulmonary_nodule_cv`

   * 問題：2クラス分類
   * 新規要素

      * K-Fold交差検証
      * DataAugmentation (ImageDataGenerator)
      * カットオフ値
      * Probability Calibration curves

* :doc:`skin_lesion`

   * 問題：7クラス分類
   * 新規要素

      * カラー画像
      * 多クラス分類
      * 事前学習されたモデルからの転移学習・ファインチューニング
      * 学習の早期終了(trainingセットを利用)


* :doc:`dld`

   * 問題：4クラス分類
   * 新規要素

      * 教師データをtraining、validation、testの3つに分割
      * 学習の早期終了(validationセットを利用)
