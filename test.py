import subprocess
import sys
import os

messages = {
    "1": "/home/vandavv/dev/glm_meme_maker/message_1.txt",
    "2": "/home/vandavv/dev/glm_meme_maker/message_2.txt",
    "3": "/home/vandavv/dev/glm_meme_maker/message_3.txt",
    "4": "/home/vandavv/dev/glm_meme_maker/message_4.txt",
}

script_directory = os.path.dirname(os.path.realpath(__file__))
for message in messages.values():
    output = subprocess.check_output([sys.executable, "task.py", message, '140,70,"JS"', '130,180,"Python"'], cwd=script_directory, env=os.environ.copy())
    print(output)
