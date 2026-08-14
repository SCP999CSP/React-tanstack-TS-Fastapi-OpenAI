from loguru import logger
from rich.live import Live
import time

logger.info("任务开始")

with Live("", refresh_per_second=10) as live:
    for i in range(101):
        live.update(f"Processing: {i}%")
        time.sleep(0.05)

logger.success("任务完成")