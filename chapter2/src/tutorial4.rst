  スクリプトファイルを読み込む
==================================

.. ipython:: python
   :suppress:

    import numpy as np
    import matplotlib.pyplot as plt
    np.random.seed(123456)

上記の関数など、作成したスクリプトを再利用するためには、
スクリプトファイルとして作成しておくほうが良い。

スクリプトファイルと言っても、これまで学習した内容を .py ファイルに保存するだけである。
なお、import 文や変数の定義はファイルをまたいでは引き継がれないため、
スクリプトファイルごとにそれらを適宜記入する必要がある。

前節で定義した関数をスクリプトファイルとして保存するには、
以下のような内容をファイルとして保存する。
今回は、これを polar.py として保存したとする。

.. code-block:: python

  import numpy as np

  def get_xy(r, theta):
      """
      Returns x, y values from polar coordinate variable r (radial coordinate)
      and theta (angular coordinate).
      """
      x = r * np.cos(theta)
      y = r * np.sin(theta)
      return x, y

このスクリプトファイルを読み込むためには、以下のように import 文を用いる。

.. code-block:: python

    import polar

    r = np.linspace(0, 1, 31)
    theta = np.linspace(0, 4.0 * np.pi, 31)
    x, y = polar.get_xy(r, theta)

なお、import 文で読み込めるスクリプトファイルは、実行するスクリプトと同じディレクトリ内か
パスの通ったディレクトリのみとなる。
任意の場所にあるスクリプトファイルを読み込むためには

.. code-block:: python

    import sys
    sys.path.append('path/to/script')
    import polar

というようにパスを通す必要がある。
