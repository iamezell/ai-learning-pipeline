import asyncio
import shutil
import sys

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


def npx_command() -> str:
    # On Windows, CreateProcess can't run .cmd shims without the extension.
    if sys.platform == "win32":
        return shutil.which("npx.cmd") or shutil.which("npx") or "npx.cmd"
    return shutil.which("npx") or "npx"


async def main() -> None:
    server_params = StdioServerParameters(
        command=npx_command(),
        args=["-y", "@plaud-ai/mcp@latest"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.list_tools()

            print("PLAUD MCP Tools:")
            for tool in result.tools:
                print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())
