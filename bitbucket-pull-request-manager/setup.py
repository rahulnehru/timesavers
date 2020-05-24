setup(
    name="bbpr",
    version="0.0.1",
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
    install_requires=[
        "os", "requests", "getpass", "gitpython", "datetime", "sys"
    ],
    entry_points={"console_scripts": ["bbrp=bbpr"]},
)