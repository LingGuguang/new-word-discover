# new-word-discover
基于b站弹幕的新词发现，无先验词库(是我还没加)，从单字开始发现新词。
python 3.6
直接运行find_new_word.py就能用,里面有两个参数:FREE_THRESHOLD自由度和SOLID_THRESHOLD凝固度,调节两个阈值可以限制新词的门槛.

介绍一下每个文件:
+  1.BILIBILI.py 是爬弹幕的代码,可惜b站换策略不能用了
+  2.danmu.txt 爬到的弹幕都存到这里了
+  3.perTreatment.py 删掉了特殊符号
+  4.Delete.py  把太短的弹幕删了，重复的也删了，防止例如'干死孙一峰'这种短语的凝固度太高。
+  5.save.py 相对干净的弹幕
+  6.find_new_word.py 代码里有乱七八糟的注释，请酌情观看。

由于数据少，调参不准，也没先验词表，结果没好到哪去，不过就新词发现来说，确实找到了不少网上才有的词，死肥宅、小破站、幼驯染、虎牙这种词也能找到，常用词因为有很多也能找到。



