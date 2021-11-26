import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="volt",
    version="0.0.1",
    description="A better Vault CLI",
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
    packages=["volt"],
    include_package_data=True,
    install_requires=[
        'click',
        'hvac',
        'requests'
    ],
    entry_points={"console_scripts": ["volt=volt.volt:main"]},
)