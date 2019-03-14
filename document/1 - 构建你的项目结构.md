# 第一篇 - 构建项目结构

## 简介

当我们开始写一个新的项目时 , 第一件事就是想好怎样来管理我们的项目结构 , 以 Django 的默认模板为例 , 你的项目可能是这样的

```python
mysite
├── mysite             
│   ├── __init__.py
│   ├── settings.py    
│   ├── urls.py        
│   └── wsgi.py   
│   blog
│   ├── migrations         
│   │   └── __init__.py     
│   ├── __init__.py        
│   ├── admin.py      
│   ├── apps.py        
│   ├── models.py       
│   ├── tests.py     
│   └── views.py  
│   ...
├── db.sqlite3         
└── manage.py          
```

当然这并没有什么不好的 , 只不过当你的app数量增多 , 以及其他相关的代码 , 会渐渐使你的项目变得乱起来 , 通常 , 前后端分离 , 我们更关注的是那些 API , 所以将所有的 API 存放在一类目录这是一个不错的选择 , APP 也应该作为一个分类存放 : 

```python
mysite
├── mysite  # 项目根目录            
│   ├── __init__.py
│   ├── settings.py    
│   ├── urls.py        
│   └── wsgi.py   
├── apps    # APP存放目录
│   ├── blog
│   │   ├── migrations         
│   │   │   └── __init__.py     
│   │   ├── __init__.py        
│   │   ├── admin.py      
│   │   ├── apps.py        
│   │   ├── models.py       
│   │   ├── tests.py     
│   │   └── views.py  
│   ├── ...        
├── api      # API存放目录
│   ├── handler
│   │   └── blog.py 
│   ├── middlewares  # 中间件存放
│   └── ...
├── utils     # 项目工具包
├── script    # 项目使用的脚本
├── deploy    # 项目部署配置
├── db.sqlite3         
└── manage.py     
```

当然这只是一些建议 , 你也可以根据自己的习惯来进行分类 , 但是对于 API , 也就是你写的那些视图 , 我还是希望你存放在一个文件夹中 , 因为那样你在注册你的 API 时能够一目了然

## 新的开始



