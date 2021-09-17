from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="cricket-player-basic-visualization",
      version="0.1",
      description="Basic visualizations/info of cricket players based on ESPN Cricinfo Statsguru",
      license="MIT",
      author="Anvesh Teegala",
      author_email="anv12345@gmail.com",
      # url="https://github.com/anveshs1/cricket-player-analysis",
      packages=find_packages(),
      keywords=['cricket'], 
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ])
