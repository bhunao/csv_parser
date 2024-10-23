from fastapi import APIRouter, Request
from jinja2_fragments.fastapi import Jinja2Blocks

from src.functions import validate_csv_file

router_files = APIRouter()
templates = Jinja2Blocks("templates")


@router_files.get("/")
async def read_all_files(r: Request):
    print(validate_csv_file)
    return templates.TemplateResponse(name="base.html", context=dict(request=r))


@router_files.post("/")
async def upload_file(r: Request):
    return templates.TemplateResponse(name="base.html", context=dict(request=r))
