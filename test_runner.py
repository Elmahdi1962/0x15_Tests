#!/bin/python3
import os, enum, re, sys
from subprocess import Popen, PIPE
import keyboard

class Check_Types(enum.Enum):
  Error = 1
  Success = 2

# The name of the shell program in your project's directory or folder
shell_file_name = "./simple_shell"
gen_env = os.environ
# The relative path from this file's directory to your project directory
project_dir = '../'
# The relative path from your project directory to the tests directory
# The tests directory should contain this file
tests_dir = '0x16_Tests'

def run_tests(test_cases):
  '''
  Runs tests for a list of test cases

  Parameters:
  test_cases (list): A list of
  '''
  tests_failed = 0
  tests_passed = 0
  os.chdir(project_dir)
  for i in range(len(test_cases)):
    p1 = Popen(['./0x16_Tests/put', test_cases[i][0]], stdout=PIPE)
    p2 = Popen([shell_file_name], stdin=p1.stdout, stdout=PIPE, env=gen_env)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]
    print(output.decode('ascii'), end='')

    # keyboard.write(shell_file_name)
    # keyboard.send('enter')
    # keyboard.write(test_cases[i][0])
    # keyboard.send('enter')
    # keyboard.write('exit')
    # keyboard.send('enter')
  os.chdir(tests_dir)

def run_key_presses():
  keyboard.write("key_press")

def betty_checks():
  '''
  Checks for Betty issues in all .c and .h files of the
  current working (project) directory.
  '''
  os.chdir(project_dir)
  files = get_files(os.curdir)
  all_checks_passed = True
  for i in range(len(files)):
    p1 = Popen(['./0x16_Tests/put', files[i]], stdout=PIPE)
    p2 = Popen(['betty', files[i]], stdin=p1.stdout, stdout=PIPE, env=gen_env)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = (p2.communicate()[0]).decode('ascii')
    output_lines = output.splitlines()
    file_descr = output_lines[1]
    file_descr_printed = False
    errors = 0
    warnings = 0
    for out_line in output_lines:
      if out_line.lower().count("ERROR: ".lower()) > 0:
        if not file_descr_printed:
          print(file_descr)
          file_descr_printed = True
        print(out_line)
        errors += 1
      elif out_line.lower().count("WARNING: ".lower()):
        if not file_descr_printed:
          print(file_descr)
          file_descr_printed = True
        print(out_line)
        warnings += 1
    if errors > 0 or warnings > 0:
      print("total: \033[31m{} errors\033[0m, \033[33m{} warnings\033[0m, {} lines checked\n".format(errors, warnings, len(output_lines)))
      all_checks_passed = False
  if all_checks_passed:
    print("\033[97;42m Congratulations: \033[0m All checks passed")
  os.chdir(tests_dir)

def get_files(folder):
  '''
  Retrieves the .c and .h files in a given folder

  Parameters:
  folder (str): The path to the folder

  Returns:
  A list of .c and .h files, otherwise an empty list
  '''
  files_lst = []
  if os.path.isdir(folder):
    for file in os.listdir(folder):
      if re.fullmatch("^.*\.(c|h)$", file):
        files_lst.append(file)
  return files_lst

def check_function_usage(func_name):
  '''
  Checks for the presence of a function in all project files

  Parameters:
  func_name (str): The name of the function
  '''
  os.chdir(project_dir)
  used_function = False
  for project_file in get_files(os.curdir):
    usage_count = 0
    i = 0
    file_name_printed = False
    res_path = os.path.join(os.getcwd(), project_file)
    if os.path.exists(res_path):
      with open(res_path, 'r') as project_file_io:
        lines = project_file_io.readlines()
        for line in lines:
          i += 1
          if line.find(func_name, 0, len(line) - 1) >= 0:
            usage_count += 1
            if not file_name_printed:
              print("{} {} {}".format("=" * 10, project_file, "=" * 10))
              file_name_printed = True
            print("\033[31m{}:{}: ERROR:\033[0m Do not use '{}'".format(project_file, i, func_name))
      if usage_count > 0:
        print("Total: \033[31m{} errors\033[0m, {} lines checked\n".format(usage_count, i))
        used_function = True

  if not used_function:
    print("\033[97;42m Congratulations: \033[0m All checks passed")
  os.chdir(tests_dir)
