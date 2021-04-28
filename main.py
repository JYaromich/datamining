import os
from collections import deque
from multiprocessing import Process

import dotenv
import pymongo
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from handshake.spiders.instagram import InstagramSpider


def parse_vertex(nodes: list):
    dotenv.load_dotenv('.env')

    crawler_settings = Settings()
    crawler_settings.setmodule('handshake.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(
        InstagramSpider,
        login=os.getenv('USERNAME'),
        password=os.getenv('ENC_PASSWORD'),
        usernames=nodes
    )
    crawler_proc.start()


def update_graph(nodes: list, graph: dict):
    process = Process(target=parse_vertex, args=(nodes,))
    process.start()
    process.join()
    # parse_vertex(nodes)
    collection = pymongo.MongoClient('mongodb://localhost')['gb_data_mining']['instagram_graph']

    for node in nodes:
        document = collection.find_one({'account': node})
        graph[document['account']] = document['vertex']
    collection.drop()
    return graph


def get_path(parent, finish, start):
    result = [finish]
    current = finish
    while True:
        if current == start:
            return ' -> '.join(result)
        current = parent[current]
        result.insert(0, current)


if __name__ == '__main__':
    start = 'jane19937788'
    finish = 'anastasia_yaromich'

    visited = [start]
    parent = dict()
    parent[start] = None

    deq = deque([start])
    graph = dict()
    while len(deq) > 0:
        current = deq.pop()

        if current == finish:
            break

        graph = update_graph([current], graph)
        for vertex in graph[current]:
            if vertex not in visited:
                visited.append(vertex)
                parent[vertex] = current
                deq.appendleft(vertex)

    print(get_path(parent, current, start))
