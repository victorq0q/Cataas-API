import sys

sys.path.append("../")
from cataas import *


cat = cat(tag="gif", text="I love you", width=512, heigth=512)

download(cat)
