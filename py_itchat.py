#-*- coding:utf-8 –*-
#!/bin/bash/
import itchat
from collections import Counter
import matplotlib.pyplot as plt
import re
import snownlp
import jieba.analyse
from wordcloud import WordCloud
import numpy as np
import Image
import csv

class itchat_frends_message():
    def __init__(self,friends):
        self.friends = friends
    def itchat_friends_sex(self):
        sexs = list(map(lambda x:x['Sex'],self.friends[1:]))
        counts = list(map(lambda x:x[1],Counter(sexs).items()))
        labels = ['未知人妖','男','女']
        color = ['fuchsia','lawngreen','skyblue']

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        plt.figure(figsize=(8,5),dpi=80)
        plt.axes(aspect=1)
        plt.pie(counts,                     #性别统计结果
                labels=labels,              #性别标签
                colors=color,               #分类颜色
                labeldistance=1.1,          #标签距离圆心的距离
                autopct='%3.1f%%',          #饼图区域文本格式
                shadow=True,                #饼图是否显示阴影
                startangle=90,              #饼图起始角度
                pctdistance=0.5             #饼图区域文本距离圆心的距离
                )
        plt.legend(loc='upper right',)
        plt.title(u'%s的微信好友性别组成' % self.friends[0]['NickName'])
        plt.show()
    #好友签名
    def itchat_friends_sign(self):
        signatures = ''
        emotions = []
        pattern = re.compile("1f\d.+")
        for friend in self.friends:
            signature = friend['Signature']
            if signature!=None:
                signature = signature.strip().replace('span','').replace('class','').replace('emoji','')
                if (len(signature) > 0):
                    nlp = snownlp.SnowNLP(signature)
                    emotions.append(nlp.sentiments)
                    signatures += ' '.join(jieba.analyse.extract_tags(signature, 5))
        with open('signatures.txt', 'wt', encoding='utf-8') as file:
            file.write(signatures)
        back_coloring = np.array(Image.open('timg (1).jpg'))
        wordcloud =WordCloud(
            font_path='C:/Windows/Fonts/simfang.ttf',
            background_color="white",
            max_words=1200,
            mask=back_coloring,
            max_font_size=75,
            random_state=45,
            width=960,
            height=720,
            margin=15
        )
        wordcloud.generate(signatures)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        # Signature Emotional Judgment
        count_good = len(list(filter(lambda x: x > 0.66, emotions)))
        count_normal = len(list(filter(lambda x: x >= 0.33 and x <= 0.66, emotions)))
        count_bad = len(list(filter(lambda x: x < 0.33, emotions)))
        labels = [u'负面消极', u'中性', u'正面积极']
        values = (count_bad, count_normal, count_good)
        plt.rcParams['font.sans-serif'] = ['simHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.xlabel(u'情感判断')
        plt.ylabel(u'频数')
        plt.xticks(range(3), labels)
        plt.legend(loc='upper right', )
        plt.bar(range(3), values, color='rgb')
        plt.title(u'%s的微信好友签名信息情感分析' % self.friends[0]['NickName'])
        plt.show()

    def analyseLocation(self):
        headers = ['NickName', 'Province', 'City']
        col = []
        with open('location.csv', 'w', encoding='utf-8', newline='', ) as csvFile:
            writer = csv.DictWriter(csvFile, headers)
            writer.writeheader()
            for friend in self.friends[1:]:
                row = {}
                row['NickName'] = friend['NickName']
                row['Province'] = friend['Province']
                row['City'] = friend['City']
                col.append(friend['City'])
                writer.writerow(row)
        with open('counter.txt','w')as file:
            file.write('\n'.join('{} {}'.format(x[0],x[1]) for x in Counter(col).items()))





'''
#腾讯优图库安装不成功，故此操作未完成
    def itchat_frends_headimage(self):
        #新建文件夹
        basepath = os.path.abspath('.')
        basefolder = basepath+'\\HeadImage\\'
        if os.path.exists(basefolder)==False:
            os.makedirs(basefolder)

        #保存图片
        for index in range(1, len(self.friends)):
            friend = self.friends[index]
            # Save HeadImages
            imgFile = basefolder + '\\Image%s.jpg' % str(index)
            imgData = itchat.get_head_img(userName=friend['UserName'])
            if os.path.exists(imgFile) == False:
                with open(imgFile, 'wb') as file:
                    file.write(imgData)

'''




if __name__ == '__main__':
    itchat.auto_login(hotReload = True)
    friends = itchat.get_friends(update = True)
    ifm = itchat_frends_message(friends)
    #ifm.itchat_friends_sex()
    #ifm.itchat_friends_sign()
    ifm.analyseLocation()

