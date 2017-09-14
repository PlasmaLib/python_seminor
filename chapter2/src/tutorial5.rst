クラスを定義して使う
============================

.. ipython:: python
   :suppress:

    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(123456)

クラス（class）とは、（複数の）データと
そのデータに関する関数（メソッドと言う）をひとまとめにした
オブジェクトである。
オブジェクト指向プログラミングの第一歩はクラスを学ぶところから始まる。
ここでは、そのさわりを簡単に述べる。


クラスの例 np.ndarray
-------------------------------

まずは、クラスがどのようなものか理解するため、その例として`np.ndarray`のメソッドを紹介する。

.. ipython:: python

  x = np.linspace(0,1,12)
  x
  y = x.reshape(4,3)  # Here, we constructed a 4 x 3 matrix.
  y

ここで reshape はメソッドであり、x の持つ値を変形したものを返すものである。
もちろん同様の操作は関数だけを用いても行うことができるが、その場合
get_reshaped_array(src, src_shape, dtype, target_shape)
というように、変形したいデータ（src）に関するたくさんの変数（srcの値、srcの大きさ、変数の型）
を全て指定する必要があり、ソースコードが冗長になる。

クラスという概念では、
np.ndarray というオブジェクトの中に、データの他、
変数の型や大きさなど必要な情報をひとまとめにして格納しておく。
そのオブジェクトのメソッドでは、それらの値を用いることができるため、
プログラムが簡潔になり、バグが少なくなる。
（複雑なプログラムを作成するためのコツは、
　くだらないバグをなくす行為にできるだけリソースを割かないようなシステムにすることである。）


クラスの定義
---------------------

ここでは例のため、極座標のクラスを作成しよう。

.. ipython:: python

    class PolarCoordinate(object):
        def __init__(self, r, theta):
            """
            An object that handles polar coordinate in 2d-space,
            a radial coordinate(s) r and angular coordinate(s) theta.
            """
            self.r = r
            self.theta = theta
        |
        def to_xy(self):
            """
            Convert to polar coordinate (r, theta) to x-y coordinate values.
            Returns x and y as a tuple.
            """
            return self.r * np.cos(self.theta), self.r * np.sin(self.theta)
        |
        def to_complex(self):
            """
            Convert to complex values.
            """
            return np.complex(self.r * np.cos(self.theta),
                              self.r * np.sin(self.theta))


__init__ メソッドは、
クラスをインスタンス化（実体を持つ変数として確保すること）時に実行されるメソッドである。
今回作成したクラスの__init__メソッドは self, r, theta の3つの引数を必要とする。
self は、このオブジェクト自体を指すものであり、
Python のメソッドのひとつ目の引数は基本的には self とすることになっている。

メソッド内では、self を通して自らのオブジェクトにアクセスする。
例えば

.. code-block :: python

  self.r = r

では、PolarCOordinate 内に変数 r を定義し、その値として__init__メソッドに渡された
rを代入することを示している。

クラスオブジェクトをインスタンス化するためには

.. ipython:: python

  polar = PolarCoordinate(1.0, 0.5 * np.pi)

というように、クラス名(引数) を実行する。なお、self引数は省略する。
クラス内の変数には . （ドット）を通してアクセスできる。

.. ipython:: python

  polar.r

また、to_xy などもメソッドであり、. を通して呼び出すことができる。

.. ipython:: python

  polar.to_xy()
