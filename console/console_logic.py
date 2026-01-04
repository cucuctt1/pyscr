import subprocess

def console_func(target,command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,shell=True,
                                   universal_newlines=True)
        if command == "quit":
            process.kill()
        for line in iter(process.stdout.readline, ''):
            target.get(line)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")
        process.kill()
    finally:
        process.terminate()
        process.wait()