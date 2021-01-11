import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi-manage",  # Replace with your own username
    version="0.0.1",
    author="auxpd",
    author_email="auxpd96@163.com",
    description="fastapi project manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/LeanDe/fastapi_manage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
