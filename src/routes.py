from io import StringIO

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from pandas.errors import ParserError
from sqlmodel import Session
from jinja2_fragments.fastapi import Jinja2Blocks

from src.core import get_session

router_files = APIRouter()
templates = Jinja2Blocks("templates")

DepSession: Session = Depends(get_session)


d_types = str | int | float


async def validate_csv_file(file: UploadFile) -> tuple[bytes, list[dict[str, d_types]]]:
    assert file
    byte_content = await file.read()
    try:
        str_content = str(byte_content, "utf-8")
        content = StringIO(str_content)
        csv = pd.read_csv(content)
    except UnicodeDecodeError:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid file type, file must be `CSV`.",
        )
    except ParserError:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid CSV file, could not process the content.",
        )
    records: list[dict[str, d_types]] = csv.to_dict("records")
    return byte_content, records


@router_files.get("/")
async def read_all_files(r: Request):
    return templates.TemplateResponse(name="base.html", context=dict(request=r))


@router_files.post("/")
async def upload_file(r: Request):
    return templates.TemplateResponse(name="base.html", context=dict(request=r))
