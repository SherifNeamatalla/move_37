from fastapi import FastAPI, Body
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from server.server_runner import do_list_agents, do_create_agent, do_load_agent, do_chat, do_act
from src.config.app_config_manager import AppConfigManager
from src.config.env_loader import load_env


class ActResponseBody(BaseModel):
    command_response: str
    command: dict


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_env()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/agent/list")
async def list_agents():
    return do_list_agents()


# Define the endpoint for your service
@app.post("/agent/create")
async def create_agent(name: str, role: str, goals: list, config: dict):
    return do_create_agent(name, role, goals, config)


@app.get("/agent/load/{agent_id}")
async def load_agent(agent_id: str):
    return do_load_agent(agent_id)


@app.post("/agent/chat/{agent_id}")
async def chat(agent_id: str, message: str = Body(...)):
    return do_chat(agent_id, message)


@app.post("/agent/act/{agent_id}")
async def act(agent_id: str, body: ActResponseBody):
    command_response = body.command_response
    command = body.command
    return do_act(agent_id, command_response, command)


if __name__ == "__main__":
    import uvicorn

    AppConfigManager()

    uvicorn.run(app, host="0.0.0.0", port=8000)
