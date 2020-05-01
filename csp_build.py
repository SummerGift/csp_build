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

    # cmd_pre = r'/rt-thread/eclipse/eclipse -nosplash --launcher.suppressErrors -application org.eclipse.cdt.managedbuilder.core.headlessbuild -data "/rt-thread/eclipse/workspace"'
    # cmd = cmd_pre + ' -import "file:/rt-thread/hello_test"'
    # print(cmd)
    # os.system(cmd)
    #
    # flag = False

    # cmd = cmd_pre + ' -cleanBuild "hello_test"'

    f = os.popen("hello_test/build.sh")
    for line in f.readlines():
        if line.find("Finished building"):
            print(line)
            flag = True

    print("flag = {0}".format(flag))


if __name__ == '__main__':
    main()
