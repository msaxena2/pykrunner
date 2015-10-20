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
        if os.path.exists(output_file_path) or os.path.exists(result_file_path):
            return ("res", "res")
        if os.path.exists(result_file_path):
            return ("res", "res")
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
        result_file = open(result_file_path, 'w')
        result_file.write("timed-out")
        result_file.close()
        return ("timeout", timeout.message)
    except Exception as normalExp:
        result_file = open(result_file_path, 'w')
        result_file.write(result[1])
        result_file.close()
        return ("exception", "Exception")


def execute(command, error_mode=subprocess.STDOUT):
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
        if not os.path.exists(activity.output_folder_path):
            os.mkdir(activity.output_folder_path)
        output_file_path = os.path.join(activity.output_folder_path,
                                        src_file.split(".")[0] + activity.output_file_extension)
        if not os.path.exists(activity.result_folder_path):
            os.mkdir(activity.result_folder_path)
        result_file_path = os.path.join(activity.result_folder_path,
                                        src_file.split(".")[0] + activity.result_file_extension)
        map_list.append((src_file_path, output_file_path, result_file_path, 1000))
        # wrapper is needed as pickling fails with pool. Alternative solution to be looked into later
    return pool.map(execute_test_wrapper, map_list)


def main():
    activity_list = pykrunner_parser.parse(os.path.abspath(sys.argv[1]))
    for activity in activity_list:
        thread_handler(activity)


if __name__ == '__main__':
    main()

