概要
===============================================

データ駆動科学が第４の科学的手法と言われ近年注目を集めています。
なかでもPythonは、データ科学の分野で最も人気を集めている言語です。
Tensorflowやchainer、pytorchなど、最新の深層学習ライブラリは全てPythonにて実装されています。
ただしデータ科学に重要なのは、深層学習など先端的なアルゴリズムだけではありません。
手持ちのデータを素早く可視化して内容を理解したり、
既存のアルゴリズムに渡せるよう複数データの合成、不良値や欠損値の処理、
といった前処理の部分が意外と重要で手間がかかることが知られています。

ここでは、このようなデータ科学にフォーカスされたライブラリを紹介します。
まず多次元データ処理ライブラリとして、xarray の使い方を概観します。
これらのライブラリはアルゴリズムというようりは、
多様なデータを素早く扱うことができるインターフェースを提供するものです。

次に、機械学習アルゴリズムが実装されているライブラリとして scikit-learn を紹介します。
有名なアルゴリズムが数多く集められているライブラリで、
様々なアルゴリズムを気軽に試すことが特徴です。

最後に、より高速な計算を簡単に実現することを目的として開発されている cupy というライブラリを簡単に紹介します。

Data intensive science has been recently considered as
the 4th paradigm in scientific discovery.
Among many other programming languages, Python is the most popular language
in the data science field.
Many cutting-edge packages for deep learning,
such as Tensorflow [tensorflow]_, Chainer [chainer]_ and Pytorch [pytorch]_,
have been developed for Python.
However, such cutting-edge packages are not only the important tools for data science.
It has been widely known that visualization and preprocessing are also very important,
such as to combine multiple data, removing outliers, filling missing values, etc.

In this section, we introduce several Python packages for data science.
First, we briefly show the usage of xarray, one of multi-dimensional data handling tools.
This library provides a useful interface to handle your data quickly,
rather than giving any algorithms.

Next, we introduce ``scikit-learn``, a compilation of classical machine learning algorithms.
It was designed to easily apply various algorithms to your own data.

Keywords
--------
Python, data science, libraries, machine learning, deep learning
