# yc_webtool
## Environment

Python 3.9.13


## Description 

透過 Flask 架設內部平台並且透過對接 api 讓以下平台的操作可以統一進行在內部頁面。

1. CDNW
2. YCCDN
3. JulyCDN 
4. Cnzz友盟網站統計


![image](https://github.com/bosco85828/yc_webtool/assets/102674291/9708687f-2879-4c59-88b8-29e866bf46f3)
![image](https://github.com/bosco85828/yc_webtool/assets/102674291/28716d58-d010-4a7f-abbd-b0d1d4cb279d)



## 使用方式

* 新建 Docker 
```
docker run -it -d --name YCtool -v /home/devops6391/yc_tool:/yc_tool -p 80:5000  python:3.9.13
```

* 安裝 python 所需套件
```
python -m pip install -r requirements.txt 
```

* 啟動服務
```
nohup gunicorn -w 5 -t 0 -b 0.0.0.0:5000 app:app --access-logfile /yc_webtool/access.log --error-logfile /yc_webtool/error.log --log-level info &
```

* DB 

更新方式
```
flask db migrate -m '備註內容'  #提交當前 models 檔案更新
flask db upgrade   #將當前映射 db upgrade 到下一版本
```
