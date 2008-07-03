####################################################################################
#                    ___           ___           ___
#        ___        /  /\         /  /\         /  /\
#       /  /\      /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \__\/    \  \:\        \  \:\        \  \:\
#                   \__\/         \__\/         \__\/
#
#   This file is part of TRAP.
#
#   TRAP is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this TRAP; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
#   or see <http://www.gnu.org/licenses/>.
#
#   (c) Luca Fossati, fossati@elet.polimi.it
#
####################################################################################


banner = r"""
                 ___           ___           ___
     ___        /  /\         /  /\         /  /\
    /  /\      /  /::\       /  /::\       /  /::\
   /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
  /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
 /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
/__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
\__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
     \  \:\   \  \:\        \  \:\        \  \:\
      \__\/    \  \:\        \  \:\        \  \:\
                \__\/         \__\/         \__\/
"""

license = r"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the
Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA.
"""

copyright = """(c) Luca Fossati, fossati@elet.polimi.it"""

import os
import Writer

class FileDumper:
    """Dumps a file; a file is composed of members which are the ones described
    in SimpleDecls and ClassDecls"""
    def __init__(self, name, isHeader):
        self.name = name
        self.members = []
        self.isHeader = isHeader

    def addMember(self, member):
        self.members.append(member)

    def write(self):
        #First I write the license, comments etc..
        #then the includes and finally the members,
        #in the same order in which they are contained
        #inside self.members
        fileHnd = open(self.name, 'wt')
        print >> fileHnd, '/***************************************************************************\\'
        print >> fileHnd, '*   '
        for line in banner.split('\n'):
            print >> fileHnd, '*   ' + line
        print >> fileHnd, '*   '
        print >> fileHnd, '*   '
        for line in license.split('\n'):
            print >> fileHnd, '*   ' + line
        print >> fileHnd, '*   '
        print >> fileHnd, '*   '
        for line in copyright.split('\n'):
            print >> fileHnd, '*   ' + line
        print >> fileHnd, '*   '
        print >> fileHnd, '\\***************************************************************************/\n\n'
        # Now I can start priting the actual code: lets create the writer
        writer = Writer.CodeWriter(fileHnd)
        if self.isHeader:
            writer.write('#ifndef ' + self.name.replace('.','_').upper() + '\n')
            writer.write('#define ' + self.name.replace('.','_').upper() + '\n')
        # as a first thing I compute the includes and print them
        includes = []
        for member in self.members:
            try:
                for include in member.getIncludes():
                    if include and not include in includes:
                        includes.append(include)
            except AttributeError:
                pass
        for include in includes:
            writer.write('#include <' + include + '>\n')
        writer.write('\n')
        # Now I simply have to print in order all the members
        for member in self.members:
            if self.isHeader:
                try:
                    member.writeDeclaration(writer)
                except AttributeError:
                    pass
            else:
                try:
                    member.writeImplementation(writer)
                except AttributeError:
                    pass
        if self.isHeader:
            writer.write('\n\n#endif')
        writer.write('\n')
        fileHnd.close()

class Folder:
    """A collection of files; in addition to creating the
    specified folder and to populating it with files,
    it also creates the correct wscript for the compilation"""
    def __init__(self, path):
        if not path:
            path = '.'
        self.path = os.path.abspath(path)
        self.headers = []
        self.codeFiles = []
        self.subfolders = []

    def addHeader(self, header):
        self.headers.append(header)

    def addCode(self, codeFile):
        self.codeFiles.append(codeFile)

    def addSubFolder(self, subfolder):
        commonPart = os.path.commonprefix((subfolder.path, self.path))
        if commonPart == self.path:
            subfolder = subfolder.path[subfolder.path.find(commonPart):]
        else:
            subfolder.path = os.path.join(self.path, os.path.split(subfolder.path)[-1])
            subfolder = subfolder.path
        if subfolder and not subfolder in self.subfolders:
            self.subfolders.append(subfolder)

    def create(self, configure = False):
        # Creates the folder and populates it with files.
        # it also creates the appropriate wscript for the
        # compilation
        curDir = os.getcwd()
        self.path = os.path.split(self.path)
        for i in self.path:
            if not os.path.exists(i):
                os.mkdir(i)
            os.chdir(i)
        for header in self.headers:
            header.write()
        for codeFile in self.codeFiles:
            codeFile.write()
        # Now I can finally create the wscript for the compilation
        # of the current folder; note that event though the project is
        # small we need to create the configure part
        self.createWscript(configure)
        os.chdir(curDir)

    def createWscript(self, configure):
        wscriptFile = open('wscript', 'wt')
        print >> wscriptFile, '#!/usr/bin/env python\n'
        if configure:
            print >> wscriptFile, '# these variables are mandatory'
            print >> wscriptFile, 'srcdir = \'.\''
            print >> wscriptFile, 'blddir = \'_build_\''
        print >> wscriptFile, 'import os\n'
        if self.codeFiles or self.subfolders:
            print >> wscriptFile, 'def build(bld):'
            if self.subfolders:
                print >> wscriptFile, '    bld.add_subdirs(\'' + ' '.join(self.subfolders) + '\')\n'
            if self.codeFiles:
                print >> wscriptFile, '    obj = bld.new_task_gen(\'cxx\', \'program\')'
                print >> wscriptFile, '    obj.source=\"\"\"'
                for codeFile in self.codeFiles:
                    print >> wscriptFile, '        ' + codeFile.name
                print >> wscriptFile, '    \"\"\"'
                print >> wscriptFile, '    obj.uselib = \'BOOST\''
                print >> wscriptFile, '    obj.name = \'' + self.path[-1] + '\''
                print >> wscriptFile, '    obj.target = \'' + self.path[-1] + '\'\n'
        # Ok, here I need to insert the configure script if needed
        if configure:
            print >> wscriptFile, 'def configure(conf):'
            print >> wscriptFile, """
    # I make sure that the search paths really exists and eliminates the non
    # existing ones (usefull in case your PC doesn't have the /usr/local/include
    # folder for example)
    import Configure

    incl_path = []
    for path in Configure.g_stdincpath:
        if os.path.exists(path):
            incl_path.append(path)
    Configure.g_stdincpath = incl_path
    lib_path = []

    Configure.g_stdlibpath += ['/usr/lib64/']
    for path in Configure.g_stdlibpath:
        if os.path.exists(path):
            lib_path.append(path)
    Configure.g_stdlibpath = lib_path

    # Set Optimized as the default compilation mode, enabled if no other is selected on the command line
    try:
        if Params.g_options.debug_level == '':
            Params.g_options.debug_level = "OPTIMIZED"
    except:
        pass

    # Check for standard tools
    conf.check_tool('g++ gcc misc')
    # Check for python
    conf.check_tool('python')
    conf.check_python_version((2,4))

    ########################################
    # Check for special gcc flags
    ########################################
    if not conf.check_flags(''):
        Params.fatal('gcc does not support the custom flags used. Please change gcc version of the custom flags')
    if not Params.g_options.static_plat:
        if not conf.check_flags('-Wl,-rpath .'):
            Params.fatal('gcc does not support -Wl,-rpath flag. Please change gcc version')

    ########################################
    # Setting the host endianess
    ########################################
    if sys.byteorder == "little":
        conf.env.append_unique('CPPFLAGS','-DLITTLE_ENDIAN_BO')
        conf.check_message_custom('endianness', '', 'little')
    else:
        conf.env.append_unique('CPPFLAGS','-DBIG_ENDIAN_BO')
        conf.check_message_custom('endianness', '', 'big')

    ########################################
    # Check for boost libraries
    ########################################
    boostconf = conf.create_boost_configurator()
    boostconf.lib = ['thread', 'regex', 'date_time' , 'program_options' , 'system', 'filesystem','unit_test_framework']
    boostconf.min_version = '1.35.0'
    boostconf.run()

    ##################################################
    # Check for pthread library/flag
    ##################################################
    if conf.check_flags('-pthread'):
        conf.env.append_unique('LINKFLAGS', '-pthread')
        conf.env.append_unique('CXXFLAGS', '-pthread')
        conf.env.append_unique('CFLAGS', '-pthread')
        conf.env.append_unique('CCFLAGS', '-pthread')
        pthread_uselib = []
    else:
        le = conf.create_library_enumerator()
        le.mandatory = 1
        le.name = 'pthread'
        le.message = 'pthread library'
        pthread_uselib = ['pthread']
        conf.env.append_unique('LIB', le.run())

    ##################################################
    # Is SystemC compiled? Check for SystemC library
    # Notice that we can't rely on lib-linux, therefore I have to find the actual platform...
    ##################################################
    # First I set the clafgs needed by TLM 2.0 for including systemc dynamic process
    # creation
    conf.env.append_unique('CPPFLAGS','-DSC_INCLUDE_DYNAMIC_PROCESSES')
    syscpath = None
    if Params.g_options.systemcdir:
        syscpath = ([os.path.abspath(os.path.join(Params.g_options.systemcdir, 'include'))])
    elif 'SYSTEMC' in os.environ:
        syscpath = ([os.path.abspath(os.path.join(os.environ['SYSTEMC'], 'include'))])

    le = conf.create_library_enumerator()
    le.mandatory = 1
    le.uselib_store = 'SYSTEMC'
    le.name = 'systemc'
    le.message = 'Library SystemC ver. 2.2.0 not found'
    le.nosystem = 1
    import glob
    if syscpath:
        sysclib = le.path = glob.glob(os.path.join(os.path.abspath(os.path.join(syscpath[0], '..')), 'lib-*'))
    le.run()
    ######################################################
    # Check if systemc is compiled with quick threads or not
    ######################################################
    if not os.path.exists(os.path.join(syscpath[0] , 'sysc' , 'qt')):
        conf.env.append_unique('CPPFLAGS', '-DSC_USE_PTHREADS')

    ##################################################
    # Check for SystemC header and test the library
    ##################################################
    he = conf.create_header_configurator()
    he.mandatory = 1
    he.header_code = \"\"\"
        #include <systemc.h>

        #ifndef SYSTEMC_VERSION
        #error SYSTEMC_VERSION not defined in file sc_ver.h
        #endif

        #if SYSTEMC_VERSION < 20070314
        #error Wrong SystemC version
        #endif

        extern "C" {
            int sc_main(int argc, char** argv) {
                wif_trace_file trace("");
                trace.set_time_unit(1, SC_NS);
                return 0;
            };
        }
    \"\"\"
    he.path = syscpath
    he.name = "systemc.h"
    he.message = 'Library and Headers for SystemC ver. 2.2.0 or greater not found'
    he.uselib = 'SYSTEMC'
    he.uselib_store = 'SYSTEMC'
    he.lib_paths = sysclib
    he.run()

    ##################################################
    # Check for TLM header
    ##################################################
    he = conf.create_header_configurator()
    he.mandatory = 1
    he.name = "tlm.h"
    he.uselib = 'SYSTEMC'
    he.lib_paths = sysclib
    he.uselib_store = 'TLM'
    he.header_code = \"\"\"
        #include <systemc.h>
        #include <tlm.h>

        #ifndef TLM_VERSION_MAJOR
        #error TLM_VERSION_MAJOR undefined in the TLM library
        #endif
        #ifndef TLM_VERSION_MINOR
        #error TLM_VERSION_MINOR undefined in the TLM library
        #endif
        #ifndef TLM_VERSION_PATCH
        #error TLM_VERSION_PATCH undefined in the TLM library
        #endif

        #if TLM_VERSION_MAJOR < 2
        #error Wrong TLM version; required 2.0
        #endif

        extern "C" int sc_main(int argc, char **argv){
            return 0;
        }
    \"\"\"
    he.message = 'Library and Headers for TLM ver. 2.0 not found'
    if Params.g_options.tlmdir:
        he.path = [os.path.abspath(os.path.join(Params.g_options.tlmdir, 'tlm'))]
    elif 'TLM' in os.environ:
        he.path = [os.path.abspath(os.path.join(os.environ['TLM'], 'tlm'))]
    he.run()

"""
            # Finally now I can add the options
            print >> wscriptFile, 'def set_options(opt):'
            print >> wscriptFile, """
    build_options = opt.add_option_group('General Build Options')
    opt.tool_options('python', option_group=build_options) # options for disabling pyc or pyo compilation
    opt.tool_options('gcc', option_group=build_options)
    opt.tool_options('g++', option_group=build_options)
    opt.tool_options('compiler_cc')
    opt.tool_options('compiler_cxx')
    opt.tool_options('boost', option_group=build_options)
    # Specify SystemC and TLM path
    opt.add_option('--with-systemc', type='string', help='SystemC installation directory', dest='systemcdir' )
    opt.add_option('--with-tlm', type='string', help='TLM installation directory', dest='tlmdir')
    # Specify the options for the processor creation
    # Specify if GDB integration should be compiled inside processor models
    opt.add_option('-D', '--enable-debug', default=False, action="store_true", help='Enables the debugging functionalities inside the processor (switch)', dest='enable_debug')
    # Specify if profiling support should be compiled inside processor models
    opt.add_option('-P', '--enable-profiler', default=False, action="store_true", help='Enables the profiling functionalities inside the processor (switch)', dest='enable_profile')
    # Specify if tracing capabilities should be compiled inside the processor models
    opt.add_option('-T', '--enable-tracing', default=False, action="store_true", help='Enable tracing capabilites inside the ArchC processors (switch)', dest='enable_tracing')
    # Specify if OS emulation support should be compiled inside processor models
    opt.add_option('-S', '--disable-os-emu', default=True, action="store_false", help='Disable OS emulation features inside the ArchC processors (switch)', dest='enable_os_emu')
"""
        wscriptFile.close()