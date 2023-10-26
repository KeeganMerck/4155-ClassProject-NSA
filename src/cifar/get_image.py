import pickle
import numpy as np

fn = "./src/cifar/data/5000_images.txt"  
img_data = np.loadtxt(fn, delimiter=",", usecols=range(0,3073), dtype=np.int64)

#Only used once to write to file. Not needed otherwise
def write_img_and_label():
  file = "./src/cifar/cifar-10-batches-py/data_batch_1"
  with open(file, 'rb') as fin:
    dict = pickle.load(fin, encoding='bytes')

  labels = dict[b'labels']  # 10,000 labels
  pixels = dict[b'data']    # 3,072 pixels (1024 per channel)

  n_images = 5000
  fn = "./src/cifar/data/5000_images.txt"

  fout = open(fn, 'w', encoding='utf-8')
  for i in range (n_images):      # n images
    for j in range(3072):  # pixels
      val = pixels[i][j]
      fout.write(str(val) + ",")
    fout.write(str(labels[i]) + "\n")
  fout.close()

def single_image(img_num):
  pxls_R = img_data[img_num][0:1024].reshape(32,32)  # not last val
  pxls_G = img_data[img_num][1024:2048].reshape(32,32)
  pxls_B = img_data[img_num][2048:3072].reshape(32,32)
  image = np.dstack((pxls_R, pxls_G, pxls_B))  # depth-stack

  label_num = img_data[img_num][3072:]

  return image, label_num