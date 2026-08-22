import asyncio
import json
import os
import shutil
import sys
from collections.abc import Awaitable, Callable
from typing import TypeVar

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

T = TypeVar("T")


def npx_command() -> str:
    # On Windows, CreateProcess can't run .cmd shims without the extension.
    if sys.platform == "win32":
        return shutil.which("npx.cmd") or shutil.which("npx") or "npx.cmd"
    return shutil.which("npx") or "npx"


def server_params() -> StdioServerParameters:
    home = os.path.expanduser("~")
    return StdioServerParameters(
        command=npx_command(),
        args=["-y", "@plaud-ai/mcp@latest"],
        env={
            "LOG_LEVEL": "silent",
            "HOME": home,
            "USERPROFILE": home,
        },
    )


def text_payload(result) -> str:
    if not result.content:
        return ""
    return result.content[0].text


def is_authenticated(result) -> bool:
    if result.is_error:
        return False
    text = text_payload(result).lower()
    return "not authenticated" not in text and bool(text)


def print_recordings(result) -> None:
    if result.is_error:
        print("list_files failed:")
        print(text_payload(result))
        return

    payload = json.loads(text_payload(result))
    recordings = payload.get("data", [])
    print(f"\nPLAUD recordings ({len(recordings)}):")
    for item in recordings:
        print(f"- {item.get('name')}  [{item.get('id')}]")


async def call_tool(session: ClientSession, name: str, arguments: dict | None = None, timeout: float = 45):
    return await asyncio.wait_for(
        session.call_tool(name, arguments=arguments or {}),
        timeout=timeout,
    )


async def with_session(work: Callable[[ClientSession], Awaitable[T]]) -> T:
    async with stdio_client(server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await work(session)


async def fetch_recordings(session: ClientSession) -> None:
    print("\nFetching recordings...", flush=True)
    files_result = await call_tool(
        session,
        "list_files",
        {"page": 1, "page_size": 20},
        timeout=60,
    )
    print_recordings(files_result)


async def attempt() -> None:
    async def phase_one(session: ClientSession) -> bool:
        tools = await session.list_tools()
        print("PLAUD MCP Tools:")
        for tool in tools.tools:
            print(f"- {tool.name}")

        print("\nChecking authentication...", flush=True)
        user = await call_tool(session, "get_current_user", timeout=45)

        if is_authenticated(user):
            print(f"Authenticated as: {text_payload(user)}", flush=True)
            await fetch_recordings(session)
            return False

        print(
            "Not authenticated. Starting login (complete it in the browser)...",
            flush=True,
        )
        login_result = await call_tool(session, "login", timeout=300)
        print(text_payload(login_result), flush=True)
        # Login can leave this stdio session wedged; caller reconnects.
        return True

    needs_reconnect = await with_session(phase_one)
    if needs_reconnect:
        print("Reconnecting after login...", flush=True)
        await with_session(fetch_recordings)


async def main() -> None:
    last_error: Exception | None = None
    for attempt_number in range(1, 4):
        try:
            await attempt()
            return
        except TimeoutError as exc:
            last_error = exc
            print(
                f"Timed out talking to Plaud MCP (attempt {attempt_number}/3). Retrying with a fresh process...",
                flush=True,
            )
        except Exception as exc:
            last_error = exc
            print(
                f"Plaud MCP error on attempt {attempt_number}/3: {exc}. Retrying...",
                flush=True,
            )
        await asyncio.sleep(1)

    raise RuntimeError("Failed to talk to Plaud MCP after 3 attempts") from last_error


if __name__ == "__main__":
    asyncio.run(main())
