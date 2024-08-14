import pandas as pd
import pandas.errors
from Engine2.Settings2 import *
from Engine2.Utils import *
from time import time
from datetime import date


class TestSite:
    """
    format: format_version-chunk_num_x-chunk_num_z-obj_num_x-obj_num_z-chunk_type-object_type-lighting_method-test_time
    details:
        - chunk_type -> [P: Plain, D: Desert, S: Snow, F: Flat]
        - object_type -> [T: Tree, C: Cactus, N: Nothing]
        - lighting_method -> [D: Dynamic Lighting]

    #
    test_sample:
        - V1-S -> 1: 1-10-10-10-10-P-T-D-60 -> Simple world test
        - V1-I -> 2: 1-80-80-0-0-F-N-D-60 -> Image test
        - C    -> -1: Custom

    test_method:
        - manual: you control!
        - soft: stand still / locked FPS
        - normal: move around / locked FPS
        - hard: move around / open FPS
        - aggressive: move around / look around / open FPS / fast
    """

    def __init__(self, action="view", test_sample="Custom", test_method="manual"):

        self.known_actions = ["test", "view"]
        self.known_settings = ["V1-S", "V1-I", "Custom"]
        self.test_sample = test_sample
        self.test_method = test_method
        self.ready_time = None
        self.test_time = 20
        self.test = False
        self.start_time = None

        self.cpu_before = None
        self.cpu_after = None
        self.gpu_before = None
        self.gpu_after = None

        self.fps_min = None
        self.fps_ave = None
        self.fps_max = None

        self.comment = TEST_SITE_COMMENT

        self.info_call_attempts = 1
        self.esp_threshold = False  # avoiding esp spam

        if action not in self.known_actions:
            if ESP:
                print("action not found!")
        elif action == "test":
            self.test = True
            self.before = cpu_info()
            if test_sample == "1":
                self.test_time = 60
            else:
                self.test_time = 60

    def ready(self):
        """
        Before run when everything is ready.
        """
        self.ready_time = int(time())
        self.cpu_before = cpu_info()
        self.gpu_before = gpu_info()

    def inside(self):
        """
        inside the loop
        """
        if self.info_call_attempts == 1:
            if not self.check_test():
                self.cpu_after = cpu_info()
                self.gpu_after = gpu_info()
                self.info_call_attempts += 1
        else:
            pass

    def fps_test(self, fps_list):
        self.fps_min, self.fps_ave, self.fps_max = fps_info(fps_list)

    def check_test(self):
        now = int(time())
        diff = abs(self.ready_time - now)
        if diff == self.test_time:
            if ESP:
                print(f"TestSite: sample {self.test_sample} ended!")
                return 0
            return 0
        return 1  # continue the test

    def after(self):
        """
        Calculate everything after the test.
        """
        cpu_usage_before = 0
        cpu_usage_after = 0

        for i in self.cpu_before[0]:
            cpu_usage_before += i[1]
        for j in  self.cpu_after[0]:
            cpu_usage_after += j[1]

        memory_usage = memory_info()

        # node_name, cpu_name, gpu_name, cpu_cores, gpu_memory, gpu_temp, system, version, machine.
        # machine not saving for security reasons!
        test_result = {"time": [str(date.today())],
                       "test_sample": [self.test_sample],
                       "test_method": [self.test_method],
                       "test_runtime": [self.test_time],
                       "node_name": [self.cpu_before[9]],
                       "cpu_name": [self.cpu_before[1][0:7]],  # less information = more security
                       "gpu_name": [self.gpu_before[1]],
                       "cpu_cores": [self.cpu_before[2]],
                       "gpu_memory": [self.gpu_before[2]],
                       "gpu_temp": [self.gpu_before[3]],
                       "system": [self.cpu_before[4]],
                       "version": [self.cpu_before[5]],
                       "cpu_usage_before": [cpu_usage_before],
                       "cpu_usage_after": [cpu_usage_after],
                       "memory_info": [memory_usage],
                       "gpu_usage": [self.gpu_after[4]],
                       "fps_min": [self.fps_min],
                       "fps_ave": [self.fps_ave],
                       "fps_max": [self.fps_max],
                       "comment": [self.comment]}

        data = pd.DataFrame(test_result)
        dpath = r"Test\TestSiteReport.csv"

        try:
            existing_data = pd.read_csv(dpath)
        except pandas.errors.EmptyDataError as Error:
            if ESP:
                print("ERROR: TestSite report file is fresh!")
                print("initial TestSite report file...")
            data.to_csv(dpath, index=False)
        except:
            if ESP:
                print("ERROR: There is a error in reading TestSite report file!")
        else:
            existing_data = existing_data._append(data)
            existing_data.to_csv(dpath, index=False)
            if ESP:
                print("TestSite report saved!")
