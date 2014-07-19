from setuptools import find_packages, setup


setup(
    name="pinax-forums",
    version=__import__("forums").__version__,
    author="",
    author_email="",
    description="an extensible forum app for Django and Pinax",
    long_description=open("README.rst").read(),
    license="MIT",
    url="http://github.com/pinax/pinax-forums/",
    packages=find_packages(),
    install_requires=[
        "django-appconf>=0.6",
        "django-user-accounts==1.0c9"
    ],
    test_suite="runtests.runtests",
    tests_require=[
        "django-appconf>=0.6",
        "Django>=1.5",
        "django-user-accounts==1.0c9"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
