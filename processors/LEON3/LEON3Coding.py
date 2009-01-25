####################################################################################
#         ___        ___           ___           ___
#        /  /\      /  /\         /  /\         /  /\
#       /  /:/     /  /::\       /  /::\       /  /::\
#      /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
#     /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
#    /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
#   /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
#   \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
#        \  \:\   \  \:\        \  \:\        \  \:\
#         \  \ \   \  \:\        \  \:\        \  \:\
#          \__\/    \__\/         \__\/         \__\/
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


import trap

#---------------------------------------------------------
# Instruction Encoding
#---------------------------------------------------------
# Lets now start with defining the instructions, i.e. their bitstring and
# mnemonic and their behavior. Note the zero* field: it is a special identifier and it
# means that all those bits have value 0; the same applies for one*
# As stated in page 44 of "The SPARC Architecture Manual V8" there are
# mainly 6 different format types

# Call instruction format
call_format = trap.MachineCode([('op', 2), ('disp30', 30)])
call_format.setBitfield('op', [0, 1])

# Branch and sethi instructions format
b_sethi_format1 = trap.MachineCode([('op', 2), ('rd', 5), ('op2', 3), ('imm22', 22)])
b_sethi_format1.setBitfield('op', [0, 0])
b_sethi_format1.setVarField('rd', ('REGS', 0), 'out')
b_sethi_format2 = trap.MachineCode([('op', 2), ('a', 1), ('cond', 4), ('op2', 3), ('disp22', 22)])
b_sethi_format2.setBitfield('op', [0, 0])

# Memory instruction format
memory_format = trap.MachineCode([('op', 2), ('rd', 5), ('op3', 6), ('rs1', 5), ('zero', 1), ('asi', 8), ('rs2', 5)])
memory_format.setBitfield('op', [1, 1])
# memory_format.setVarField('rd', ('REGS', 0), 'out') # for load is destination for write is source register, set in the instruction
memory_format.setVarField('rs1', ('REGS', 0), 'in')
memory_format.setVarField('rs2', ('REGS', 0), 'in')

# Remaining (logical and other) instruction formats
dpi_format1 = trap.MachineCode([('op', 2), ('rd', 5), ('op3', 6), ('rs1', 5), ('one', 1), ('simm13', 13)])
dpi_format1.setBitfield('op', [1, 0])
dpi_format1.setVarField('rd', ('REGS', 0), 'out')
dpi_format1.setVarField('rs1', ('REGS', 0), 'in')

# Coprocessor of fpu instruction format
coprocessor_format = trap.MachineCode([('op', 2), ('rd', 5), ('op3', 6), ('rs1', 5), ('opf', 9), ('rs2', 5)])
coprocessor_format.setBitfield('op', [1, 0])
coprocessor_format.setVarField('rd', ('REGS', 0), 'out')
coprocessor_format.setVarField('rs1', ('REGS', 0), 'in')
coprocessor_format.setVarField('rs2', ('REGS', 0), 'in')

