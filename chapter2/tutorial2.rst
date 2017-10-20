外部パッケージの使用
=============================

Pythonの特徴は、多様なパッケージ（いくつかの機能をまとめたライブラリ）が
豊富に開発されていることが特徴である。

実際には生のPythonだけで用いることは少なく、基本的な数値計算機能を提供する Numpy [2]_ や
グラフ描画ライブラリである Matplotlib [3]_
を始めとして外部パッケージを多量に用いることになる。


.. [2] NumPy, NumPy developers, http://www.Numpy.org/
.. [3] Matplotlib, John Hunter, Darren Dale, Eric Firing, Michael Droettboom and the Matplotlib development team, https://matplotlib.org/

------------------------------------------
Numpy を利用する
------------------------------------------

Numpy や Matplotlib はデータ解析における最も基本的なパッケージである。
本講座の方法に従って Anaconda をインストールした環境では、
これらは既にインストールされている。

こういったパッケージを 各自で開発するスクリプトで用いるためには以下のように
import 文により宣言する必要がある。

.. ipython:: python

  import numpy as np

ここで import numpy as np は、「Numpy パッケージを np という名前で用いる」
という宣言である。
なお、asの後ろの名前はユーザが勝手に決めてよいものだが、
混乱を避けるため、広く用いられている略称を用いることが望ましい。
Numpy の場合、np が正式な略称である。
このようにしてインポートした後は、np.*** という形で用いることができる。

Numpy は線形代数演算や特殊関数の計算など、
多くの基本的な数学操作を含む科学技術計算用ライブラリである。

多くのアルゴリズムは、これまで C や Fortran で開発されてきた Netlib [4]_ などのライブラリの
Pythonラッパーであるため、
非常に安定しているほか、CやFortranと同等の高速演算が可能である。

また、Anacondaからインストールした Numpy には
MKL [5]_ というインテルの数値計算ライブラリが同梱されている。
行列計算などは自動的に並列化されるため、
並列化されていないFortran、Cプログラムよりも高速に実行できることがある。

.. [4] The Netlib, http://www.netlib.org/

.. [5] Intel, MKL, https://software.intel.com/en-us/mkl

Numpy の代表的な関数
------------------------------------------------------------------

Numpy を用いることで、多くの種類の算術演算を行うことができる。
例えば sin 関数は以下のようにして用いる。

.. ipython:: python

  x = np.sin(0.5 * np.pi)
  x

Numpy では非常に多くの種類の関数やクラスが用意されている。
そのためどのような関数が用意されているかを把握することも難しく、
それらの使用法をすべて暗記することはほとんど不可能である。

Python などのオープンソースソフトウェアでは、
開発に際して、使用法などの文書を同時に残していく文化が形成されており、
ユーザがある関数の使い方を知りたいと思った場合もすぐにその情報にアクセスできる。

Jupyter-notebook では、以下のように ``np.`` まで記入してから Tab を押下すると、
np.内にある関数一覧が表示されるほか、``np.s`` まで記入してから Tab を押下すると
それに合う候補を表示してくれる。
使用法がわからない関数でも、カーソルが括弧内にあるときに
Shift + Tab を押下するとで、それぞれの関数の使い方に関する文書（docstringsと言う）
にアクセスできるため、使い方をすぐに理解することができる。

.. figure:: figs/np_suggest.png
   :scale: 50 %
   :alt: suggestion for np functions

   Jupyter-notebook のサジェスト機能の様子。``np.`` まで入力してから、Tab を押すことで
   ``np`` パッケージ内でアクセスできるものが表示できる。

.. figure:: figs/np_suggest2.png
   :scale: 50 %
   :alt: docstrings for np.sinc

   Jupyter-notebook による docstring 表示の様子。
   関数内部（括弧``()``の内側）で Shift + Tab を入力することで、
   関数名、引数、docstringを表示できる。


さらに、科学技術用途以外も含め Python は広く用いられている汎用言語なので、
インターネットで検索するだけでも多くの情報を見つけることができる。


多次元配列型 np.ndarray
------------------------

Numpy は、多次元配列用のクラス（クラスについては後述する）である ``np.ndarray`` を提供している
（なお、"nd"array は、n-dimensional の略である）。
``np.ndarray`` は配列の大きさを後から変更できない、
全ての要素の型が同一なものに限られる、という点はリストと異なるが、
同様にインデクシング・スライシングに対応している。

``np.ndarray`` は、多次元配列の基礎となるクラスで、
線形演算を含む多くのNumpy関数で利用する他、
だけでなくpandasなど他のライブラリでも広く利用されている
基本的なオブジェクト形式となっている。

以下では、その利用法について簡単に触れる。
``np.ndarray`` を定義するためには、``np.ndarray`` から用意するか、
``np.ones`` や ``np.linspace`` などの関数を用いる。

.. ipython:: python

  # [5 x 3 x 2] の大きさの配列をxとして確保する。
  x = np.ndarray((5, 3, 2))

  # [2 x 3] の大きさで、要素がすべて１のint型の配列をyとして確保する。
  y = np.ones((2, 3), dtype=int)
  y

``np.ndarray`` とスカラー、``np.ndarray`` 同士の計算は、要素ごとの計算として定義されている。

.. ipython:: python

  y * 3

  y + y

また、``np.abs()`` や ``np.square()`` などスカラーを引数に持つ関数に渡した場合は、
要素ごとに該当する演算が行われた ``np.ndarray`` が返される。

.. ipython:: python

  np.sin(y)

二次元配列としての内積は ``np.dot(x, y)`` や Python 3 では ``x @ y`` として計算できる。


Numpy を用いて効率よく計算を行う
------------------------------------------------------------------

上述したように、Numpyの内部ではCやFortranによる演算を行うため高速である。
逆に言うと、Numpyの内部に任せられることをPythonで実装すると非常に低速になる。
例えば

.. ipython:: python

  z = np.ndarray(y.shape)
  for i in range(y.shape[0]):
    for j in range(y.shape[1]):
      z[i,j] = np.sin(y[i,j])

は、``z = np.sin(y)`` に比べてコードが冗長になるだけでなく、低速になる。
Pythonではできるだけループを用いないこと（外部ライブラリができる部分はそれに任せる）が、
高速な演算を行うコツである。

なお Numpy の詳しい使い方は、4章に譲る。


ファイルへの読み込み・書き出し
------------------------------------------------------------------


Pythonでファイルの読み込み・書き出しを行う場合、
ファイルを開く > １行ずつ内容を読み込む・書き出す > ファイルを閉じる
のように、低レベルの操作を行うことは少ない。
多くのパターンのファイル操作が用意されているので、
そちらを用いる方が圧倒的に高速でありバグも少ないからである。

例えば単純なCSVデータの読み込み、書き込みには、``np.loadtxt``、``np.savetxt``
などを用いることが多い。

------------------------------------------
Matplotlib を利用する
------------------------------------------

Matplotlib は、広く用いられているグラフ描画ライブラリである。
Matlabのグラフ描画機能を参考にして開発されたようで、よく似た命名規則を持っている。

Matlab の詳しい使い方自体は次章に譲り、
ここでは単純な描画方法についてのみ述べる。

.. ipython:: python

  import matplotlib.pyplot as plt
  %matplotlib inline

``import matplotlib.pyplot as plt`` は、
matplotlib パッケージの中の pyplot モジュールを plt という名前で用いる
という意味である。
また ``%matplotlib inline`` は Jupyter-notebook 用のコマンドであり、
コードセルのすぐ下に ``Matplotlib`` の図を表示させるためのものである。

なお、パッケージ、モジュールなどの厳密な定義は、章末の「Pythonの階層構造」を参考にすること。

Matplotlibの最も基本的な用法は、１次元データを表示することである。

.. ipython:: python

  x = np.linspace(0,1,11)  # 0 ~ 1 を11等分した要素を持つ np.ndarray を返す関数
  y = np.sin(np.pi * x)

  @savefig tutorial2_plot1.png width=4in
  plt.plot(y)


``plt.plot`` の引数に１次元データを渡すことで、
横軸が要素番号、縦軸が要素の値のグラフを描画できる。

x軸を指定するには、

.. ipython:: python

  @savefig tutorial2_plot2.png width=4in
  plt.plot(x, y, '-o')

というように、x軸の値とy軸の値を引数として渡す。
なお、３つ目の引数には描画の様式を指定する。ここで、３つ目の引数に'-o'を渡すと
丸印のマーカを線で繋いだグラフを描画できる。
