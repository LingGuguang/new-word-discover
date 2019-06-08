#删除重复弹幕
import numpy
from collections import Counter 

class Delete(object):
    __list = []
    __most = []
    def __init__(self, data):
        self.__list = data

    def delete(self):
        if len(self.__most) == 0:
            self.most()
        self.__list = list(set(self.__list))
        return self.__list

    def get_list(self):
        return self.__list

    def isList(self):
        if(isinstance(self.__list,list)):
            return True
        else:
            return False

    #find topK times
    def most(self, k=50):
        self.k = k
        #if has counted , just return self.__most
        if len(self.__most):
            return self.__most[:self.k]
        #else test if isList
        elif self.isList():
            self.__most = Counter(self.__list).most_common(self.k)
            return self.__most
        #else data is not list
        else:
            return ['ERROR!!! Find it!']


if __name__ == '__main__':
    test = ['哈哈','哈哈','哈哈','不错','good','很强','可以','可以']
    d = Delete(test)
    print(d.most(10))
   

