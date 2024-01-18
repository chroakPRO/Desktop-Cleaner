from setuptools import setup, find_packages

setup(
    name='Organizer-Pro',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # List your package dependencies here
        # 'numpy',
        # 'pandas',
        'openai',
        

    ],
    # Additional metadata
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    license='MIT',
    keywords='ai organizer',
)
