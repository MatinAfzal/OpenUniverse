# This file contains the functions required by the engine
import psutil
import GPUtil
import platform as pl
import numpy as np
from OpenGL.GL import *
from .Settings2 import *


def format_vertices(coordinates, triangles) -> np.ndarray:
    allTriangles = []
    for t in range(0, len(triangles), 3):
        allTriangles.append(coordinates[triangles[t]])
        allTriangles.append(coordinates[triangles[t+1]])
        allTriangles.append(coordinates[triangles[t+2]])
    return np.array(allTriangles, np.float32)


def compile_shader(shader_type, shader_source):
    """
    Shader compiler
    """
    if ESP:
        print("Compile Program...")
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    
    # Compile error viewer
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error_message = "\n" + error_message.decode("utf-8")
        raise Exception(error_message)
    
    return shader_id


def create_program(vertex_shader_code, fragment_shader_code):
    """
    Program handler (& Compile)
    """
    
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)
    
    # Error viewer
    if not link_success:
        info = glGetProgramInfoLog(program_id)
        raise RuntimeError(info)
    
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)

    if ESP:
        print("Program Created, program_id: ", str(program_id))
    return program_id


def save_report(fps_list, start_time, end_time, time_based=False):
    if ESP:
        print("Saving Report...")

    (cpu_usage, processor, total_cores, pysical_cores, system, release, version, machine, boot_time,
     node_name) = cpu_info()

    gpu_id, gpu_name, gpu_total_memory, gpu_temperature = gpu_info()

    fps_min, fps_ave, fps_max = fps_info(fps_list)
    
    report = f"""
    $ TIME $
    / START: {start_time} | END: {end_time}

    $ BUILD $
    / CPU: {processor} | GPU: {gpu_name} | SYS: {system} | VER: {version} | REL: {release}
    
    $ FPS $
    / MIN: {fps_min} | MAX: {fps_max} | AVE: {fps_ave}
    
    $ CPU $
    / CPU: {processor} | TOTAL CORES: {total_cores} | PHYSICAL CORES: {pysical_cores}
    / INDEX - PERCENT
    /USAGE: {cpu_usage}
    
    $ GPU $
    / GPU: {gpu_name} | ID: {gpu_id} | TOTAL MEMORY: {gpu_total_memory} | TEMP: {gpu_temperature}
    
    $ SYSTEM $
    / NODE: {node_name} | MACHINE: {machine} | BOOT: {boot_time}
    """

    # if time_based:
    #     # Time based Report saving
    #
    #     try:
    #         dt_string = start_time.strftime("%d.%m.%Y--%H.%M.%S")
    #         with open(f"report\\{dt_string}.txt", "w") as report_file:
    #             report_file.write(report)
    #             report_file.close()
    #     except Error as Exception:
    #         return 0, type(Error).__name__
    #     else:
    #         return 1, None
    #
    # else:
    #     try:
    #         with open(r"report\engine_report.txt", "w") as report_file:
    #             report_file.write(report)
    #             report_file.close()
    #     except Error as Exception:
    #         return 0, type(Error).__name__
    #     else:
    #         return 1, None
    return 1


def cpu_info() -> list:
    uname = pl.uname()
    system = uname.system
    node_name = uname.node
    release = uname.release
    version = uname.version
    machine = uname.machine
    processor = uname.processor
    boot_time = psutil.boot_time()
    pysical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)

    c_use = []
    for i, percentage in enumerate(psutil.cpu_percent(interval=1.0, percpu=True)):
        c_use.append((i, percentage))

    return [c_use, processor, total_cores, pysical_cores, system, release, version, machine, boot_time, node_name]


def gpu_info() -> list:
    gpus = GPUtil.getGPUs()
    gpu_id = None
    gpu_name = None
    gpu_total_memory = None
    gpu_temperature = None
    gpu_memory_usage = None
    for gpu in gpus:
        gpu_id = gpu.id
        gpu_name = gpu.name
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_memory_usage = gpu.memoryUsed
    return [gpu_id, gpu_name, gpu_total_memory, gpu_temperature, gpu_memory_usage]


def fps_info(fps_list: list):
    fps_min = round(min(fps_list[30:-30]))  # skip 0 in the list
    fps_max = round(max(fps_list))
    fps_ave = round(sum(fps_list) / len(fps_list))
    return fps_min, fps_ave, fps_max


def memory_info() -> list:
    memory_usage = psutil.virtual_memory()
    return memory_usage
