import audiogen
import itertools
import sys
import skimage.io
import skimage.filters
import skimage.color
import matplotlib.pyplot as plt

def get_signal_from_img(fname='ekg-m.png'):
  img = skimage.io.imread(fname)
  img = skimage.color.rgb2gray(img)
  edges = skimage.filters.sobel(img)
  plt.imshow(img)
  plt.show()
  print img


def main():
  get_signal_from_img()
  #audiogen.sampler.write_wav(sys.stdout, audiogen.tone(440))

if __name__ == '__main__':
    main()
