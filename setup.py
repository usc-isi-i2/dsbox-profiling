from setuptools import setup

setup(name='dsbox-datapreprocessing',
      version='0.1.1',
      url='https://github.com/usc-isi-i2/dsbox-cleaning.git',
      maintainer_email='kyao@isi.edu',
      maintainer='Ke-Thia Yao',
      description='DSBox data preprocssing tools',
      license='MIT',
      packages=['dsbox', 'dsbox.datapreprocessing', 'dsbox.datapreprocessing.profiler'],
      zip_safe=False,
      install_requires=['pandas', 'langdetect']
      )
