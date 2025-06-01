"""Labeeb: Main entry point."""

# labeeb/__main__.py
from .main import main

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
