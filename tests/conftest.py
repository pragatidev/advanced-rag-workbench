"""Keep the suite offline. Live generate is a CLI demo, not CI."""

import os

os.environ["RAGBENCH_GENERATE"] = "extractive"
