機械学習ライブラリ scikit-learn
===============================

.. ipython:: python
  :suppress:

  import numpy as np
  import matplotlib.pyplot as plt
  import sys
  sys.path.append('data')
  import eg
  thomson = eg.load('data/thomson@115500.dat')  # thomson データの読み込み


Scikit-learn は Pythonで最も有名な機械学習ライブラリでしょう。
主な特徴は以下のようなものです。

+ 一般的な機械学習アルゴリズムが網羅されている
+ ドキュメントがよく整備されており、素人でも簡単に利用できる
+ 簡単に理解できる平易な実装となっている
+ 計算負荷の高いところはC++で実装されているため比較的高速

機械学習というと、IT関係、人工知能関係のごく限られた内容を想定されるかもしれませんが、
そんなことはありません。
機械学習とは統計と言い換えてもほとんど問題ないでしょう。
実験データや計算データなど、データ解析に関わる問題であれば関わる可能性も高いと思います。

主に

+ 回帰問題
+ 教師有り分類問題
+ 教師無し分類問題
+ 次元圧縮・特徴抽出
+ モデル選択
+ データ前処理

に関する様々なアルゴリズムが実装されています。


scikit-learn のインストール
-----------------------------

Anaconda distribution を用いて Python 開発環境を整えた人は

.. code-block:: bash

  conda install scikit-learn

としてください。Native の Python を用いている人は

.. code-block:: bash

  pip install scikit-learn

とするとよいでしょう。


scikit-learn の使用例
---------------------

scikit-learn では様々な手法が利用できますが、ここでは線形回帰を紹介します。
線形回帰とは、計測データ y を基底関数 :math:`\phi(x)` の線形和で近似するものです。

.. math::

  y_i \approx \sum_j w_j \phi_j(x_i)

ここで、 :math:`w_j` は線形結合の係数です。
:math:`\phi(x)` にどういった式を用いるかで、
多項式近似や、スプライン近似などを表すことができる汎用的なモデルです。
scikit-learn では ``linear_model`` モジュールとして提供されています。
ここでは、前節で紹介したトムソン散乱による電子温度分布を複数のガウス関数の和で近似することにします。

最も簡単な近似法は、最小二乗法です。最小二乗法では、

.. math::

  \sum_i \left(y_i - \sum_j w_j \phi_j(x_i)\right)^2

を最小化する :math:`w_j` を求めます。
このような最小二乗法は、ノイズがガウス分布に従っていると仮定したものです。
しかし、一般にノイズが綺麗なガウス分布に従っているとは限りません。
例えば 前節に示したトムソン散乱による電子温度分布も、外れ値と言えるようなデータ点も見受けられます。

このような外れ値（outlier）を含むようなデータの近似アルゴリズムも様々存在します。
scikit-learn でも複数種類実装されていますが、
ここではHuber回帰という手法を用いたものを紹介します。

Huber回帰では、通常の最小二乗法と異なり、以下のコスト関数を最小化します。

.. math::

  \sum_i \mathcal{H}\left(\frac{y_i - \sum_j w_j \phi_j(x_i)}{\sigma}\right)

ここで、 :math:`\sigma` は外れ値を除いたノイズの分散で、これもデータから推定します。
:math:`\mathcal{H}(z)` はHuberのロス関数で、以下のように定義されるものです。

.. math::

  \mathcal{H}(z) = \begin{cases}
  \; z^2      & |z| \le 1 \\
  \; 2|z| - 1 & |z| \ge 1
  \end{cases}

簡単には、近似値の近くにある点については通常の二乗誤差を考え、
:math:`\sigma` より遠く離れている点については一乗誤差に緩和してロス関数に加えるものです。
遠く離れている点についてのコストが小さくなるため、異常値に引っ張られることが少なくなります。

ここでは、scikit-learn を用いて Huber回帰を行ってみます。

.. ipython:: python

 from sklearn import linear_model  # linear_model モジュールを用います

 # data ここでは 6800 msに得られた Te の分布を解析します
 Te = thomson.sel(Time=6800, method='nearest')['Te'].values
 R = thomson['R'].values

 # basis R:2500--5000 を10分割した点を中心とするガウス関数の和で近似しましょう
 centers = np.linspace(2500, 5000, 10)
 phi = np.exp(-((R.reshape(-1, 1) - centers) / 200)**2)

 # 最小二乗法
 lin = linear_model.LinearRegression(fit_intercept=False)
 # フィッティング
 lin.fit(phi, Te)
 # 求めたフィッティング係数を用いた予測
 Te_lin_fit = lin.predict(phi)

 # ロバスト最小二乗法
 rob = linear_model.HuberRegressor(fit_intercept=False)
 # フィッティング
 rob.fit(phi, Te)
 # 求めたフィッティング係数を用いた予測
 Te_rob_fit = rob.predict(phi)

 plt.plot(R, Te, '--o', ms=3, label='data')
 plt.plot(R, Te_lin_fit, label='linear regression', lw=2)
 plt.plot(R, Te_rob_fit, label='huber regression', lw=2)
 plt.legend(loc='best')  # 凡例を表示する
 plt.xlabel('$R$ (mm)')  # 凡例を表示する
 @savefig thomson_te_fit.png width=4in
 plt.ylabel('$T_\mathrm{e}$ (eV)')  # 凡例を表示する


通常の最小二乗法では、
異常値に引きずられて :math:`R` = 2500 mm 付近で多くの計測点から離れているのに対し、
Huber回帰ではこれら異常値に頑健なフィッティングができていることがわかります。

また実装面では、``LinearRegression`` と ``HuberRegressor`` は
引数・戻り値などの使い方が統一されています。
そのため、 ``LinearRegression`` では外れ値に影響されすぎていると感じれば、
すぐに ``HuberRegressor`` などのロバストな回帰手法を試すことができるようになっています。
他にも様々なアルゴリズムがよく似たインターフェースで提供されており、
簡単に試行錯誤を重ねることができる、ということがこのようなライブラリを用いることのメリットだと思います。

この節では、回帰問題を通して scikit-learn の使い方を簡単に紹介しました。
上記の回帰問題からもわかるように、全てのデータに無条件で合うモデルは存在しません。
よいモデルはデータに依存するため、色々なモデルを適用してみて結果を見るというような
多数回の試行錯誤が必要です。
scikit-learn では、そのような試行錯誤を簡単にできるよう工夫されて作られています。
たくさんの例がドキュメントページにまとめられているので、ぜひそちらもご覧ください。
