from setuptools import setup

try:
    from jupyterpip import cmdclass
except:
    import pip, importlib
    pip.main(['install', 'jupyter-pip']); cmdclass = importlib.import_module('jupyterpip').cmdclass

setup(
    name='progressbar',
    version='0.1',
    description='Implaments simple progressbars',
    author='Ryan Morshead',
    author_email='ryan.morshead@gmail.com',
    license='New BSD License',
    url='https://github.com/rmorshead/progressbar',
    keywords='progressbar',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Programming Language :: Python',
                 'License :: OSI Approved :: MIT License'],
    packages=['progressbar', 'progressbar/py'],
    include_package_data=True,
    install_requires=["jupyter-pip"],
    cmdclass=cmdclass('progressbar'),
)