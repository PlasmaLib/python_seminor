SciPyを用いたPredator-Preyモデルのシミュレーション
=================================================

本章の最後に，SciPyを用いた微分方程式の解法例として，predator-preyモデルのシミュレーションについて紹介します．

帯状流と乱流の相互作用は，捕食者—被食者(Predator-Prey)モデルで記述されることが知られており [PP]_ ，このモデルは１階の連立微分方程式の形をしています．
SciPyパッケージのodeintモジュールを使うと１階の常微分方程式の数値解を簡単に得ることが出来ます [#]_ ．
odeintはLSODA(Livermore Solver for Ordinary Differential equations with Automatic switching for stiff and non-stiff problems)法を利用した汎用的な積分器ですが，
詳しくはODEPACK Fortran library  [ODE]_ を参照して下さい．

まずは，ソースコードを見てみましょう．

.. literalinclude:: predator_prey.py
    :language: python
    :linenos:

.. image:: predator_prey.png
    
プログラムの内容は以下のようになっています．

#. 解析する関数（この場合predator_prey）を定義する
    * 第1引数fが微分方程式中の未知関数
    * 第2引数tが関数のパラメータ（時間に対応）
    * 第3 \- 6引数a, b, c, dが定数
    * 戻り値がパラメータtにおけるdx/dt, dy/dtを与える
#. 微分方程式の定数a, b, c, dを与える
#. 微分方程式の初期値f0を与える
#. 未知関数の解析範囲(時間)を与えるパラメータ列tを用意する
#. 関数 ``SciPy.integrate.odeint`` に1 \- 4を引数にして呼び出す
#. 戻り値がパラメータtに対応する未知関数fの各値となる

.. プログラムの内容が理解できた所で，計算結果を解釈してみましょう．

帯状流とプラズマ乱流の相互作用を当てはめて考えてみると，乱流を餌として発生・成長する帯状流は捕食者の役割を，またプラズマ圧力勾配により発生する線形不安定性を源として成長する乱流は被食者の役割を果たします．

このようにPythonを用いることで，簡単にモデルの計算と可視化をすることができます．
コーディングの時間を短縮し，試行錯誤に多くの時間を割けるのがPythonの利点でもありますので，みなさんもまずは簡単なプログラムを作成し，動作を確認してみて下さい．

.. Pythonのスピード感を体感してみて下さい．

.. [PP] 小林すみれ　他：プラズマ・核融合学会誌 **92**, 211 (2016).
.. [ODE] http://people.sc.fsu.edu/~jburkardt/f77_src/odepack/odepack.html
.. [#] なお，高階の微分方程式でも，１階の微分方程式に変換することでodeintを用いて計算することができます．
