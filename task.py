import argparse
from pathlib import Path

import cv2
import base64
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("template", type=Path, help="Path to meme template as a PNG Base64 string")
parser.add_argument("texts", nargs="+")
args = parser.parse_args()

with open(args.template) as f:
    encoded_data = f.read().split(',')[1]
nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
for raw_text in args.texts:
    x,y,text = raw_text.split(',')
    cv2.putText(image, text, (int(x), int(y)), cv2.FONT_HERSHEY_TRIPLEX, 1, 0, 2, cv2.LINE_AA)
retval, buffer = cv2.imencode('.png', image)
image_as_text = base64.b64encode(buffer)
print("RESULT: ", image_as_text.decode())

