import os
import time
import subprocess


def execute_command(cmd_string, cwd=None, shell=True):
    """Execute the system command at the specified address."""

    sub = subprocess.Popen(cmd_string, cwd=cwd, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, shell=shell, bufsize=4096)

    stdout_str = ''
    while sub.poll() is None:
        stdout_str += str(sub.stdout.read())
        time.sleep(0.1)

    return stdout_str


def get_test_result(result):
    if result.find("Finished building") != -1:
        return True
    else:
        return False


def main():
    print("Hello python is running...")
    execute_command("scons --version")
    execute_command("pytest --version")

    os.chdir("/rt-thread")
    execute_command("git clone https://gitee.com/SummerGift/hello_test.git")

    cmd_pre = r'/rt-thread/eclipse/eclipse -nosplash --launcher.suppressErrors -application ' \
              r'org.eclipse.cdt.managedbuilder.core.headlessbuild -data "/rt-thread/eclipse/workspace" '
    cmd = cmd_pre + ' -import "file:/rt-thread/hello_test"'
    result = execute_command(cmd)

    print("import result {0}".format(result))

    cmd = cmd_pre + ' -cleanBuild "hello_test"'
    result = execute_command(cmd)

    if get_test_result(result):
        print("================>Project test success.")
    else:
        print("================>Project test fails.")


if __name__ == '__main__':
    main()
