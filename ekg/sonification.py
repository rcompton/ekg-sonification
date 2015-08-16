import audiogen
import itertools
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import skimage.io
import wave
import contextlib
import subprocess

def beep(frequency=440, seconds=0.25):
  for sample in audiogen.util.crop_with_fades(audiogen.generators.tone(frequency), seconds=seconds):
    yield sample

def sonification_generator(fname='ekg.tsv'):
  df = pd.read_csv(fname,sep='\t')
  out = []
  df['freq'] = (df['ekg'] - df['ekg'].min()) + 1
  df['freq'] = df['freq']*100
  #print max(df['freq']), min(df['freq'])
  for idx, row in df.iterrows():
    #print idx, row['ekg'], row['sec']
    freq = row['freq']
    #print freq
    out.append(beep(frequency=freq, seconds=0.03))
  return out

def get_wav_len(fname):
  with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    return duration

def make_animation(audio, finname='ekg-m.png', foutname='nosound.mp4'):
  duration = get_wav_len(audio)
  print duration
  img = skimage.io.imread(finname)
  print img.shape

  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_aspect('equal')
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)

  im = ax.imshow(img, cmap='gray', interpolation='nearest')
  plt.tight_layout()
  def update_img(n):
    tmp = np.zeros_like(img)
    tmp[:,n] = 10
    im.set_data(tmp+img)
    return im

  #legend(loc=0)
  FFMpegWriter = animation.writers['avconv_file']
  metadata = dict(title='Movie Test', artist='Matplotlib', comment='Movie support!')
  writer = FFMpegWriter(fps=15, metadata=metadata)
  with writer.saving(fig, foutname, 100):
    for i in range(int(writer.fps*duration)):
      percent_done = i/(writer.fps*duration)
      vbar = percent_done*img.shape[1]
      print vbar
      update_img(int(vbar))
      writer.grab_frame()

  #add audio to video
  cmdl = ['avconv', '-i', foutname, '-i', audio, '-c', 'copy', '-shortest', 'audio_'+foutname]
  subprocess.check_call(cmdl)
  return

def main():

  sound_file = 'ekg-sounds.wav'
  gen = sonification_generator()
  with open(sound_file, 'wb') as fout:
      audiogen.sampler.write_wav(fout, itertools.chain.from_iterable(gen))

  #audiogen.sampler.write_wav(sys.stdout, itertools.chain.from_iterable(gen))
  make_animation(audio=sound_file)



if __name__ == '__main__':
    main()
