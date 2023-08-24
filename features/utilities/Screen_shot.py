import os
import time


class Screenshot:
    def capture_screenshot(self, d, path, name=None):
        timestamp = time.strftime("%d%m%Y_%H%M%S")
        filename = name + "_" + timestamp.replace(":", "_") + ".png"
        file = os.path.join(path, filename)
        d.save_screenshot(file)
        if not os.path.exists("reports/Screenshots"):
            os.makedirs("reports/Screenshots")
