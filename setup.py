from setuptools import setup, find_packages

setup(name='py7D',
      version='0.0.1',
      description = 'A lightweight python interface to 7Digital web service',
      author = "Jason Rubenstein",
      author_email = 'jasondrubenstein@gmail.com',
      url = 'git://github.com/jasonrubenstein/python-7Digital.git',
      package_dir = {'' : 'lib'},
      py_modules = ['lockerEndpoint', 'oauth7digital', 'py7D'],
      install_requires = ['xmltodict', 'oauth2'],
      license = 'MIT License',
      keywords = '7Digital, py7D',
      zip_safe = True)
