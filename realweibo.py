from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import os
import re
import xlwt
import pandas as pd

current_Path = os.path.dirname(os.path.abspath(__file__)) + '\\'


base_url = 'https://s.weibo.com/'

headers = {
    'Host':'m.weibo.cn',
    'Refer':'https://weibo.com/zzk1996?is_all=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.48'
}

#搜索
def get_Research(research_Words,page):
    params = {
        'q': research_Words,
        'Refer': 'index',
        'page': str(page)
    }
    url = 'https://s.weibo.com/weibo?' + urlencode(params)
    #print(url)
    # print(urlencode(params))

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None


def get_Information(research_Words,page):
    res = []
    html = get_Research(research_Words,page)
    doc = pq(html)
    #print(doc)
    with open(current_Path + 'test.txt','w+',encoding = 'utf8') as f:
        f.write(html)
    # items = doc(".content").items()
    items = doc("div[class='card']").items()
    
    for li in items:
        temp_Info_Dict = {}
        
        ###抽取昵称
        info = li.find('div')('.name')
        nick_Name = info.attr('nick-name')
        temp_Info_Dict['博主id'] = nick_Name
        ###抽取内容
        # text = li('.txt')
        text = li("p[node-type='feed_list_content_full']>a")
        temp_Info_Dict['微博正文'] = text.text()
        if temp_Info_Dict['微博正文'] == '':
            text = li("p[node-type='feed_list_content']>a")
            temp_Info_Dict['微博正文'] = text.text()
        #print(text.text())
        #print(temp_Info_Dict['微博正文'])
        ###时间&设备
        time_Device = li("p[class='from']>a").text()
        temp_Info_Dict['发布时间'] = time_Device
        ###转发数 评论数 点赞数
        forwards = li('.card-act li').items()#("a[action-type='feed_list_forward']")
        for i,forward in enumerate(forwards):
            num = re.sub("\D","",forward.text())
            #print(num)
            if num == '':
                num = 0
            else:
                num = int(num)
            if i == 1:
                temp_Info_Dict['转发'] = num
            elif i == 2:
                temp_Info_Dict['评论'] = num
            elif i == 3:
                temp_Info_Dict['点赞'] = num
            #print(forward.text())
        res.append(temp_Info_Dict)
        #print(res)
    return res
        ###发布时间


##导出excel
def export_excel(export):
    pf = pd.DataFrame(list(export))
    #指定字段顺序
    order = ['博主id','微博正文','转发','评论','点赞','发布时间']
    pf = pf[order]
    file_path = pd.ExcelWriter(current_Path + 'name.xlsx')
    pf.fillna(' ',inplace = True)
    #输出
    pf.to_excel(file_path,encoding = 'utf-8',index = False)
    #保存表格
    file_path.save()



def main():
    lis = []
    #for i in range(1,10):
    lis += get_Information('#尼日利亚爆发不明疾病#',1)
    #print(lis)
    export_excel(lis)

if __name__ == '__main__':
    main()
    # pool = Pool()
    # groups = ([x*20 for x in range(GROUP_START,GROUP_END+1)])
    # pool.map(main,groups)
    # pool.close()
    # pool.join()

