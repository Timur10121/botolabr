from pydantic import BaseModel
from typing import Optional, List, Any


# ── Auth ──────────────────────────────────────────────────────────────────

class RegisterBody(BaseModel):
    username: str
    email: str
    password: str


class LoginBody(BaseModel):
    username: str
    password: str


class UpdateProfileBody(BaseModel):
    name:     Optional[str] = None
    lastname: Optional[str] = None
    email:    Optional[str] = None
    username: Optional[str] = None


class ChangePasswordBody(BaseModel):
    current_password: str
    new_password: str


# ── Bots ──────────────────────────────────────────────────────────────────

class ConnectBotBody(BaseModel):
    token: str


class CheckBotBody(BaseModel):
    token: str


# ── Scenarios ─────────────────────────────────────────────────────────────

class ScenarioNode(BaseModel):
    id:   str
    type: str
    x:    Optional[float] = 0
    y:    Optional[float] = 0
    data: Optional[Any]   = None   # node-specific payload


class ScenarioEdge(BaseModel):
    id:     str
    source: str
    target: str
    label:  Optional[str] = None


class ScenarioBody(BaseModel):
    bot_id:      int
    name:        str
    description: Optional[str]             = ""
    trigger:     Optional[str]             = ""
    nodes:       Optional[List[Any]]       = []
    edges:       Optional[List[Any]]       = []


class UpdateScenarioBody(BaseModel):
    name:        Optional[str]       = None
    description: Optional[str]       = None
    trigger:     Optional[str]       = None
    nodes:       Optional[List[Any]] = None
    edges:       Optional[List[Any]] = None
    active:      Optional[bool]      = None


# ── Webhook ───────────────────────────────────────────────────────────────

class WebhookUpdate(BaseModel):
    update_id:      int
    message:        Optional[Any] = None
    callback_query: Optional[Any] = None
