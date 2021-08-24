import setuptools  # type: ignore

setuptools.setup(
    name="rendering_server_client",
    version="0.0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
