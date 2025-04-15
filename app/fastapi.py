from dataclasses import dataclass
from dataclasses import dataclass
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.logger import Logger
from fastapi.responses import JSONResponse
import http.client
import json
import os

@dataclass
class Fastapi:

    
    host: str
    port: int
    reload: bool
    logger: any
    
    def __post_init__(self):
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="app/templates")
        self.app.mount(f"/static", StaticFiles(directory="app/static"), name="static")

    def request_medium_api(self,path: str):
        conn = http.client.HTTPSConnection("medium2.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': os.getenv("MEDIUM_API_KEY"),
            'x-rapidapi-host': "medium2.p.rapidapi.com"
        }
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data = res.read()
        self.logger.info(json.loads(data.decode("utf-8")))
        return json.loads(data.decode("utf-8"))

    def run(self):
        self.server()
        self.logger.info("Server Initialized!")
        uvicorn.run(app=self.app, host=self.host, port=self.port)
    def server(self):

        @self.app.get("/")
        async def base(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.post("/user/{user_id}")
        async def get_user_info(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}")
            return {"user_id": user_id, "endpoint": "user"}
        
        @self.app.post("/user/{user_id}/lists")
        async def get_user_info(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/lists")
            return {"user_id": user_id, "endpoint": "user"}
        
        @self.app.post("/user/{user_id}/interests")
        async def get_user_interests(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/interests")
            return {"user_id": user_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/html")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/html")
            return {"user_id": article_id, "endpoint": "user"}

        @self.app.post("/user/{user_id}/following")
        async def get_user_interests(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/following")
            return {"user_id": user_id, "endpoint": "user"}
        

        @self.app.post("/user/{user_id}/articles")
        async def get_user_articles(user_id: str, request: Request):
            return {"user_id": user_id, "endpoint": "user/articles"}
        
        @self.app.post("/user/id_for/{username}")
        async def get_user_id(request: Request, username: str):
            path = f"/user/id_for/{username}"
            data = self.request_medium_api(path)
            return JSONResponse(content=data)

        @self.app.post("/user/{user_id}/followers")
        async def get_user_followers(request: Request, user_id: str):
            query_params = await request.json()
            count = query_params.get("count", "10")
            after = query_params.get("after", "")
            after_param = f"&after={after}" if after else ""
            path = f"/user/{user_id}/followers?count={count}{after_param}"
            data = self.request_medium_api(path)
            return JSONResponse(content=data)
        
        @self.app.post("/user/{user_id}/articles")
        async def get_user_articles(request: Request, user_id: str):
            # İsteğe bağlı olarak query parametreleri alabilirsin
            query_params = await request.json()
            count = query_params.get("count", "1")  # örneğin makale sayısı
            after = query_params.get("after", "")    # sayfalama için kullanılabilir

            after_param = f"&after={after}" if after else ""
            path = f"/user/{user_id}/articles?count={count}{after_param}"

            data = self.request_medium_api(path)
            print(data)
            return JSONResponse(content=data)
        

        @self.app.post("/user/{user_id}/publication_following")
        async def get_user_interests(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/publication_following")
            return {"user_id": user_id, "endpoint": "user"}
        

        @self.app.post("/user/{user_id}/publications")
        async def get_user_interests(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/publications")
            return {"user_id": user_id, "endpoint": "user"}
        

        @self.app.post("/user/{user_id}/top_articles")
        async def get_user_interests(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/top_articles")
            return {"user_id": user_id, "endpoint": "user"}

        @self.app.post("/user/{user_id}/books")
        async def get_user_interests(user_id: str, request: Request):
            self.request_medium_api(f"/user/{user_id}/books")
            return {"user_id": user_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/markdown")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/markdown")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/assets")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/assets")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/responses")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/responses")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/fans")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/fans")
            return {"user_id": article_id, "endpoint": "user"}

        @self.app.post("/article/{article_id}/content")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/content")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/related")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/related")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/article/{article_id}/recommended")
        async def get_user_interests(article_id: str, request: Request):
            self.request_medium_api(f"/article/{article_id}/recommended")
            return {"user_id": article_id, "endpoint": "user"}
        
        @self.app.post("/publication/id_for/{publication_slug}")
        async def get_user_interests(publication_slug: str, request: Request):
            self.request_medium_api(f"/publication/id_for/{publication_slug}")
            return {"user_id": publication_slug, "endpoint": "user"}
        
        @self.app.post("/publication/{publication_id}")
        async def get_user_interests(publication_id: str, request: Request):
            self.request_medium_api(f"/publication/{publication_id}")
            return {"user_id": publication_id, "endpoint": "user"}
        
        @self.app.post("/publication/{publication_id}/articles")
        async def get_user_interests(publication_id: str, request: Request):
            self.request_medium_api(f"/publication/{publication_id}/articles")
            return {"user_id": publication_id, "endpoint": "user"}
        
        @self.app.post("/publication/{publication_id}/newsletter")
        async def get_user_interests(publication_id: str, request: Request):
            self.request_medium_api(f"/publication/{publication_id}/newsletter")
            return {"user_id": publication_id, "endpoint": "user"}
        
        @self.app.post("/archived_articles/{tag}")
        async def get_user_interests(tag: str, request: Request):
            self.request_medium_api(f"/archived_articles/{tag}")
            return {"user_id": tag, "endpoint": "user"}
        
        @self.app.post("/recommended_feed/{tag}?page={page}")
        async def get_user_interests(tag: str, request: Request, page:str):
            self.request_medium_api(f"/recommended_feed/{tag}?page={page}")
            return {"user_id": tag, "endpoint": "user", "page":page}
        
        @self.app.post("/top_writers/{topic_slug}")
        async def get_user_interests(topic_slug: str, request: Request):
            self.request_medium_api(f"/top_writers/{topic_slug}")
            return {"user_id": topic_slug, "endpoint": "user"}
        
        @self.app.post("/latestposts/{topic_slug}")
        async def get_user_interests(topic_slug: str, request: Request):
            self.request_medium_api(f"/latestposts/{topic_slug}")
            return {"user_id": topic_slug, "endpoint": "user"}
        
        @self.app.post("/topfeeds/{tag}/{mode}")
        async def get_user_interests(tag: str, request: Request, mode:str):
            self.request_medium_api(f"/topfeeds/{tag}/{mode}")
            return {"user_id": tag, "endpoint": "user", "mode":mode}
        
        @self.app.post("/related_tags/{tag}")
        async def get_user_interests(tag: str, request: Request):
            self.request_medium_api(f"/related_tags/{tag}")
            return {"user_id": tag, "endpoint": "user"}

        @self.app.post("/tag/{tag}")
        async def get_user_interests(tag: str, request: Request):
            self.request_medium_api(f"/tag/{tag}")
            return {"user_id": tag, "endpoint": "user"}
        
        @self.app.post("/root_tags")
        async def get_user_interests(request: Request):
            self.request_medium_api(f"/root_tags")
            return {"endpoint": "user"}
        
        @self.app.post("/recommended_users/{tag}")
        async def get_user_interests(tag: str, request: Request):
            self.request_medium_api(f"/recommended_users/{tag}")
            return {"user_id": tag, "endpoint": "user"}
        
        @self.app.post("/recommended_lists/{tag}")
        async def get_user_interests(tag: str, request: Request):
            self.request_medium_api(f"/recommended_lists/{tag}")
            return {"user_id": tag, "endpoint": "user"}
        
        @self.app.post("/list/{list_id}")
        async def get_user_interests(list_id: str, request: Request):
            self.request_medium_api(f"/list/{list_id}")
            return {"user_id": list_id, "endpoint": "user"}
        
        @self.app.post("/list/{list_id}/articles")
        async def get_user_interests(list_id: str, request: Request):
            self.request_medium_api(f"/list/{list_id}/articles")
            return {"user_id": list_id, "endpoint": "user"}
        
        @self.app.post("/list/{list_id}/responses")
        async def get_user_interests(list_id: str, request: Request):
            self.request_medium_api(f"/list/{list_id}/responses")
            return {"user_id": list_id, "endpoint": "user"}
        
        @self.app.post("/search/users?query={query}")
        async def get_user_interests(query: str, request: Request):
            self.request_medium_api(f"/search/users?query={query}")
            return {"user_id": query, "endpoint": "user"}

        @self.app.post("/search/articles?query={query}")
        async def get_user_interests(query: str, request: Request):
            self.request_medium_api(f"/search/articles?query={query}")
            return {"user_id": query, "endpoint": "user"}
        
        @self.app.post("/search/publications?query={query}")
        async def get_user_interests(query: str, request: Request):
            self.request_medium_api(f"/search/publications?query={query}")
            return {"user_id": query, "endpoint": "user"}
        
        @self.app.post("/search/lists?query={query}")
        async def get_user_interests(query: str, request: Request):
            self.request_medium_api(f"/search/lists?query={query}")
            return {"user_id": query, "endpoint": "user"}
        
        @self.app.post("/search/tags?query={query}")
        async def get_user_interests(query: str, request: Request):
            self.request_medium_api(f"/search/tags?query={query}")
            return {"user_id": query, "endpoint": "user"}


if __name__ == "__main__":
    pass