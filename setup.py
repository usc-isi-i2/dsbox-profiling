from setuptools import setup

setup(name='dsbox-dataprofiling',
      version='0.2.2',
      url='https://github.com/usc-isi-i2/dsbox-cleaning.git',
      maintainer_email='kyao@isi.edu',
      maintainer='Ke-Thia Yao',
      description='DSBox data profiling  tools',
      license='MIT',
      packages=['dsbox', 'dsbox.datapreprocessing', 'dsbox.datapreprocessing.profiler'],
      zip_safe=False,
      python_requires='>=3.5',
      install_requires=[
          'numpy>=1.11.1', 'pandas>=0.20.1', 'langdetect>=1.0.7'
      ],
      entry_points = {
          'd3m.primitives': [
              'dsbox.Profiler = dsbox.datapreprocessing.profiler:Profiler',
          ],
      },

)
