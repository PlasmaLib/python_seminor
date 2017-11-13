pandas と xarray
===================

.. ipython:: matplotlib

Pandas や xarray は高速で便利なデータ構造およびデータ解析ツールを提供するオープンソースライブラリです。
著者の考えるこれらのライブラリの最も大きな特徴は、データと軸情報を矛盾なく扱える点です。

例として何か時系列の信号、例えばHαの発光強度の時間変化のデータがあるとしましょう
（なお、本節で用いるデータは  ***** にアップロードされています。以降では、これらのデータを data に保存しているという前提でコードを記載します。）。
ある時刻の計測値が知りたいときを考えます。

これを Numpy で実現するには、まず軸情報（計測時間のデータ）を参照して、
その時刻に最も近い時刻のインデックスを得ます。そしてインデックスを用いてHαの計測値を参照します。

.. ipython:: python

  import numpy as np
  ha_t, ha = np.loadtxt('data/ha.dat', unpack=True, skiprows=1)  # ファイル読み込み
  target_t = 4.0  # 計測値を知りたい時刻
  index = np.argmin(np.abs(ha_t - target_t))  # 最も近いインデックスを取得する
  ha_t[index], ha[index]

これを Pandas で行うと、

.. ipython:: python

  import pandas as pd  # Pandas は pd と略すのが一般的
  df = pd.read_csv('data/ha.dat', index_col=0,  # 0行目を軸として指定する
                   delim_whitespace=True)
  df.loc[4.0]  # 4.0 s での値を取得する

Numpyでは、時刻と計測値を別々の ``np.ndarray`` として保持しておく必要がありますが、
Pandas ではデータと軸を DataFrame と呼ばれる1つオブジェクトとして扱うことができます。
さらに、軸の値をあたかも引数のように操作することができます。

このように一般に現実データは、単独のデータの羅列というよりは、
ある時刻における発光強度、というように複数の要素から構成されており、両者に対応関係があります。
pandas はそういったデータ（ラベル付きデータと呼びます）をうまく扱うフレームワークを提供しており、
アンケート結果や株価の推移など、現実世界の様々なデータに広く利用されています。

ただし pandas は、表に表されるような基本的に1次元データを対象に開発されている言語です。
しかし科学データは一般的に多次元データです。
複数の空間位置で何か値を計測しているとすると、空間と時間という2つの軸情報が必要となりますが、
pandasではそれをうまく扱うことができません。

pandas の機能を多次元データに拡張しているライブラリが xarray です。
使用法や概念もよく似ているので、ここでは主に xarray の使用法を紹介することにします。


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
核融合科学研究所で計測された Thomson 散乱による電子温度・密度の結果を読み込みましょう。
ファイルの読み込みプログラムを *** に用意しました。
これを `data/eg.py` に保存して以下のように読み込む。

.. ipython:: python

  import xarray as xr  # xarray は xr と省略するのが一般的なようです
  import sys
  sys.path.append('data')
  import eg

  thomson = eg.load('data/thomson@120000.dat')  # thomson データの読み込み
  print(thomson)

まず、``print`` 文を用いた時の出力が綺麗に整形されていることがわかります。
``Dimensions`` の行に ``(R: 140, Time: 300)`` とあるのは、
データは2つの次元 ``Time`` と ``R`` に依存するということを示しています。
``Coordinates`` セクションには、それら軸の座標の値、
``Data variables`` セクションには、それらの軸に対応する計測値が含まれています。

各 ``Coordinates`` や ``Data variables`` にアクセスするには、辞書型のように
``['Te']`` というようにすることでアクセスできます。

.. ipython:: python

  thomson['Te']

``Coordinate`` セクションに ``Time, R`` にあるように、座標情報も付属します。
ある時刻でのこの計測値をグラフに描きたい、ということもよくあります。
その場合も、この座標の値を用いて簡単に表すことができます。

.. ipython:: python

  @savefig thomson_plot1.png width=4in
  plt.plot(thomson['R'], thomson['Te'].sel(Time=3.0, method='nearest'))

``.sel`` メソッドを用いることで、座標軸に対応した値を取得できます。
ここでは、 ``Time`` 軸が 3.0 に最も近い計測値を取得しています。
同様に、計測位置 ``R`` が最も 3.6 に近い計測値を取得するには

.. code-block:: python

  thomson['Te'].sel(R=3.6, method='nearest')

というようにします。


こういったライブラリができることは、コーディングさえすればNumpyなどでも同様のことができるため、
独自の使用法を習得してまで使おうというインセンティブが湧かないかもしれません。
しかし毎回自身でコーディングすることは、試行錯誤のスピードを低下させるだけでなく、
ケアレスミスも誘発します。
最初に使用法を覚える段階は面倒ですが、慣れてしまうとこのようなライブラリを用いる方が圧倒的に楽になるのでお勧めします。
