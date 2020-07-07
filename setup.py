from setuptools import setup, find_packages

setup(
    name="flask-react-auth-backend",
    version="0.1",
    packages=find_packages(),
    # scripts=["say_hello.py"],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        "Flask-Dance[sqla]",
        "email_validator",
        "Flask-Security",
    ],
    # metadata to display on PyPI
    author="Andrew Owen Martin",
    author_email="andrew@aomartin.co.uk",
    description="Minimal example of using authentication with React in the front and Flask in the back.",
    keywords="flask react auth oauth",
    # url="http://example.com/HelloWorld/",   # project home page, if any
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },
    classifiers=["License :: OSI Approved :: Apache Software License"]
    # could also include long_description, download_url, etc.
)
