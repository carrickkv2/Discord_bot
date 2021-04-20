import os
import typing
from ExtractTable import ExtractTable
from dotenv import load_dotenv
from os import getenv


def extract_to_csv(image_url: str, output_folder: typing.Union[str, bytes, os.PathLike]) -> bool:
    """
    Extracts data from an image and outputs it to csv.
    """
    load_dotenv()
    api = getenv("API")
    et_sess = ExtractTable(api_key=api)  # Replace your VALID API Key here
    # print(et_sess.check_usage())

    image_location = image_url
    # output_extract = str(et_sess.ServerResponse.json())
    # print(et_sess.ServerResponse.json())

    # Checks the API Key validity as well as shows associated plan usage
    et_sess.process_file(filepath=image_location, output_format="csv")

    return bool(et_sess.save_output(output_folder, output_format="csv"))


def usage_extract():
    load_dotenv()
    api = getenv("API")
    et_sess = ExtractTable(api_key=api)
    output_extract = str(et_sess.check_usage())
    output_extract += '\n'
    return output_extract
