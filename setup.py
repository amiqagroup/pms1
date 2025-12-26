from setuptools import setup, find_packages

setup(
    name="uae_property_management",
    version="0.1.0",
    description="Leasing-focused property management for UAE",
    long_description=open(
        "README.md", encoding="utf-8").read() if __name__ == "__main__" else "",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "frappe>=15.0.0,<17.0.0",
        "erpnext>=15.0.0,<17.0.0",
    ],
    python_requires=">=3.11",
)
