import numpy as np
import pandas as pd
from main.Engine2.Settings2 import *

class TestSite:
    def __init__(self, action="view"):
        self.known_actions = ["view", "import"]

        if action not in self.known_actions:
            if ESP:
                print()

