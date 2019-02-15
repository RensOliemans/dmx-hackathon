import sys
from loguru import logger
from config import LOGLVL

logger.remove()
logger.add(sys.stdout, colorize=True, level=LOGLVL,
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
                  "| <level>{level:<8}</level> "
                  "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                  "<level>{message}</level>")
logger.add("logs/log{time}.log", colorize=True, backtrace=False, level="DEBUG", retention="10 days",
           format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
                  "| <level>{level:<8}</level> "
                  "| <cyan>{name}</cyan>:<cyan>{line}</cyan> - "
                  "<level>{message}</level>")
