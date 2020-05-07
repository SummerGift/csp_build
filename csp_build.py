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


def get_test_result(content):
    if content.find("Finished building") != -1:
        return True
    else:
        return False


def update_glibc():
    execute_command("wget http://ftp.gnu.org/gnu/glibc/glibc-2.25.tar.gz")
    execute_command("wget http://ftp.gnu.org/gnu/glibc/glibc-linuxthreads-2.3.2.tar.gz")
    execute_command("tar -zxvf glibc-2.25.tar.gz")
    execute_command("cd glibc-2.25")
    execute_command("tar -zxvf ../glibc-linuxthreads-2.3.2.tar.gz")
    execute_command("cd ..")
    execute_command("./glibc-2.25/configure --prefix=/usr --disable-profile "
                    "--enable-add-ons --libexecdir=/usr/lib --with-headers=/usr/include")
    # execute_command("cd glibc-2.25")
    execute_command("make")
    execute_command("make install")


def main():
    print("Hello python is running...")
    execute_command("scons --version")
    execute_command("pytest --version")

    os.chdir("/rt-thread")

    update_glibc()
    os.chdir("/rt-thread")

    execute_command("git clone https://gitee.com/SummerGift/hello_test.git")

    cmd_pre = r'/rt-thread/eclipse/eclipse -nosplash --launcher.suppressErrors -application ' \
              r'org.eclipse.cdt.managedbuilder.core.headlessbuild -data "/rt-thread/eclipse/workspace" '
    cmd = cmd_pre + ' -import "file:/rt-thread/hello_test"'
    execute_command(cmd)
    cmd = cmd_pre + ' -cleanBuild "hello_test"'
    result = execute_command(cmd)

    if get_test_result(result):
        print("================>Project test success.")
    else:
        print("================>Project test fails.")


if __name__ == '__main__':
    main()
