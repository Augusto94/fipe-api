import json
import os

import redis
from google.cloud import tasks_v2

if os.getenv("ENVIRONMENT") == "local":
    # Conectar-se ao Redis
    redis_client = redis.Redis(host="redis", port=6379, db=0)
else:
    # Configurações do Cloud Tasks
    project_id = "fipe-300f7"
    location = "southamerica-east1"
    queue = "fipe-queue"

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(project_id, location, queue)


async def send_to_queue(marca):
    if os.getenv("ENVIRONMENT") == "local":
        # Envia mensagem para redis local
        redis_client.rpush("marcas-queue", json.dumps(marca))
    else:
        # Cria task no serviço do Cloud Tasks
        task = {
            "http_request": {
                "http_method": "POST",
                "url": "https://api-2-6cu7fqvgrq-rj.a.run.app/veiculos",
                "body": json.dumps(marca).encode("utf-8"),
                "headers": {"Content-Type": "application/json"},
            }
        }
        client.create_task(request={"parent": parent, "task": task})
