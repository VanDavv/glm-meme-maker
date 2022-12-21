FROM dkimg/opencv
WORKDIR /golem/work
ADD task.py .
ADD test_message.txt .
VOLUME /golem/input /golem/output
