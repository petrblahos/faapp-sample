import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    'Babel', 'lingua',
    'transaction', 'pyramid_tm',
    'sqlalchemy', 'zope.sqlalchemy',
    'formalchemy',
    ]

setup(name='faapp',
      version='0.0',
      description='faapp',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      message_extractors = { 'faapp': [
        ('**.py',   'lingua_python', None ),
        ('**.pt',   'lingua_xml', None ),
        ('templates/**.mako', 'mako', None),
        ('static/**', 'ignore', None),
        ]},
      tests_require=requires,
      test_suite="faapp",
      entry_points = """\
      [paste.app_factory]
      main = faapp:main
      [console_scripts]
      initialize_faapp_db = faapp.scripts.initializedb:main
      """,
      )

