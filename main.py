
"""Main entry point for the AI Music Board application."""
from Models.exceptions import MusicBoardApplicationError
from music_board_application import MusicBoardApplication
import logging
import sys


def main():
    """Main entry point."""
    logger = logging.getLogger(__name__)
    app = None
    try:
        app = MusicBoardApplication()
        app.initialize()
        app.run()
    except MusicBoardApplicationError as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if app:
            app.cleanup()




if __name__ == "__main__":
    main()