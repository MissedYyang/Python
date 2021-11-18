#自动下载乐乐课堂的视频======数学微课视频
import re
import os
import requests


def get_cid(titles,cids):
	#http://www.leleketang.com/let3/knowledges.php?grade_id=10&course_id=2
	url='http://www.leleketang.com/let3/knowledges.php?grade_id=10&course_id=2'
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
	result=requests.get(url=url,headers=headers)
	#print(result.text)
	title_all=re.findall('title="(.*?)" href="javascript:;"',result.text)
	cid_all=re.findall('data-step=.? data-cid="(.*?)" ',result.text)
	#print(title_all,cid_all)
	for i in range(len(cid_all)):
		if '人教版' in title_all[i]:
			#print(title_all[i],cid_all[i])
			titles.append(title_all[i])
			cids.append(cid_all[i])
	return titles,cids


def get_mp4all(titles,cids):
	for c in range(len(cids)):
		path="C:\\Users\\Administrator\\Desktop\\kkt\\"+(titles[c])
		if not os.path.exists(path):
			os.mkdir(path)
		os.chdir(path)
		headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
		for i in range(1,4):
			print(i)
			url2='http://www.leleketang.com/let3/knowledge_list.php?cid='+cids[c]+'&p={}'.format(i)
			result2=requests.get(url=url2,headers=headers).text
			#data-video="http://v2.leleketang.com/dat/ms/ma/k/video/27773.mp4"></div>
			#<div class="knowledge_name ellipsis">正八边形的相关计算</div>
			#print(result2.text)
			video_all=re.findall('data-video="(.*?)">',result2)
			name_all=re.findall('<div class="knowledge_name ellipsis">(.*?)</div>',result2)
			#print(name_all,video_all)
			for j in range(len(video_all)):

				f=open(name_all[j].replace('"','')+'.mp4','wb')
				f.write(requests.get(video_all[j],headers=headers,stream=True).content)
				f.close()
				print(' 下载完成： ',name_all[j])
		os.chdir(r"C:\Users\Administrator\Desktop\kkt")




titles=[]
cids=[]
titles,cids=get_cid(titles,cids)
#print(titles,cids)
get_mp4all(titles,cids)