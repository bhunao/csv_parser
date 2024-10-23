# from io import StringIO
#
# import pandas as pd
# from fastapi import HTTPException, UploadFile, status
# from pandas.errors import ParserError
#
# d_types = str | int | float
#
#
# async def validate_csv_file(file: UploadFile) -> tuple[bytes, list[dict[str, d_types]]]:
#     assert file
#     byte_content = await file.read()
#     try:
#         str_content = str(byte_content, "utf-8")
#         content = StringIO(str_content)
#         csv = pd.read_csv(content)
#     except UnicodeDecodeError:
#         raise HTTPException(
#             status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="Invalid file type, file must be `CSV`.",
#         )
#     except ParserError:
#         raise HTTPException(
#             status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="Invalid CSV file, could not process the content.",
#         )
#     records: list[dict[str, d_types]] = csv.to_dict("records")
#     return byte_content, records
