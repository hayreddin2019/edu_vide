# coding:utf-8
import uvicorn
from fastapi import FastAPI
import redis

r = redis.Redis(host='localhost', port=6379)

app = FastAPI()


@app.get("/")
def main(url: str = None):
    if not url:
        return {"message": "Please enter a URL"}
    if r.get(url):
        return {"message": "URL already exists"}
    r.lpush("queue", url)
    _list = url.split(",")
    return {"url": _list}


if __name__ == "__main__":
    uvicorn.run("0fast:app", host="127.0.0.1", port=61, log_level="info")
