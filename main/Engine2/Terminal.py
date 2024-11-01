import os
import argparse
import sys
from time import sleep
from datetime import datetime
from .Settings2 import *


class Terminal:
    def __init__(self, lock):
        self.lock = lock
        self.msg_welcome()
        self.run = True
        self.render_loop = False
        self.parser = argparse.ArgumentParser()

        subparsers = self.parser.add_subparsers(dest="command")
        uni_parser = subparsers.add_parser("uni", help="Main command for engine controls.")
        uni_subparsers = uni_parser.add_subparsers(dest="subcommand")

        uni_controls_parser = uni_subparsers.add_parser("controls", help="Show render loop controls.")
        uni_won_parser = uni_subparsers.add_parser("won", help="Show wall of names.")

        subparsers.add_parser("clear", help="Clear the screen.")
        subparsers.add_parser("exit", help="exit the engine")

    def listener(self):
        while self.run:
            command = input(f"\nOpenUniverse{VERSION}\n$ ").strip().lower()
            self.handler(command)
        return None

    def handler(self, command):
        command_parts = command.split()
        try:
            args = self.parser.parse_args(command_parts)
            if args.command == "clear":
                self.act_clear(self.lock)
            elif args.command == "exit":
                self.act_exit()
            elif args.command == "uni":
                if args.subcommand == "controls":
                    self.msg_controls()
                elif args.subcommand == "won":
                    self.msg_won()
            else:
                print(f"Command '{command}' not found!\nUse -h or --help to see available options.")
        except SystemExit:
            if command not in ["-h", "--help"]:
                sleep(0.01)  # Avoiding jumbled thread output
                print(f"Command '{command}' not found!\nUse -h or --help to see available options.")
        except Exception as e:
            print(f"Error processing command: {e}")

    @staticmethod
    def output(lock, string):
        with lock:
            print(string)

    @staticmethod
    def msg_welcome():
        print("---------------------------------------------------------------------")
        print(BANNER)
        print("Project repo: https://github.com/MatinAfzal/OpenUniverse")
        if ESP:
            print("Starting Engine...")
        else:
            print("ESP (ENGINE_STATUS_PRINT) IS OFF!")

        start = datetime.now()
        print("Starting at:" + str(start.now()))

        if ESP:
            print("---Begin of ENGINE_STATUS_PRINT (ESP) logs---")

    @staticmethod
    def msg_controls():
        print("""
        OpenUniverse Control Guide:
            movement: w - a - s - d
            yaw & pitch: mouse
            world main axes: x  (0.3 second interrupt)
            face culling: c     (0.3 second interrupt)
            view mode: v        (GL_POINTS, GL_LINES, GL_TRIANGLES) (0.3 second interrupt)
            camera info: z      (1 second interrupt)
            light control: l    (Pause, Grab, PLace, Continue) (0.3 second interrupt)
            memory info: m      (1 second interrupt)
            live debugger: F3   (UNAVAILABLE V1.2.3-beta)
            builder mode: b     (0.3 second interrupt)
                - Change block: MouseRightClick
                - Place Block: MouseLeftClick
                - Distance: MouseScroll
        """)

    @staticmethod
    def msg_won():
        for name in WON:
            print(name)

    @staticmethod
    def act_clear(lock):
        with lock:
            os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def act_exit():
        sys.exit()
