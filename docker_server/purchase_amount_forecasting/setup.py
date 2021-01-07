from setuptools import setup, find_packages

setup(
    name = 'purchase_amount_forecasting',
    version = '0.2',
    packages = find_packages(),
    url='',
    author='Lei You',
    author_email='lei.you@pm.me',
    description='Purchase amount forecasting case study',
    install_requires=['fbprophet']
)
