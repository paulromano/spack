.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _binary_caches:

============
Build Caches
============

Some sites may encourage users to set up their own test environments
before carrying out central installations, or some users may prefer to set
up these environments on their own motivation. To reduce the load of
recompiling otherwise identical package specs in different installations,
installed packages can be put into build cache tarballs, uploaded to
your Spack mirror and then downloaded and installed by others.


--------------------------
Creating build cache files
--------------------------

A compressed tarball of an installed package is created. Tarballs are created
for all of its link and run dependency packages as well. Compressed tarballs are
signed with gpg and signature and tarball and put in a ``.spack`` file. Optionally,
the rpaths (and ids and deps on macOS) can be changed to paths relative to
the Spack install tree before the tarball is created.

Build caches are created via:

.. code-block:: console

   $ spack buildcache create spec


---------------------------------------
Finding or installing build cache files
---------------------------------------

To find build caches or install build caches, a Spack mirror must be configured
with:

.. code-block:: console

   $ spack mirror add <name> <url>

Build caches are found via:

.. code-block:: console

   $ spack buildcache list

Build caches are installed via:

.. code-block:: console

   $ spack buildcache install

Note that the above command is intended to install a particular package to a
build cache you have created, and not to install a package from a build cache.
For the latter, once a mirror is added, by default when you do ``spack install`` the ``--use-cache``
flag is set, and you will install a package from a build cache if it is available.
If you want to always use the cache, you can do:

.. code-block:: console

   $ spack install --cache-only <package>

For example, to combine all of the commands above to add the E4S build cache
and then install from it exclusively, you would do:

.. code-block:: console

    $ spack mirror add E4S https://cache.e4s.io
    $ spack buildcache keys --install --trust
    $ spack install --cache-only <package>

We use ``--install`` and ``--trust`` to say that we are installing keys to our
keyring, and trusting all downloaded keys.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
List of popular build caches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Extreme-scale Scientific Software Stack (E4S) <https://e4s-project.github.io/>`_: `build cache <https://oaciss.uoregon.edu/e4s/inventory.html>`_


----------
Relocation
----------

Initial build and later installation do not necessarily happen at the same
location. Spack provides a relocation capability and corrects for RPATHs and
non-relocatable scripts. However, many packages compile paths into binary
artifacts directly. In such cases, the build instructions of this package would
need to be adjusted for better re-locatability.

.. _cmd-spack-buildcache:

--------------------
``spack buildcache``
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create tarball of installed Spack package and all dependencies.
Tarballs are checksummed and signed if gpg2 is available.
Places them in a directory ``build_cache`` that can be copied to a mirror.
Commands like ``spack buildcache install`` will search Spack mirrors for build_cache to get the list of build caches.

==============  ========================================================================================================================
Arguments       Description
==============  ========================================================================================================================
``<specs>``     list of partial specs or hashes with a leading ``/`` to match from installed packages and used for creating build caches
``-d <path>``   directory in which ``build_cache`` directory is created, defaults to ``.``
``-f``          overwrite ``.spack`` file in ``build_cache`` directory if it exists
``-k <key>``    the key to sign package with. In the case where multiple keys exist, the package will be unsigned unless ``-k`` is used.
``-r``          make paths in binaries relative before creating tarball
``-y``          answer yes to all create unsigned ``build_cache`` questions
==============  ========================================================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache list``
^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieves all specs for build caches available on a Spack mirror.

==============  =====================================================================================
Arguments       Description
==============  =====================================================================================
``<specs>``     list of partial package specs to be matched against specs downloaded for build caches
==============  =====================================================================================

E.g. ``spack buildcache list gcc`` with print only commands to install ``gcc`` package(s)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache install``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieves all specs for build caches available on a Spack mirror and installs build caches
with specs matching the specs input.

==============  ==============================================================================================
Arguments       Description
==============  ==============================================================================================
``<specs>``     list of partial package specs or hashes with a leading ``/`` to be installed from build caches
``-f``          remove install directory if it exists before unpacking tarball
``-y``          answer yes to all to don't verify package with gpg questions
==============  ==============================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache keys``
^^^^^^^^^^^^^^^^^^^^^^^^^

List public keys available on Spack mirror.

=========  ==============================================
Arguments  Description
=========  ==============================================
``-i``     trust the keys downloaded with prompt for each
``-y``     answer yes to all trust all keys downloaded
=========  ==============================================
