
setup(
   name='fencrypt',
   version='1.0',
   description='A useful module',
   license="Private",
   long_description="Fencrypt Applied Cryptography Assignement",
   author='Isaiah Genis',
   author_email='ig596@nyu.edu',
   url="http://www.foopackage.com/",
   packages=['fencrypt'],  #same as name
   install_requires=['wheel', 'bar', 'greek','pycryptodome'], #external packages as dependencies
   scripts=[
            'fencrypt',
            'fencrypt_api',
           ]
)
