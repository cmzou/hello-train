import state_machine
import image_cycler

import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] - %(levelname)s - %(name)s:%(message)s",
    )

    try:
        state_machine.main()
    except Exception as e:
        logger.error("Error detected:", e)
        image_cycler.displays["error"].display_current_image(state_machine.inky_display)
