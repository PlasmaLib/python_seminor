NumPyによる計算高速化
========================

Pythonは動的型付けを行う（実行時に型を決める言語）インタプリタであるため，柔軟で短いコードが書けたり，短時間で開発ができるメリットがあります．
このメリットだけでも十分かもしれませんが，やはり科学技術計算をしようとするならば計算速度は速いほうが望ましいです．
そこで，この節では高速な科学技術計算のためのテクニックを幾つか紹介します．

数値計算をする上でfor文による多重ループを使いたくなる事があるでしょう．
しかし，コンパイル言語ではないPythonでは，for文を用いると処理が非常に遅くなります．
そこで，NumPyの組み込み関数(universal function)を活用します．
ユニバーサル関数とは，ndarrayの全要素に対して，ブロードキャスティングにより要素ごとに演算処理を行い，結果をndarrayで返す関数です．
これらの関数はCやFortranで実装されており，かつ線形演算ではBLAS/LAPACKのおかげで，C/C++と遜色のないほど高速で動作します．

Pythonのコードで良いパフォーマンスを得るには，以下の事が重要です．

* Pythonのループと条件分岐のロジックを，配列操作と真偽値の配列の操作に変換する
* 可能なときは必ずブロードキャストする
* 配列のビュー（スライシング）を用いてデータのコピーを防ぐ
* ufuncとufuncメソッドを活用する

計算速度の比較として，for文，sum関数，NumPyを使った場合の例を紹介します．

for文を使って１から１億までの和を計算する（Python的な書き方ではない）
---------------------------------------------------------------------

.. ipython:: python
    
    def test_for_loop():
        #tick = time.time()
        s = 0
        for i in range(1, 100000001):
            s += i
        #print('Calculation result: %d' % s)
        #tock = time.time()
        #print('Time of test_for_loop: %.06f[s]' % (tock-tick))
        return s


1から1億を返すイテレータを用意し，その和を計算する
---------------------------------------------------------------------

.. ipython:: python
    
    def test_sum():
        #tick = time.time()
        s = sum(range(1, 100000001))
        #print('Calculation result: %d' % s)
        #tock = time.time()
        #print('Time of test_sum: %.06f[s]' % (tock-tick))
        return s

NumPyを使い，1から1億が入った配列を用意し，その和を計算する
----------------------------------------------------------------------

.. ipython:: python

    def test_numpy_sum():
        #tick = time.time()
        a = np.arange(1, 100000001, dtype=np.int64)
        #print('Calculation result: %d' % a.sum())
        #tock = time.time()
        #print('Time of test_numpy_sum: %.06f[s]' % (tock-tick))
        return a.sum()
    
用意した関数を実行して，計算速度を比較してみましょう．
今回は以下のような環境で実行時間を計測しました．

+--------+-----------------------+
| OS     | macOS 10.12.6         |
+--------+-----------------------+
| Kernel | Darwin 16.7.0         |
+--------+-----------------------+
| CPU    | 2.8 GHz Intel Core i7 |
+--------+-----------------------+
| Python | 3.5.4                 |
+--------+-----------------------+
| NumPy  | 1.11.3                |
+--------+-----------------------+

まずは計算結果を確認します．

.. ipython:: python
    
    print('Result of test_for_loop: %d' % (test_for_loop()))
    print('Result of test_sum: %d' % (test_sum()))
    print('Result of test_numpy_sum: %d' % (test_numpy_sum()))

処理時間を計測するために，標準ライブラリの ``timeit`` を用いてみます．
ここでは，それぞれの関数を10回実行し，1回あたりの実行時間を表示しています．
なお，実行回数を指定するnumberの初期値は100万ですので，時間のかかる処理を初期値のまま行ってしまわないように注意して下さい．

.. ipython:: python
    
    import timeit
    print('Time of test_for_loop: %.06f[s]' % (timeit.timeit(test_for_loop, number=10)/10))
    print('Time of test_sum: %.06f[s]' % (timeit.timeit(test_sum, number=10)/10))
    print('Time of test_numpy_sum: %.06f[s]' % (timeit.timeit(test_numpy_sum, number=10)/10))

このように，np.sumを用いると，for文を用いた場合に比べて計算時間を10分の1以下に抑えることができる場合があります．

numpy.whereを用いた条件制御
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

次に，ブロードキャストを利用した高速化の例として，ユニバーサル関数であるnp.whereを用いた例を紹介します．
科学技術計算をする上で，for文とともに頻出なのが三項演算子（条件文）である ``x if condition else y`` の処理でしょう．
np.whereはこの三項演算子のベクトル演算版です．
x, yを配列または数値として， ``np.where(条件, x, y)`` のように書きます．
まずは簡単な例として，真偽値の配列condと２つの配列xarr, yarrを用いて挙動を見てみましょう．

.. ipython:: python

    cond = np.array([True, True, False, True, False])
    xarr = np.array([1.0, 1.1, 1.2, 1.3, 1.4]) 
    yarr = np.array([2.0, 2.1, 2.2, 2.3, 2.4])

cond, xarr, yarrを上記のように定義します．
このとき，condの要素がTrueであればxarrの同位置の要素を，Falseであればyarrの同位置の要素を取る処理を考えます．
これをPythonのリスト内包を用いて書くと次のようになります．
    
.. ipython:: python
    
    result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
    result
    
しかし，この方法には，「対象配列が大きくなると動作が遅くなる」，「多次元配列に対応できない」，といった問題があります．
np.whereを用いることで，これらの問題を解決し，以下のように簡単に記述することができます．

.. ipython:: python
    
    result = np.where(cond, xarr, yarr)
    result

np.whereの2番目と3番目の引数（先ほどの例ではxarr, yarr）は，配列でなくスカラー値を取ることもできます．
np.whereを使う主な場面は，ある配列を基にして別の配列を作るようなときでしょう．

例として，乱数を格納した配列を考えます．
それぞれの要素を置き換え，正の場合は2にする事を考えます．
この操作は，np.whereを使って以下のように書くことができます．

.. ipython:: python
    
    arr2d = np.random.randn(4, 5)   #4 × 5の乱数データを作成
    arr2d
    np.where(arr2d > 0, 2, arr2d)
    
np.where関数に配列を渡すとき，同じサイズの1つの配列や1つのスカラー値を渡す以外にも別の方法がありますので，その一例を紹介します．
2つの真偽値の配列cond1とcond2があるとします．
このとき，とりうる真偽の組は4種類あります．
この種類に応じて，それぞれ別の値を割り当てたいとします．
この処理をPython標準機能で書くと次のようになります．

.. code-block:: python

    result = []
    for i in range(n):
        if cond1[i] and cond2[i]:
            result.append(0)
        elif cond1[i]:
            result.append(1)
        elif cond2[i]:
            result.append(2)
        else:
            result.append(3)

これをnp.whereを使って書くと次のようになります.
   
.. code-block:: python

    np.where(cond1 & cond2, 0,
        np.where(cond1, 1, 
            np.where(cond2, 2, 3)))

Pythonの処理を高速化するには，ndarrayのユニバーサル関数や演算を用いて可能な限りforループを使わずに基礎的な数値計算を実装することが鍵になります．




