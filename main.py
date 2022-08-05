import argparse
import os
from datetime import timedelta

os.environ["YAGNA_APPKEY"] = "55359a3e7afb4525be26fff47accc41f"
import asyncio
import logging
import pathlib
from typing import AsyncIterable

from aiohttp import ClientConnectorError
from yapapi import Golem, Task, WorkContext, NoPaymentAccountError
from yapapi.log import enable_default_logger
from yapapi.payload import vm

log = logging.getLogger(__name__)


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script_dir = pathlib.Path(__file__).resolve().parent
        script = context.new_script(timeout=timedelta(minutes=10))
        uploaded_template_path = f"/golem/input/{pathlib.Path(task.data['template']).name}"
        result_path = script_dir / "result.png"
        script.upload_file(task.data["template"], uploaded_template_path)
        script.upload_file(str(script_dir / "task.py"), "/golem/input/task.py")
        future_result = script.run("/usr/bin/python3", "/golem/input/task.py", uploaded_template_path, *task.data["texts"])
        script.download_file("/golem/output/result.png", str(result_path))
        yield script
        task.accept_result(result=await future_result)
        print(f"Result saved at {result_path.absolute()}")


async def main(args):
    package = await vm.repo(
        image_hash="3c9a6ebed84cc12613834140dc52ffe05b0f3169c675460343c68118",
    )

    tasks = [Task(data={"texts": args.texts, "template": str(args.template.absolute())})]

    try:
        async with Golem(budget=1.0, subnet_tag="devnet-beta") as golem:
            async for completed in golem.execute_tasks(worker, tasks, payload=package):
                pass
    except NoPaymentAccountError as ex:
        log.error(f"Sender is not initialized!\nPlease run \"yagna payment init --sender\" or consult the docs\nError: {ex}")
    except (ConnectionResetError, ClientConnectorError) as ex:
        log.error(f"Yagna client is not running!\nPlease run \"yagna service run\" or consult the docs\nError: {ex}")


if __name__ == "__main__":
    enable_default_logger(log_file="hello.log")
    parser = argparse.ArgumentParser()
    parser.add_argument("template", type=pathlib.Path, help="Path to meme template")
    parser.add_argument("texts", nargs="+", help="Specify text to be inserted (can be multiple, space-separated)\nExample:\n10,20,\"my text\" - will insert the \"my text\" message 10 px from top and 20px from left")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(args))
    loop.run_until_complete(task)