関数を定義して使う
=======================

.. ipython:: python
   :suppress:

    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(123456)


これまで、``np.sin`` を始めとする関数を用いてきた。
このように、何か操作をして値を返すもの（ファイルを保存するなど値を返さないものもある）
を関数と呼ぶ。
本節ではこのような関数を定義して用いる方法について述べる。

なお、もし Numpy などの外部パッケージが同様の操作を行う関数を定義している場合は
そちらを用いる方がよいことがほとんどである。
既存のパッケージは、大勢で作成・動作確認しているため、
個人が作成したものよりもバグが圧倒的に少ない。
さらに Numpyのように C や Fortranを裏で利用することで、高速化の工夫を行っていることも多い。

以下に、例として極座標変数 (r, theta) から直行座標での値 (x, y) への変換を行う
関数の定義を示す。

.. ipython:: python

    def get_xy(r, theta):
        """
        Returns x, y values from polar coordinate variable r (radial coordinate)
        and theta (angular coordinate).
        """
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

上記のように、関数の定義は ``def`` 文から始め、関数名( ``get_xy`` )の次にカッコ内に引数( ``r``, ``theta``) を
指定し、コロンの後に改行する。
関数の範囲はインデントにより示すことが必要である。
慣習として関数名は小文字で始めることが多い。

また動作上必須ではないが、 ``def`` 文の次の行にはその関数の説明、操作の内容や引数・戻り値の意味などを
３つのダブルコーテーションで囲った文字列として書いておくことが推奨されている
（この説明はdocstringsと呼ばれる）。
docstrings を記述しておくことで、メンテナンス時に関数の役割を思い出しやすいほか、
Jupyter-notebookなどの開発環境では
その使用法をソースコードを読むことなく理解できる。
自身で使うだけのプログラムでも、簡単に記述しておくことが重要である。

関数の内部（インデントで示される領域）では必要な計算を行い、
必要であれば ``return`` 文で値を返す。
なお、Pythonの関数は複数の値を返すことができる。
その場合、戻り値はそれらを含むタプルとなる。


定義した関数は以下のように、引数にオブジェクトを渡すことで実行できる。

.. ipython:: python

    r = np.linspace(0, 1, 21)
    theta = np.linspace(0, 4.0 * np.pi, 21)
    x, y = get_xy(r, theta)
    @savefig tutorial3_plot1.png width=4in
    plt.plot(x, y)
