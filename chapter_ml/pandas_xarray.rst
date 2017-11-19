pandas と xarray
===================

.. ipython::
  supress::

  import matplotlib.pyplot as plt

Pythonの有名なデータ解析ライブラリに pandas [1]_ があります。
pandas は、汎用的なのデータ解析に関するインターフェースを提供するものです。
その注目すべき特徴の1つが、座標付きのデータ（labeled data）をうまく扱うことができる点です。

例えば時系列データを扱うとき、時間データと計測値の2つを保持しておく必要が有ります。
ある時間領域を切り出す時は同じ操作を両データに適応する必要が有りますし、
またある時刻での計測値を知りたいときは、時間データから対応する要素番号を探しだし、
計測データに対してその要素番号を用いてアクセスすることが必要です。
これらの操作は前節で紹介した ``np.ndarray`` でももちろん可能ですが、
毎回各自がコーディングしていると時間がかかるだけでなく、ミスの元になります。

このようなデータ解析に必要な汎用的な操作をまとめてインターフェースとして提供しているのがpandasです
（日付関連の操作や、欠損値に対する操作、複数のデータをまとめる操作など、他にも多様な便利機能がまとめられています）。
pandasはアンケート結果や株価の推移など、一般のデータ解析に広く用いられています。

一方でプラズマ計測データなど多くの物理データは、複数の座標軸を持ちます。
例えば、電子温度分布の時間変化データは、計測位置と時間という2つの軸を持つことになります。
ある時間における分布が知りたかったり、ある位置の温度の時間変化が知りたかったりします。
しかし pandas は1次元のデータ（表に表すことのできるデータ）しか扱うことができません。
xarray [2]_ [3]_ は、 pandas を多次元データに拡張したもので、地球科学研究分野から生まれたものです。
まだ新しいライブラリですが、
他種類の多次元データを扱うことの多いプラズマ研究でも有用だと思われますので、ここで紹介します。

.. [1] https://pandas.pydata.org/
.. [2] https://xarray.pydata.org/
.. [3] Hoyer, S. & Hamman, J., (2017).
  xarray: N-D labeled Arrays and Datasets in Python. Journal of Open Research Software. 5(1), p.10


xarray のインストール
----------------------

Anaconda distribution を用いて Python 開発環境を整えた人は

.. code-block:: bash

  conda install xarray

としてください。Native の Python を用いている人は

.. code-block:: bash

  pip install xarray

とするとよいでしょう。


xarray の使い方
---------------

ここでは、実際のプラズマ実験データを使ってxarray の使い方を説明します。
核融合科学研究所で計測された トムソン散乱による電子温度・密度の結果を読み込みましょう。
ファイルの読み込みプログラムやいくつかの計測データの例を
https://github.com/plasmalib/python_tutorial/data
に用意しました。 これを `data` フォルダに保存して以下のように読み込みましょう。

.. ipython:: python

  import xarray as xr  # xarray は xr と省略するのが一般的なようです
  import sys
  sys.path.append('data')
  import eg  # 読み込みプログラムも data/eg.py として保存しておいてください

  thomson = eg.load('data/thomson@115500.dat')  # thomson データの読み込み
  print(thomson)

まず、``print`` 文を用いた時の出力が綺麗に整形されていることがわかります。
``Dimensions`` の行に ``(R: 140, Time: 246)`` とあるのは、
含まれる変数は、2つの次元 ``Time`` と ``R`` に依存するということ、
それらの大きさがそれぞれ140、246であることを示しています。
``Coordinates`` セクションには、それら軸の座標の値が表示されています。
LHDのThomson散乱では、電子温度や密度その推定誤差などが得られますが、それらが
``Data variables`` セクションに含まれています。
``Data variables`` セクションの例えば `Te` の列には `(Time, R)` とありますが、
これはこの変数が ``Time`` と ``R`` に依存するということを示しています。

各 ``Coordinates`` や ``Data variables`` にアクセスするには、辞書型のように
``['Te']`` というようにすることでアクセスできます。

.. ipython:: python

  thomson['Te']

このように1種類のデータを選んでも、同時に座標情報が付随していることがわかります。


ラベルを用いたインデクシング
~~~~~~~~~~~~~~~~~~~~~~~~~~

``Coordinate`` セクションに ``Time, R`` が表示されているように、このデータには座標情報も付属します。
``.sel`` メソッドを用いることで、座標軸を元に要素を選択することができます。

.. ipython:: python

  thomson.sel(Time=6800.0, method='nearest')

ここでは、 ``Time`` 軸が 6800.0 に最も近い計測値を取得しています。
``Dimensions`` の行から ``Time`` が消えて ``(R: 140)`` だけになったことからもわかるように、
全ての計測値を一度にインデクシングしていることがわかります。

ある時刻の結果だけグラフに描きたい、ということもよくありますが、
その場合も、 ``.sel`` メソッドを用いることで1行で実現できます。

.. ipython:: python
  name: thomson_fig

  plt.plot(thomson['R'], thomson['Te'].sel(Time=6800.0, method='nearest'))
  plt.xlabel('$R$ (m)')
  @savefig thomson_plot1.png width=4in
  plt.ylabel('$T_\mathrm{e}$ (eV)')

範囲の選択も容易です。

.. ipython:: python

  # R = 3300.0 - 4000.0 間のデータを選択
  thomson_center = thomson.sel(R=slice(3300.0, 4000.0))
  thomson_center


座標名を利用した操作
~~~~~~~~~~~~~~~~~~~~~~~~~~

xarray では、軸に名前が付いているので、データが格納されている配列の軸の順序
（1つ目の軸が ``Time`` 、2つ目の軸が ``R`` に対応している、など）を覚えておく必要がありません。
例えば、各フレームでの電子温度の中央値を得たい場合、``median`` メソッドを用います。
``dim`` オプション内に、どちら方向に沿った中央値を得たいかを指定します。

.. ipython:: python

  thomson_center.median(dim='R')  # 'R' 方向の中央値を取ったデータは ''Time'' のみに依存する
  plt.plot(thomson_center['Time'], thomson_center['Te'].median(dim='R'))
  plt.xlabel('time (s)')
  @savefig thomson_plot2.png width=4in
  plt.ylabel('$T_\mathrm{e}$ (eV)')


座標を用いた異種データの結合
~~~~~~~~~~~~~~~~~~~~~~~~~~

異なる時間間隔で計測されたデータ間を結合したい時もあると思います。
例えば、トムソン散乱と干渉計による線積分電子密度の結果を比べることを考えます。
ただし、トムソン散乱と干渉計は計測時刻が異なるので、
干渉計の計測時刻からトムソン散乱の計測時刻に近いものを集めてくる必要が有ります。
この場合に限らず、複数種のデータを扱う際はこのような操作が必須となるため、
pandas や xarray には簡便な方法が用意されています。

例えば、干渉計の計測データからトムソン散乱の計測時間に合わせたデータを取ってくるには、

.. ipython:: python

  fir = eg.load('data/firc@115500.dat')  # thomson データの読み込み
  fir

  # thomson の時刻が [ms]なので [s] に修正する。
  thomson['Time'] = thomson['Time'] * 0.001

  # thomson の時刻に最も近い fir 計測結果を取得する。
  fir_selected = fir.reindex(Time=thomson['Time'], method='nearest')
  fir_selected

これで両者の演算が可能になります。


その他の特徴
~~~~~~~~~~~~~~~~~~~~~~~~~~

xarray は他にも様々な便利機能を備えています。

+ 軸・データの関係を記録する netCDF [5]_ ファイルへの入出力
+ dask [6]_ を用いたメモリに格納できない規模のデータの取り扱い、並列計算

ここではこれらを説明する紙面の余裕がありませんが、どれも有用な機能となっています。
xarray の document ページ http://xarray.pydata.org をご参考ください

こういったライブラリができることは、コーディングさえすればNumpyなどでも同様のことができるため、
独自の使用法を習得してまで使おうというインセンティブが湧かないかもしれません。
しかし毎回自身でコーディングすることは、試行錯誤のスピードを低下させるだけでなく、
ケアレスミスも誘発します。

最初に使用法を覚える段階はまどろっこしく自身で作った方が早いように感じますが、
慣れてしまうとこのようなライブラリを用いる方が圧倒的に操作が楽に確実になります。
有用なツールの習得に時間をかけるのは、ちょっとした投資と言えるかもしれません。

.. [5] https://www.unidata.ucar.edu/software/netcdf/
.. [6] https://dask.pydata.org/en/latest/
