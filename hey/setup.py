from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='OrganizerPro',
    version='0.1.0',  # Update this with every release
    packages=find_packages(),
    include_package_data=True,
    package_data={
    'organizerpro': ['data/*.txt'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'openai',  # Add any other dependencies required
    ],
    python_requires='>=3.6',  # Assuming your package is compatible with Python 3.6 and above
    entry_points={
        'console_scripts': [
            'organizerpro=organizerpro.main:main',  # Update the path to your main script
        ],
    },
    author='Christopher EK',
    author_email='chr.oak@icloud.com',
    description='OrganizerPro is a Python-based utility designed to intelligently organize files using the OpenAI ChatGPT API.',
    license='MIT',
    keywords='ai organizer',
    url='https://github.com/chroakPRO/Desktop-Cleaner/tree/ai-integration',  # Your project's main homepage
    download_url='https://github.com/chroakPRO/Desktop-Cleaner/archive/refs/heads/ai-integration.zip',  # Link to a specific release
    classifiers=[
        'Development Status :: 3 - Alpha',  # Update as per your development status
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
