import os
import shutil

origin = "/mnt/c/Users/hajun/Project/image_1/dataset"
base = "/mnt/c/Users/hajun/Project/image_1/splitted"
clss_list = os.listdir(origin)
os.mkdir(base)

train_dir = os.path.join(base, "train")
val_dir = os.path.join(base, "val")
test_dir = os.path.join(base, "test")

os.mkdir(train_dir)
os.mkdir(val_dir)
os.mkdir(test_dir)

for clss in clss_list:
  os.mkdir(os.path.join(train_dir, clss))
  os.mkdir(os.path.join(val_dir, clss))
  os.mkdir(os.path.join(test_dir, clss))