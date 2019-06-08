import numpy as np 
import re
import math 

class newWord(object):
    
    #limit是匹配的最大词语长度，例如limit=3，天下无双长度为4，就不匹配。
    #我限定最长7最短2
    def __init__(self, tolerance):
        self.tolerance = tolerance
        self.MAX_TOLERANCE = 5
        self.FREE_THRESHOLD = 2 #自由度阈值
        self.SOLID_THRESHOLD = 45   #凝固度阈值
        self.words = []
        self.prob = {} #频率用字典好查
        self.nighbor_words = {} #左右邻词频率
        self.new_words = {}

    #预处理+分词,contents是句子的list集合
    def make_words_dict(self, content):
        #文章切成小句，并用空格分割，本质还是一整个字符串
        content = self.pre_treatment(content)
        if content:
            #正则切割字符串,并存到词典里
            #还没添加字典匹配分割!!!!!!还不能用！！！！--------------
            all_words = re.findall(r'[a-z][A-Z]+|\s+|[\u4e00-\u9fff]', content)
            self.words.extend(all_words)

    def pre_treatment(self, content):
        #\W+匹配所有不成串的字符串，例如标点和空格，约等于[^0-9a-zA-Z_],^表示不匹配，即不匹配[^...]里的字符。
        content = re.sub(r'\W+', ' ', content)

        #可以添加新的处理，例如停用词，替换词
        #
        return content

    def start_find(self):
        #1.计算词频率和左右邻词
        self.tf_LRwords()
        #2.自由度和凝固度
        self.calc_free_solid()
        #3.比对字典,找到多出来的词
        self.compare()
        #4.考虑要不要加进字典，
        self.insert_to_dict()

    def compare(self):
        return None
    
    def insert_to_dict(self):
        return None

    def tf_LRwords(self):
        tolerance = self.tolerance
        if tolerance > self.MAX_TOLERANCE or tolerance < 2:
            raise Exception(1, 'tolerance overfitting')

        #向右得到tolerance内的所有组合，len_words是所有可能的开头词个数，len_contents是总共有多少词
        self.len_words = len(self.words)-tolerance + 1
        self.len_contents = len(self.words)

        #得到单词序列
        for begin in range(self.len_words):
            #从单字开始，end表示结尾词的id
            for add in range(tolerance):
                #end是词组结尾编号
                end = begin + add
                # 如果跨句了(到文章结尾了)，结束
                if end > self.len_contents:
                    return None
                
                word = ''.join(self.words[begin:end+1])
                # 如果跨句了(匹配到空格了)，跳过。
                if re.findall(r'\s+', word):
                    #因为用的是range，所以只能浪费时间break了，而不能重新定位begin到空格之后。
                    break 
                
                # 放到频率库里,而且有些长词本质是常搭配的短语，例如'怕上火喝王老菊'，出现的多但
                # 却只是个总出现的短语，不能被当作词，所以要对此进行惩罚，以1/单词数作为每次增
                # 加的次数。
                if word not in self.prob.keys():
                    self.prob[word] = 1/self.len_words
                else :
                    self.prob[word] += 1/self.len_words
                
                #以下计算词组的左右邻词
                left_word_id = begin - 1
                right_word_id = end + 1

                if word in self.nighbor_words.keys():
                    #if else 避免遇到文章头尾溢出,strip()避免左右邻近是空格，空格去掉了也是空字符串
                    left_word = self.words[left_word_id].strip() if left_word_id > -1 else ''
                    right_word = self.words[right_word_id].strip() if right_word_id < self.len_contents else ''

                    #开始创建左右邻词表
                    '''
                        本来要存很多元组塞到list里作为左右邻接词的存储结构，但发现占太大内存了。
                        所以找了其他人的解决办法，发现字符串占更小内存。
                        最后打算用分隔符‘ - ’作为词与词和频率与频率的分割，并把每次的结果都
                        保存成字符串,例如(数据-智商-词汇,195-247-102)这样。
                        数据结构太重要了。
                    '''
                    if left_word:
                        left_word_tuple = self.nighbor_words[word]['left_word']
                        #如果
                        left_word_list = [item for item in left_word_tuple[0].split('-') if item]
                        left_word_freq = [item for item in left_word_tuple[1].split('-') if item]
                        
                        if left_word in left_word_list:
                            num_id = left_word_list.index(left_word)
                            freq = str(int(left_word_freq[num_id]) + 1) 
                            left_word_freq[num_id] = freq
                        else :
                            left_word_list.append(left_word)
                            left_word_freq.append('1')
                        left_word_str = '-'.join(left_word_list)
                        left_word_freq = '-'.join(left_word_freq)
                        self.nighbor_words[word]['left_word'] = (left_word_str, left_word_freq)

                    if right_word:
                        right_word_tuple = self.nighbor_words[word]['right_word']
                        #如果
                        right_word_list = [item for item in right_word_tuple[0].split('-') if item]
                        right_word_freq = [item for item in right_word_tuple[1].split('-') if item]
                        
                        if right_word in right_word_list:
                            num_id = right_word_list.index(right_word)
                            freq = str(int(right_word_freq[num_id]) + 1) 
                            right_word_freq[num_id] = freq
                        else :
                            right_word_list.append(right_word)
                            right_word_freq.append('1')
                        right_word_str = '-'.join(right_word_list)
                        right_word_freq = '-'.join(right_word_freq)
                        self.nighbor_words[word]['right_word'] = (right_word_str, right_word_freq)
                else :  #词不在左右邻词里
                    left_word = self.words[left_word_id].strip() if left_word_id > -1 else ''
                    right_word = self.words[right_word_id].strip() if right_word_id < self.len_contents else ''
                    #元组储存词与出现次数，为了后面不出错还是要给元组赋空元组的
                    left_word_tuple = (left_word, '1') if left_word else ('', '')
                    right_word_tuple = (right_word, '1') if right_word else('', '')

                    self.nighbor_words[word] = {
                        'left_word': left_word_tuple,
                        'right_word': right_word_tuple,
                    }
    # 自由度and凝固度
    def calc_free_solid(self):
        for word in self.nighbor_words.keys():
            free = self.calc_free(word)
            solid = self.calc_solid(word)
            #考虑修改这里，可能solid和free的一种加权更合理，否则太难规定阈值了
            if free > self.FREE_THRESHOLD and solid > self.SOLID_THRESHOLD:
                self.new_words[word] = int(self.prob[word]*self.len_words)
    
    #自由度
    def calc_free(self, word):
        #得到左右词
        left_tuple = self.nighbor_words[word]['left_word']
        right_tuple = self.nighbor_words[word]['right_word']
        left_all_words_freq = [int(item) for item in left_tuple[1].split('-') if item]
        right_all_words_freq = [int(item) for item in right_tuple[1].split('-') if item] 
        left_entropy = self.calc_entropy(left_all_words_freq)
        right_entropy = self.calc_entropy(right_all_words_freq)
        return left_entropy if left_entropy < right_entropy else right_entropy 

    #凝固度
    def calc_solid(self, word):
        #把它分开成单个词。考虑加分隔符存储，但也要考虑字典的查询问题。
        words = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', word)
        len_words = len(self.words)
        all_solid = []
        for word_id in range(1, int(len(words)), 1):
            first_word = self.prob[''.join(word[:word_id])]
            second_word = self.prob[''.join(word[word_id:])]
            word_prob = self.prob[word]
            final_prob = (word_prob*len_words)/(first_word*second_word)
            all_solid.append(final_prob)
        return min(all_solid) if all_solid else 0.0

    #用信息熵计算两个度
    def calc_entropy(self, words_freq):
        entropy = float(0)
        sum_freq = sum(words_freq)
        for word_freq in words_freq:
            P = word_freq/sum_freq
            entropy -= P*math.log(P,2)
        return entropy
    

if __name__ == '__main__':
    #输入的文本需要是整个一个大字符串，make_words_dict里会有数据清洗的代码，
    #可是还没有实现词库匹配分割，所以只能从单字开始发现单词

    '''
    要想使用本代码，总共分两步：
    1. 词的预处理和分词，在make_words_dict里
    2. 开始发现新词
    '''
 
    string = ''
    with open('save.txt', 'r', encoding='utf-8') as f:
        for content in f.readlines():
            string = ''.join([string,content.replace('\n', ' ')])
    #print(string)
    wte = newWord(3)
    wte.make_words_dict(string)
    wte.start_find()
    print(wte.new_words)
