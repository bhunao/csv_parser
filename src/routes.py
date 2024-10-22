from io import StringIO

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from pandas.errors import ParserError
from sqlmodel import Session
from jinja2_fragments.fastapi import Jinja2Blocks

from src.core import get_session
from src.models import (
    File,
)

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
async def read_all_files(r: Request, s: Session = DepSession):
    return templates.TemplateResponse(name="base.html", context=dict(request=r))


@router_files.post("/")
async def upload_file(file: UploadFile, s: Session = DepSession):
    file_content, _file_dict_record = await validate_csv_file(file)

    new_record = File(name=str(file.filename), content=file_content).create(s)
    return new_record
