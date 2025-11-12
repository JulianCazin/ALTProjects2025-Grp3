import sys
import logging
import os

from classes.game import Game

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def main():
    """Main function of the program"""
    logger.info("Program starting...")

    Game().run()
    logger.info("Game started.")

    logger.info("End of the program.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("An error occured: %s", e)
        sys.exit(1)
