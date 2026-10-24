import sys

sys.stdout.reconfigure(encoding="utf-8")

from rich.console import Console
from src.tools.tools import web_search, scrape_url

console = Console(legacy_windows=False)


r = web_search.invoke({"query": "What is the cybersecurity demand against AI in 2026?"})
console.print(r)
