from setuptools import setup

setup(
    name='starSeer',
    version='1.0',
    author='Ramon Gargalhone',
    author_email='rgargalhone@lna.br',
    description='Minimizing telescope (mounts) pointing errors using NN.',
    packages=['starSeer'],
    install_requires=[
        # List any dependencies your module requires
        'pandas',
        'scikit-learn',
        'joblib',
        'pathlib',
    ],
)
