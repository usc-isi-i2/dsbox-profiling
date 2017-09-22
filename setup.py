from setuptools import setup

setup(name='dsbox-datapreprocessing',
      version='0.1.5',
      url='https://github.com/usc-isi-i2/dsbox-cleaning.git',
      maintainer_email='kyao@isi.edu',
      maintainer='Ke-Thia Yao',
      description='DSBox data preprocssing tools',
      license='MIT',
      packages=['dsbox', 'dsbox.datapreprocessing', 'dsbox.datapreprocessing.profiler'],
      zip_safe=False,
      python_requires='>=2.7',
      install_requires=[
          'numpy>=1.11.1', 'pandas>=0.20.1', 'langdetect>=1.0.7', 'future>=0.16'
      ]
)
