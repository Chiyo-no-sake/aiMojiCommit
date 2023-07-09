from setuptools import setup, find_packages

setup(
    name='aimojicommit',
    version='1.0.0',
    author='Luca Pasini',
    author_email='luca.pasini.26@gmail.com',
    description='AI commit generator with OpenAI',
    packages=find_packages(),
    data_files=[('', ['requirements.txt'])],
    install_requires=[
        'click==8.1.4',
        'pick==2.2.0',
        'tiktoken==0.4.0',
        'openai==0.27.8',
    ],
    entry_points={
        'console_scripts': [
            'aimoji=aimojicommit.aimojicommit:aimojicommit',
        ],
    },
)
