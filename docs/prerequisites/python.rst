Python
======

条件演算子(conditional operator)
----------------------------
.. code-block:: python

   x if a > b else y

if文を簡潔に書ける場合があります。

内包表記(comprehension)
-----------------------
.. code-block:: python

   [i*2 for i in range(10)]

for文を簡潔にかけるようになります。使われる括弧によって種類が変わります。

* :code:`[]` : リスト内包表記
* :code:`{}` : 集合内包表記か辞書内包表記
* :code:`()` : ジェネレータ内包表記

スライス(slice)
---------------
.. code-block:: python

   array[:, 0]

リストや配列の部分指定等に使います。

* :code:`[::-1]` : 逆順で取得
* :code:`[::2]` : 偶数番目の要素を取得
* :code:`[1::2]` : 奇数番目の要素を取得
* :code:`[:3]` : 最初の3つを取得
* :code:`[-3:]` : 最後の3つを取得

Ellipsis
--------
.. code-block:: python

   image[..., 0]

:code:`...` の部分のことです。多次元配列でスライスの一部を省略するときに使えます。

型ヒント(Type hint)
-------------------
.. code-block:: python

   def func(x : int):

:code:`: int` の部分のことです。型を指定するときに使います。
ただし、型が強制されるわけではないので指定されている型以外が使用された場合でもエラーは出ません。

デコレータ(decorator)
---------------------
.. code-block:: python

   @property
   def x(self):
       return self._x

:code:`@XXX` の部分のことです。関数に機能を付加する際に使います。

セイウチ演算子(Walrus operator)
-------------------------------
.. code-block:: python

   if (n := len(a)) > 10:

:code:`:=` の部分のことです。比較的新しい演算子なのであまり見ることはないと思います。安易に使うこともお勧めしません。

Chained comparison
------------------
.. code-block:: python

   0 < x < 10

複数の比較を簡潔に書けます。