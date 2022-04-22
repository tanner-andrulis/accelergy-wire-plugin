from setuptools import setup
import os
from os import path

def readme():
      with open('README.md') as f:
            return f.read()

setup(
      name='accelergy-wire-plug-in',
      version='0.1',
      description='An energy estimation plug-in for Accelergy framework for analog components',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
      ],
      keywords='accelerator hardware energy estimation analog adc',
      author='',
      author_email='',
      license='MIT',
      install_requires = [],
      python_requires = '>=3.8',
      data_files=[
                  ('share/accelergy/estimation_plug_ins/accelergy-wire-plugin', ['./accelergywrapper.py']),
                  ('share/accelergy/estimation_plug_ins/accelergy-wire-plugin', ['./wire.estimator.yaml']),
                  ('share/accelergy/primitive_component_libs/', ['wire.lib.yaml'])
                  ],
      include_package_data = True,
      entry_points = {},
      zip_safe = False,
    )
