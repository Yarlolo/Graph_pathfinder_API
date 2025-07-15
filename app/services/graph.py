import heapq
from app.core.celery_app import celery_app
import time

def dijkstra(graph, start, end):
    time.sleep(5)
    queue = [(0, start, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)

        if node not in seen:
            seen.add(node)
            path = path + [node]

            if node == end:
                return (path, cost)

            for neig, c in graph.get(node, {}).items():
                heapq.heappush(queue, (cost + c, neig, path))

    return float('inf'), []


@celery_app.task(name="find_shortest_path", bind=True, ignore_result=False)
def shortest_path(self, graph: dict, start: int, end: int):
    try:
        graph_dict = {}
        for edge in graph["edges"]:
            if edge["start"] not in graph_dict:
                graph_dict[edge["start"]] = {}
            graph_dict[edge["start"]][edge["end"]] = edge["weight"]

        path, total_distance = dijkstra(graph_dict, start, end)
        return {"path": path, "total_distance": total_distance}
    except Exception as e:
        self.retry(exc=e, countdown=5)