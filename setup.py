from setuptools import setup, find_packages

setup(
    name="scheduling-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'flask>=3.1.0',
        'flask-sqlalchemy>=3.1.1',
        'flask-jwt-extended>=4.7.1',
        'flask-cors>=5.0.1',
        'flask-restful>=0.3.10',
        'python-dotenv>=1.0.0',
        'werkzeug>=3.0.1',
        'prometheus-client>=0.19.0'
    ],
    entry_points={
        'console_scripts': [
            'scheduling-system=src.app:main'
        ]
    }
)
