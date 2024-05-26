from setuptools import setup

setup(
    name='starSeer',
    version='1.0',
    author='Ramon Gargalhone',
    author_email='ramonefoster@gmail.com',
    description='Minimizing telescope (mounts) pointing errors using Machine Learning.',
    packages=['starSeer'],
    install_requires=[
        # List any dependencies your module requires
        'pandas',
        'scikit-learn',
        'joblib',
        'pathlib',
    ],
)
