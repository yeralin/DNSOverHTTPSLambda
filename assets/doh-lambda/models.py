from pydantic import BaseModel
from typing import Dict, List, Optional

from utils import to_camel


class Model(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Http(Model):
    method: str
    path: str
    protocol: str
    source_ip: str
    user_agent: str


class RequestContext(Model):
    route_key: str
    account_id: str
    stage: str
    api_id: str
    domain_name: str
    domain_prefix: str
    request_id: str
    time: str
    time_epoch: int
    http: Http


class APIGatewayV2HTTPEvent(Model):
    version: str
    route_key: str
    raw_path: str
    raw_query_string: str
    cookies: Optional[List[str]]
    headers: Dict[str, str]
    is_base_64_encoded: bool
    request_context: RequestContext
    path_parameters: Optional[Dict[str, str]]
    query_string_parameters: Optional[Dict[str, str]]  # For GET requests
    body: Optional[str]  # For POST requests


class APIGatewayV2HTTPResponse(Model):
    status_code: int
    headers: Dict[str, str]
    is_base_64_encoded: bool
    body: str
