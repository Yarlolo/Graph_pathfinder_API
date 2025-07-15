from fastapi import APIRouter, Depends, HTTPException, Body
from app.schemas.graph import GraphRequest, PathResult, TaskResponse
from app.core.security import get_current_user
from app.services.graph import shortest_path
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from pydantic import BaseModel

router = APIRouter()


@router.post('/кратчайший-путь/', response_model=TaskResponse, summary='Запуск задачи поиска пути')
async def start_find_path(
        request: GraphRequest,
        email: str = Depends(get_current_user)):

    graph_dict = {
        'nodes': request.nodes,
        'edges': [{'start': edge.start, 'end': edge.end, 'weight': edge.weight}
                  for edge in request.edges]}

    task = shortest_path.delay(graph_dict, request.start, request.end)

    return {
        "task_id": task.id,
        "status": "В очереди на выполнение",
        "message": "Задача принята в обработку"}


class TaskIDRequest(BaseModel):
    task_id: str

@router.post('/проверка_статуса',response_model=PathResult | TaskResponse,
             summary='Проверка статуса задачи')
async def check_task_status(request: TaskIDRequest = Body(...,
                                    example={"task_id": "690072bc-aa0c-4183-bbbb-f7d10e0d9584"},
                                    description="Запрос должен содержать task_id в формате UUID")):

    task_id = request.task_id.strip()
    task = AsyncResult(task_id, app=celery_app)

    if task.state == 'PENDING':
        return {
            "status": "Ключ отсутсвует",
            "task_id": task_id,
            "message": "Задача с переданным id не найдена"}

    elif task.state == 'SUCCESS':
        if task.result is None:
            raise HTTPException(
                status_code=500,
                detail="Результат задачи отсутствует")
        return task.result

    elif task.state == 'FAILURE':
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Ошибка выполнения задачи",
                "task_id": task_id,
                "details": str(task.result) if task.result else None})

    else:
        return {
            "status": task.state,
            "task_id": task_id}
