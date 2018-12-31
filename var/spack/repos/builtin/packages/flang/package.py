# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Flang(CMakePackage):
    """Flang is a Fortran compiler targeting LLVM."""

    homepage = "https://github.com/flang-compiler/flang"

    url      = "https://github.com/flang-compiler/flang/archive/flang_20180612.tar.gz"
    git      = "https://github.com/flang-compiler/flang.git"

    version('develop', branch='master')
    version('20180921', '4440ed5fdc390e4b7a085fb77b44ac54')
    version('20180612', '62284e26214eaaff261a922c67f6878c')

    depends_on('llvm@flang-develop', when='@develop')
    depends_on('llvm@flang-20180921', when='@20180921 target=x86_64')
    depends_on('llvm@flang-20180612', when='@20180612 target=x86_64')

    # LLVM version specific to OpenPOWER.
    depends_on('llvm@flang-ppc64le-20180921', when='@20180921 target=ppc64le')
    depends_on('llvm@flang-ppc64le-20180612', when='@20180612 target=ppc64le')

    depends_on('pgmath@develop', when='@develop')
    depends_on('pgmath@20180921', when='@20180921')
    depends_on('pgmath@20180612', when='@20180612')

    def cmake_args(self):
        options = [
            '-DWITH_WERROR=OFF',
            '-DCMAKE_C_COMPILER=%s' % os.path.join(
                self.spec['llvm'].prefix.bin, 'clang'),
            '-DCMAKE_CXX_COMPILER=%s' % os.path.join(
                self.spec['llvm'].prefix.bin, 'clang++'),
            '-DCMAKE_Fortran_COMPILER=%s' % os.path.join(
                self.spec['llvm'].prefix.bin, 'flang'),
            '-DFLANG_LIBOMP=%s' % find_libraries(
                'libomp', root=self.spec['llvm'].prefix.lib)
        ]

        return options

    @run_after('install')
    def post_install(self):
        # we are installing flang in a path different from llvm, so we
        # create a wrapper with -L for e.g. libflangrti.so and -I for
        # e.g. iso_c_binding.mod. -B is needed to help flang to find
        # flang1 and flang2. rpath_arg is needed so that executables
        # generated by flang can find libflang later.
        flang = os.path.join(self.spec.prefix.bin, 'flang')
        with open(flang, 'w') as out:
            out.write('#!/bin/bash\n')
            out.write(
                '{0} -I{1} -L{2} -L{3} {4}{5} {6}{7} -B{8} "$@"\n'.format(
                    self.spec['llvm'].prefix.bin.flang,
                    self.prefix.include, self.prefix.lib,
                    self.spec['pgmath'].prefix.lib,
                    self.compiler.fc_rpath_arg, self.prefix.lib,
                    self.compiler.fc_rpath_arg,
                    self.spec['pgmath'].prefix.lib, self.spec.prefix.bin))
            out.close()
        chmod = which('chmod')
        chmod('+x', flang)

    def setup_environment(self, spack_env, run_env):
        # to find llvm's libc++.so
        spack_env.set('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
        run_env.set('FC', join_path(self.spec.prefix.bin, 'flang'))
        run_env.set('F77', join_path(self.spec.prefix.bin, 'flang'))
        run_env.set('F90', join_path(self.spec.prefix.bin, 'flang'))
