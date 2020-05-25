import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="bbpr",
    version="0.0.2",
    description="Pull request manager for BitBucket",
    url="https://github.com/rahulnehru/timesavers",
    author="Rahul Nehru",
    author_email="rnehru92@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["bbpr"],
    include_package_data=True,
    install_requires=install_requires,
    entry_points={"console_scripts": ["bbpr=bbpr.cli:main"]},
)