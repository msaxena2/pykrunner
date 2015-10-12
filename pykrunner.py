__author__ = 'manasvi'
import os
import subprocess
import sys
from multiprocessing import Pool
import signal
import pykrunner_parser


class TimeOutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeOutException("timeout occured")


def execute_test(src_file_path, output_file_path, result_file_path, timeout):
    command = ["kcc", src_file_path, "-o", output_file_path]
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        result = execute(command)
        if (result[0] != "stderr"):
            command = [output_file_path]
            result = execute(command, error_mode=subprocess.STDOUT)
            result_file = open(result_file_path, 'w')
            result_file.write(result[1])
            result_file.close()
            return result
        return result
    except TimeOutException as timeout:
        return ("timeout", timeout.message)


def execute(command, error_mode=None):
    try:
        print("pykrunner runninng \"" + " ".join(map(str, command)) + "\"")
        # Capture the Error in STDOUT
        if error_mode == None:
            result = subprocess.check_output(command)
        else:
            result = subprocess.check_output(command, stderr=error_mode)
        return ("stdout", result)
    except subprocess.CalledProcessError as stderr:
        return ("stderr", stderr.output)


# wrapper function may be needed if lambda fails in pool call
def execute_test_wrapper(tuple_a):
    return execute_test(tuple_a[0], tuple_a[1], tuple_a[2], tuple_a[3])


def thread_handler(activity):
    pool = Pool(processes=activity.thread_count)
    map_list = []
    for src_file in filter(lambda x: x.endswith(activity.src_file_extension), os.listdir(activity.test_folder_path)):
        src_file_path = os.path.join(activity.test_folder_path, src_file)
        output_file_path = os.path.join(activity.output_folder_path, src_file.split(".")[0] + activity.output_file_extension)
        result_file_path = os.path.join(activity.result_folder_path, src_file.split(".")[0] + activity.result_file_extension)
        map_list.append((src_file_path, output_file_path, result_file_path, 20))
        # wrapper is needed as pickling fails with pool. Alternative solution to be looked into later
    return pool.map(execute_test_wrapper, map_list)


def activiy_handler(activity):
    thread_handler(activity.test_folder_path, activity.src_file_extension, )


# def thread_handler(test_folder, output_path, src_file_extension, thread_count):
# non_termination_list = []
# for src_file in os.listdir(test_folder):
# active_thread_list = []
# if src_file.endswith(src_file_extension):
# if (thread_count > 0):
# src_file_path = os.path.join(test_folder, src_file)
# output_file_path = os.path.join(output_path, src_file.split(".")[0] + ".out")
# result_file_path = os.path.join(output_path, src_file.split(".")[0] + ".pyk")
# active_thread_list.append(
# threading.Thread(name=src_file,
# target=execute_test(src_file_path, output_file_path, result_file_path)))
# else:
# non_termination_list.extend(run_and_wait(active_thread_list))
#                 thread_count += len(active_thread_list)
#                 active_thread_list = []
#     if len(active_thread_list) > 0:
#         non_termination_list.extend(run_and_wait(active_thread_list))
#     return non_termination_list
#


# def process_test_folder(executable_path, test_folders, output_path, src_file_ext, result_file_ext):
#     success_map = {}
#     for test_folder_path in test_folders:
#         for src_file in os.listdir(test_folder_path):
#             if src_file.endswith(src_file_ext):
#                 print "Testing " + src_file
#                 src_file_path = os.path.join(test_folder_path, src_file)
#                 src_file_name = src_file.split(".")[0]
#                 output_executable = os.path.join(output_path, (src_file_name + ".out"))
#                 output_pykrun = os.path.join(output_path, (src_file_name + ".pyk"))
#                 kcc_result = execute((executable_path + " " + src_file_path + " -o " + output_executable))
#                 if kcc_result[0] == "SUCCESS":
#                     try:
#                         result = execute(output_executable)
#                         output_pykrun_file = open(output_pykrun, mode='w')
#                         output_pykrun_file.write(result[1])
#                         ref_file_ext = os.path.join(test_folder_path, (src_file_name + result_file_ext))
#                         if (os.path.exists(ref_file_ext)):
#                             if filecmp.cmp(output_pykrun_file, open(ref_file_ext)):
#                                 success_map[src_file] = "Success"
#                             else:
#                                 success_map[src_file] = "Files didn't match"
#                         else:
#                             success_map[src_file] = "Reference File Absent"
#                     except Exception, msg:
#                         if msg == "time out":
#                             success_map[src_file] = "Time Out"
#
#     return success_map


# def parse_config_file(config_file):

# def main():
#     state = "default"
#     test_folders = []
#     file_extension = ""
#     output_folder = ""
#     result_file_ext = ""
#
#     for line in open(os.path.abspath(sys.argv[1])):
#         line = line.rstrip()
#
#         if line == "test-folders:":
#             state = "test-folders"
#             continue
#         if line == "file-extension:":
#             state = "file-extension"
#             continue
#         if line == "output-folder:":
#             state = "output-folder"
#             continue
#         if line == "result-file-ext:":
#             state == "result_ext"
#             continue
#         if line == "":
#             state == "default"
#             continue
#
#         if state == "test-folders":
#             test_folders.append(line)
#         elif state == "file-extension":
#             file_extension = line
#             state = "default"
#         elif state == "output-folder":
#             output_folder = line
#             state = "default"
#         elif state == "result_ext":
#             result_file_ext = line
#             state = "default"
#         else:
#             continue
#
#     # results = process_test_folder("kcc", test_folders, output_folder, file_extension, result_file_ext)
#     for test_folder in test_folders:
#         thread_handler(test_folder, output_folder, file_extension, 1)
#         # print str(thread_handler(test_folder, output_folder, file_extension, 3))

def main():
    activity_list = pykrunner_parser.parse(os.path.abspath(sys.argv[1]))

    print activity_list[0].test_folder_path


if __name__ == '__main__':
    main()

