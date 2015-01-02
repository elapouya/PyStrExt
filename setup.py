from setuptools import setup

setup(name='pystrext',
      version='0.1.5',
      description='Python string extension',
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='string helpers',
      url='https://pypi.python.org/pypi/pystrext',
      author='Eric Lapouyade',
      author_email='elapouya@gmail.com',
      license='LGPL 2.1',
      packages=['pystrext'],
      install_requires = ['Sphinx', 'sphinxcontrib-napoleon'],
      zip_safe=False)
