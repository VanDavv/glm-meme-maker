import argparse
from pathlib import Path
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("template", type=Path, help="Path to meme template")
parser.add_argument("texts", nargs="+")
args = parser.parse_args()

image = cv2.imread(str(args.template))
for raw_text in args.texts:
    x,y,text = raw_text.split(',')
    cv2.putText(image, text, (int(x), int(y)), cv2.FONT_HERSHEY_TRIPLEX, 1, 0, 2, cv2.LINE_AA)
cv2.imwrite(f"/golem/output/result.png", image)

