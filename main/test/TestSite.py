import numpy as np
import pandas as pd
from Engine2.Settings2 import *


class TestSite:
    """
    format: format_version-chunk_num_x-chunk_num_z-obj_num_x-obj_num_z-chunk_type-object_type-lighting_method
    details:
        - chunk_type -> [P: Plain, D: Desert, S: Snow]
        - object_type -> [T: Tree, C: Cactus]
        - lighting_method -> [D: Dynamic Lighting]

    #
    test_sample:
        - V1-S -> 1: 1-10-10-10-10-P-T-D

    test_method:
        - soft: stand still / locked FPS
        - normal: move around / locked FPS
        - hard: move around / open FPS
        - aggressive: move around / look around / open FPS / fast
    """

    def __init__(self, action="view", test_sample="1", test_method="soft"):

        self.known_actions = ["test", "view"]
        self.known_settings = ["V1-S, "]

        if action not in self.known_actions:
            if ESP:
                print("action not found!")
        elif action == "test":
            pass
