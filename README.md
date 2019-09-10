# sanic-chatapp-toy-project  
realtime chatting application server  
python `sanic` framework + websocket + Redis(pub/sub) + PostgreSQL(save for user data)  

## Skills
back-end : Python(sanic) 
DB : Redis, PostgreSQL  
IDE : PyCharm  

## Doc
[API Doc](https://github.com/sehajyang/sanic-toy-project/wiki)

## require
Python 3.7

# How to run?
1. install requirements
```
pip install -r requirements.txt
```
2. setting .env
**environment variable**
```
* REDIS_HOST
* REDIS_PORT
* REDIS_POOL_SIZE
* PG_USER
* PG_PASSWORD
* PG_DB
* PG_HOST
```
3. run main.py
