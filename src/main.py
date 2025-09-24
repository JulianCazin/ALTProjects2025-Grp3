import sys
import logging
import os

from classes.game import Game

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def main():
    """Fonction principale de l'application."""
    logger.info("Démarrage du programme...")
    
    Game().run()
    logger.info("Game started.")

    
    logger.info("Fin du programme.")




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Une erreur est survenue: %s", e)
        sys.exit(1)
