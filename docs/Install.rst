Installing ``ancIBD``
===============

You can find ``ancIBD`` on the official Python package repository (PyPI). It can be installed using ``pip``:
::
    python3 -m pip install ancIBD

The software package distributes all source code that ``pip`` then compiles automatically during installation. 

Expert note: The file ``setup.py`` contains the relevant installation information. In specific cases, you can manually compile the relevant C code using ``Cython``.



Upgrading ``ancIBD``   
************
If you already have a ``ancIBD`` release installed and wish to upgrade to the latest release, you can do so with ``pip`` by adding ``--upgrade``:
::
    pip install --upgrade ancIBD
    
c Extension
************
For performance reasons, the heavy lifting of the algorithms is coded into C methods (``cfunc.c``). This "extension" is built automatically during installation from ``cfunc.pyx`` via the package cython (when ``CYTHON=True`` in setup.py, the default setting). If you set ``CYTHON=False``, the extension is directly compiled from ``cfunc.c`` (experimental, not tested on all platforms).


Dependencies
************
The basic Python package dependencies are sufficient for the core functions of  ``ancIBD``. We kept the required dependencies minimal to avoid creating dependency conflicts. When ``ancIBD`` is installed, the following dependent Python packages will be automatically installed without any further action on your part:

* ``numpy`` for calculations with numerical arrays at C speed 
* ``pandas`` for handling databases and tables at C speed 
* ``h5py`` for handling hdf5, a file format with partial I/O
* ``psutil`` for process monitoring

Some downstream and advanced functionalities require additional packages, such as ``matplotlib`` for specific plots. If you need those, import errors will alert you. You can then install missing packages manually via ``pip`` (as above for ``ancIBD``).
