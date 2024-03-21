from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from tool import anno_totext
from tool import cleaning

#Open driver and page
driver = webdriver.Chrome()
time.sleep(3)
url_list=['https://namu.wiki/w/%EC%9D%B4%EB%A7%90%EB%85%84',
          'https://namu.wiki/w/%EC%B9%A8%EC%B0%A9%EB%A7%A8']

for url in url_list:
    driver.get(url) #나무위키 링크

    #Create Annotation DB
    annotation_path=driver.find_elements(By.CLASS_NAME, 'rsWhfw9f') # 주석탭 div 상위 div,,
    if annotation_path[-1].text.startswith('[1]'):
        annotation_text=annotation_path[-1].text
    elif annotation_path[-2].text.startswith('[1]'):
        annotation_text=annotation_path[-2].text
    annotation_dict={}
    for index,i in enumerate(annotation_text.split('\n')):
        try:
            txt=i.split('] ')[1]
            if txt!='링크':
                annotation_dict[str(index+1)]=txt
            else:
                annotation_dict[str(index+1)]=''
        except:
            pass
    #Parsing Table
    web_table=driver.find_element(By.CLASS_NAME, '-o8je-6h._a5b5640faca9f1712f81cb0b01f8ea51').find_elements(By.TAG_NAME, "tr") # table
    table_list=[row.text for row in web_table if len(row.text)>=2]
    anno_totext(table_list,annotation_dict)
    table_list=[i.replace("\n"," : ",1) for i in table_list]
    table_list=[i.replace("\n"," ") for i in table_list]
    cleaning(table_list)

    #Parsing Text Page
    q=driver.find_elements(By.CLASS_NAME, 'OI-CF\\+jx') # 문단별 내용 div
    li=[]
    for i in q:
        if not i.find_elements(By.TAG_NAME, 'table'):
            j=i.find_elements(By.TAG_NAME,'div')
            for c in j:
                if len(c.text)>=2 :
                    li.append(c.text)

    #Remove Blockquote writer
    remove_list=[]
    for j in driver.find_elements(By.TAG_NAME,'blockquote'):
        try :
            remove_list.append(j.text.split('\n')[1])
        except:
            pass
    wiki_text=[i for i in li if i not in remove_list][:-2]

    anno_totext(wiki_text,annotation_dict)
    wiki_text_list=[]
    for text in wiki_text:
        wiki_text_list.extend(text.split('\n\n'))
    cleaning(wiki_text_list)

    

    #ToTxtFile
    file_name = 'wiki_text.txt'
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write('\n'.join(table_list+wiki_text_list))

driver.quit()