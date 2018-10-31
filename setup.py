from setuptools import setup

setup(name='drz',
      version='0.2.2',
      description='A painless deployment system for modern code',
      url='https://github.com/kilometercreative/Drizzle',
      author='Kaeden Wile',
      author_email='kaeden@kilometercreative.com',
      license='MIT',
      packages=['drz'],
      entry_points={'console_scripts': ['drz=drz:entrypoint']},
      # install_requires=[
      #     'awscli',  # just so we have it downloaded
      # ],
      include_package_data=True,
      zip_safe=False)
