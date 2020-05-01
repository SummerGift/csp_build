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


def main():
    print("Hello python is running...")
    execute_command("scons --version")
    execute_command("pytest --version")

    os.chdir("/rt-thread")
    execute_command("git clone https://gitee.com/SummerGift/hello_test.git")
    execute_command("chmod a+x hello_test/build.sh")
    execute_command("hello_test/build.sh")


if __name__ == '__main__':
    main()
