# -*- coding: iso-8859-1 -*-
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
#   (a) Luca Fossati, fossati@elet.polimi.it
#   (b) Redwanur Rahman, md.rahman@mail.polimi.it
#   (c) Ashanka Das, ashanka.das@mail.polimi.it
####################################################################################


# Lets first of all import the necessary files for the
# creation of the processor
import trap
import cxx_writer
from PPC405Coding import *
from PPC405Methods import *

# ISA declaration: it is the container for all the single instructions
isa = trap.ISA()
#ADD
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra;
""")
add_Instr = trap.Instruction('ADD', True)
add_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
add_Instr.setCode(opCode,'execute')
add_Instr.addBehavior(IncrementPC, 'execute')
add_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(add_Instr)
#ADDC
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra;
if ((int)rb + (int)ra>exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
addc_Instr = trap.Instruction('ADDC', True)
addc_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
addc_Instr.setCode(opCode,'execute')
addc_Instr.addBehavior(IncrementPC, 'execute')
addc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addc_Instr)
#ADDE
opCode = cxx_writer.writer_code.Code("""
rt = (int)rb + (int)ra + XER[CA];
if ((int)rb + (int)ra + XER[CA] > exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
adde_Instr = trap.Instruction('ADDE', True)
adde_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,0,1,0,1,0]}, ('add r', '%rt', ' r', '%ra', ' r', '%rb'))
adde_Instr.setCode(opCode,'execute')
adde_Instr.addBehavior(IncrementPC, 'execute')
adde_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(adde_Instr)
#ADDI
opCode = cxx_writer.writer_code.Code("""
rt = (((int) ra | 0) + exts(d);
""")
addi_Instr = trap.Instruction('ADDI', True)
addi_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,1,0] }, ('addi r', '%rt', ' r ', '%ra', '  ', '%d'))
addi_Instr.setCode(opCode,'execute')
addi_Instr.addBehavior(IncrementPC, 'execute')
#addi_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addi_Instr)
#ADDIC 
opCode = cxx_writer.writer_code.Code("""
rt = (int) ra  + exts(d);
if (((int) ra  + exts(d))> (exp (2,32) -1))) XER[ca]=1;
else XER[ca]=o;
""")
addic_Instr = trap.Instruction('ADDIC', True)
addic_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,0,0] }, ('addic r', '%rt', ' r ', '%ra', '  ', '%d'))
addic_Instr.setCode(opCode,'execute')
addic_Instr.addBehavior(IncrementPC, 'execute')
#addic_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addic_Instr)
#ADDIC. 
opCode = cxx_writer.writer_code.Code("""
rt = (int) ra  + exts(d);
if (((int) ra  + exts(d))> (exp (2,32) -1))) XER[ca]=1;
else XER[ca]=o;
""")
addicdot_Instr = trap.Instruction('ADDICDOT', True)
addicdot_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,0,1] }, ('addicdot r', '%rt', ' r ', '%ra', '  ', '%d'))
addicdot_Instr.setCode(opCode,'execute')
addicdot_Instr.addBehavior(IncrementPC, 'execute')
#addic_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addicdot_Instr)
#ADDIS
opCode = cxx_writer.writer_code.Code("""
rt = ((int) ra |0) + (d | 0);
""")
addis_Instr = trap.Instruction('ADDIS', True)
addis_Instr.setMachineCode(oper_Dform_1 , {'primary_opcode': [0,0,1,1,1,1] }, ('addicdot r', '%rt', ' r ', '%ra', '  ', '%d'))
addis_Instr.setCode(opCode,'execute')
addis_Instr.addBehavior(IncrementPC, 'execute')
#addis_Instr.addTest({'rt': 3, 'ra': 1}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addis_Instr)
#ADDME
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra + XER[CA]+(-1);
if ((int)ra + XER[CA]+0xFFFFFFFF > exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
addme_Instr = trap.Instruction('ADDME', True)
addme_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,0,1,0]}, ('Add r', '%rt', ' r', '%ra'))
addme_Instr.setCode(opCode,'execute')
addme_Instr.addBehavior(IncrementPC, 'execute')
addme_Instr.addTest({'rt': 1, 'ra': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addme_Instr)
#ADDZE
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra + XER[CA];
if ((int)ra + XER[CA]> exp(2,32)-1) {
	XER[CA] = 1;
}
else {
	XER[CA] = 0;
}
""")
addze_Instr = trap.Instruction('ADDZE', True)
addze_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,1,1,0,0]}, ('Add r', '%rt', ' r', '%ra'))
addze_Instr.setCode(opCode,'execute')
addze_Instr.addBehavior(IncrementPC, 'execute')
addze_Instr.addTest({'rt': 1, 'ra': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(addze_Instr)
#AND
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & (int)rb;
""")
and_Instr = trap.Instruction('AND', True)
and_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,0,0,1,0,1,0]}, ('and r', '%ra', ' r', '%rs', ' r', '%rb'))
and_Instr.setCode(opCode,'execute')
and_Instr.addBehavior(IncrementPC, 'execute')
#and_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x66440044, 'PC':0x4})
#and_Instr.addTest({'ra': 1, 'rs': 1, 'rb': 1}, {'GPR[1]': 0xab88cd77, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[1]': 0xab88cd77, 'PC':0x4})
isa.addInstruction(and_Instr)
#ANDC
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & ~((int)rb);
""")
andc_Instr = trap.Instruction('ANDC', True)
andc_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,1,1,1,0,0]}, ('and r', '%ra', ' r', '%rs', ' r', '%rb'))
andc_Instr.setCode(opCode,'execute')
andc_Instr.addBehavior(IncrementPC, 'execute')
#andc_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andc_Instr)
#ANDI 
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & (0x0000000000000000 |(int)si);
""")
andi_Instr = trap.Instruction('ANDI', True)
andi_Instr.setMachineCode(oper_Dform_2, {'primary_opcode': [0,1,1,1,0,0]}, ('and r', '%ra', ' r', '%rs', '  ', '%si'))
andi_Instr.setCode(opCode,'execute')
andi_Instr.addBehavior(IncrementPC, 'execute')
#andi_Instr.addTest({'ra': 3, 'rs': 1, ' ': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andi_Instr)
#ANDIS
opCode = cxx_writer.writer_code.Code("""
ra = (int)rs & ((int)si | 0x0000000000000000 );
""")
andis_Instr = trap.Instruction('ANDIS', True)
andis_Instr.setMachineCode(oper_Dform_2, {'primary_opcode': [0,1,1,1,0,1]}, ('and r', '%ra', ' r', '%rs', '  ', '%si'))
andis_Instr.setCode(opCode,'execute')
andis_Instr.addBehavior(IncrementPC, 'execute')
#andis_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(andis_Instr)
#B register Mormat not found(oper_Iform may be but AA,LK not found)
opCode = cxx_writer.writer_code.Code("""
//if ( (int) aa ==1)
//LI ← target6:29
//NIA ← EXTS(LI || 20)
//else
//LI ← (target – CIA)6:29
//NIA ← CIA + EXTS(LI || 20)
//if LK = 1 
//(LR) ← CIA + 4
//PC ← NIA
""")
b_Instr = trap.Instruction('B', True)
b_Instr.setMachineCode(oper_Iform, {'primary_opcode': [0,1,0,0,1,0]}, ('TODO'))
b_Instr.setCode(opCode,'execute')
b_Instr.addBehavior(IncrementPC, 'execute')
#b_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(b_Instr)
#BC
opCode = cxx_writer.writer_code.Code("""
TODO
""")
bc_Instr = trap.Instruction('BC', True)
bc_Instr.setMachineCode(oper_Bform, {'primary_opcode': [0,1,0,0,0,0]}, ('TODO'))
bc_Instr.setCode(opCode,'execute')
bc_Instr.addBehavior(IncrementPC, 'execute')
#bc_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(bc_Instr)
#BCCTR
opCode = cxx_writer.writer_code.Code("""
TODO
""")
bccrt_Instr = trap.Instruction('BCCRT', True)
bccrt_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,0,0,1,1], 'xo': [1,0,0,0,0,1,0,0,0,0]}, ('TODO'))
bccrt_Instr.setCode(opCode,'execute')
bccrt_Instr.addBehavior(IncrementPC, 'execute')
#bccrt_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(bccrt_Instr)
#BCLR
opCode = cxx_writer.writer_code.Code("""
TODO
""")
bclr_Instr = trap.Instruction('BCLR', True)
bclr_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,0,1,0,0,0,0]}, ('TODO'))
bclr_Instr.setCode(opCode,'execute')
bclr_Instr.addBehavior(IncrementPC, 'execute')
#bclr_Instr.addTest({'ra': 3, 'rs': 1, 'rb': 2}, {'GPR[1]': 0xffcc8844, 'GPR[2]': 0x66666666, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0x99888800, 'PC':0x4})
isa.addInstruction(bclr_Instr)
#CMP
opCode = cxx_writer.writer_code.Code("""
int c0,c1,c2,c3;
if (int)ra < (int)rb c0=1;
if (int)ra > (int)rb c1=1;
if (int)ra = (int)rb c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmp_Instr = trap.Instruction('CMP', True)
cmp_Instr.setMachineCode(oper_Xform_16, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,0,0,0,0,0]}, ('cmp r', '%bf', ' r', '%ra', ' r', '%rb'))
cmp_Instr.setCode(opCode,'execute')
cmp_Instr.addBehavior(IncrementPC, 'execute')
#cmp_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmp_Instr)
#CMPI
opCode = cxx_writer.writer_code.Code("""
int c0=0,c1=0,c2=0,c3=0;
if (int)ra < exts(im_si) c0=1;
if (int)ra > exts(im_si) c1=1;
if (int)ra = exts(im_si) c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmpi_Instr = trap.Instruction('CMPI', True)
cmpi_Instr.setMachineCode(oper_Dform_5, {'primary_opcode': [0,0,1,0,1,1]}, ('cmpi r', '%bf', ' r', '%ra')) # need to check
cmpi_Instr.setCode(opCode,'execute')
cmpi_Instr.addBehavior(IncrementPC, 'execute')
#cmpi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmpi_Instr)
#CMPL
opCode = cxx_writer.writer_code.Code("""
int c0,c1,c2,c3;
if (int)ra < (int)rb c0=1;
if (int)ra > (int)rb c1=1;
if (int)ra = (int)rb c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmpl_Instr = trap.Instruction('CMPL', True)
cmpl_Instr.setMachineCode(oper_Xform_16, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,0,0,0,0,0]}, ('cmpl r', '%bf', ' r', '%ra'))
cmpl_Instr.setCode(opCode,'execute')
cmpl_Instr.addBehavior(IncrementPC, 'execute')
#cmpl_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmpl_Instr)
#CMPLI
opCode = cxx_writer.writer_code.Code("""
int c0=0,c1=0,c2=0,c3=0;
if (int)ra < exts(im_si) c0=1;
if (int)ra > exts(im_si) c1=1;
if (int)ra = exts(im_si) c2=1;
c3=XER[S0];
int n=bf;
CR[n]=c0; 
//CR[1]=c1; CR[2]=c2; CR[3]=c3;
""")
cmpli_Instr = trap.Instruction('CMPLI', True)
cmpli_Instr.setMachineCode(oper_Dform_5, {'primary_opcode': [0,0,1,0,1,0]}, ('cmpi r', '%bf', ' r', '%ra')) # need to check
cmpli_Instr.setCode(opCode,'execute')
cmpli_Instr.addBehavior(IncrementPC, 'execute')
#cmpli_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cmpli_Instr)
#CNTLZW
opCode = cxx_writer.writer_code.Code("""
int n=0;
do{
if (int) ra = 1 ;
else	{
 	n = n+1;
	ra=n;
	}
}while(n<32);
""")
cntlzw_Instr = trap.Instruction('CNTLZW', True)
cntlzw_Instr.setMachineCode(oper_Xform_13, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,0,1,1,0,1,0]}, ('cntlzw r', '%ra', ' r', '%rs'))
cntlzw_Instr.setCode(opCode,'execute')
cntlzw_Instr.addBehavior(IncrementPC, 'execute')
#cntlzw_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cntlzw_Instr)
#CRAND
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba & (int)bb;
""")
crand_Instr = trap.Instruction('CRAND', True)
crand_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,0,0,0,0,0,0,0,1]}, ('crand r', '%bt', ' r', '%ba', ' r', '%bb'))
crand_Instr.setCode(opCode,'execute')
crand_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crand_Instr)
#CRANDC
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba &  ~((int)bb);
""")
crandc_Instr = trap.Instruction('CRANDC', True)
crandc_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,0,0,0,0,0,0,1]}, ('crand r', '%bt', ' r', '%ba', ' r', '%bb'))
crandc_Instr.setCode(opCode,'execute')
crandc_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crandc_Instr)
#CREQV
opCode = cxx_writer.writer_code.Code("""
bt = ~((int) ba|(int) bb) &  ~((int) ba & (int)bb));
//(a || b) && !(a && b) xor
""")
creqv_Instr = trap.Instruction('CREQV', True)
creqv_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,0,0,1,0,0,0,0,1]}, ('creqv r', '%bt', ' r', '%ba', ' r', '%bb'))
creqv_Instr.setCode(opCode,'execute')
creqv_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(creqv_Instr)
#CRNAND
opCode = cxx_writer.writer_code.Code("""
bt = ~((int) ba & (int) bb);
""")
crnand_Instr = trap.Instruction('CRNAND', True)
crnand_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,1,1,0,0,0,0,1]}, ('crnand r', '%bt', ' r', '%ba', ' r', '%bb'))
crnand_Instr.setCode(opCode,'execute')
crnand_Instr.addBehavior(IncrementPC, 'execute')
#crand_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crnand_Instr)
#CRNOR
opCode = cxx_writer.writer_code.Code("""
bt = ~((int) ba|(int) bb);
""")
crnor_Instr = trap.Instruction('CRNOR', True)
crnor_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,0,0,1,0,0,0,0,1]}, ('crnor r', '%bt', ' r', '%ba', ' r', '%bb'))
crnor_Instr.setCode(opCode,'execute')
crnor_Instr.addBehavior(IncrementPC, 'execute')
#crnor_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crnor_Instr)
#CROR
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba|(int) bb;
""")
cror_Instr = trap.Instruction('CROR', True)
cror_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,1,1,0,0,0,0,0,1]}, ('cror r', '%bt', ' r', '%ba', ' r', '%bb'))
cror_Instr.setCode(opCode,'execute')
cror_Instr.addBehavior(IncrementPC, 'execute')
#cror_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(cror_Instr)
#CRORC
opCode = cxx_writer.writer_code.Code("""
bt = (int) ba| ~((int) bb);
""")
crorc_Instr = trap.Instruction('CRORC', True)
crorc_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,1,1,0,1,0,0,0,0,1]}, ('crorc r', '%bt', ' r', '%ba', ' r', '%bb'))
crorc_Instr.setCode(opCode,'execute')
crorc_Instr.addBehavior(IncrementPC, 'execute')
#crorc_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crorc_Instr)
#CRXOR
opCode = cxx_writer.writer_code.Code("""
bt = ((int) ba|(int) bb) &  ~((int) ba & (int)bb));
""")
crxor_Instr = trap.Instruction('CRXOR', True)
crxor_Instr.setMachineCode(oper_XLform_1, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,1,0,0,0,0,0,1]}, ('crxor r', '%bt', ' r', '%ba', ' r', '%bb'))
crxor_Instr.setCode(opCode,'execute')
crxor_Instr.addBehavior(IncrementPC, 'execute')
#crxor_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(crxor_Instr)
#DCBA
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) ba);
//dcba(ea);
""")
dcba_Instr = trap.Instruction('DCBA', True)
dcba_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,0,1,1,1,1,0,1,1,0]}, ('dcba r', '%ra', ' r', '%rb'))
dcba_Instr.setCode(opCode,'execute')
dcba_Instr.addBehavior(IncrementPC, 'execute')
#dcba_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcba_Instr)
#DCBF
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) ba);
//dcbf(ea);
""")
dcbf_Instr = trap.Instruction('DCBF', True)
dcbf_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,1,0,1,0,1,1,0]}, ('dcbf r', '%ra', ' r', '%rb'))
dcbf_Instr.setCode(opCode,'execute')
dcbf_Instr.addBehavior(IncrementPC, 'execute')
#dcbf_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbf_Instr)
#DCBI
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) ba);
//dcbi(ea);
""")
dcbi_Instr = trap.Instruction('DCBI', True)
dcbi_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,0,1,0,1,1,0]}, ('dcbi r', '%ra', ' r', '%rb'))
dcbi_Instr.setCode(opCode,'execute')
dcbi_Instr.addBehavior(IncrementPC, 'execute')
#dcbi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbi_Instr)
#DCBST
opCode = cxx_writer.writer_code.Code("""
//dcbst(ea);
""")
dcbst_Instr = trap.Instruction('DCBST', True)
dcbst_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,1,1,0,1,1,0]}, ('dcbst r', '%ra', ' r', '%rb'))
dcbst_Instr.setCode(opCode,'execute')
dcbst_Instr.addBehavior(IncrementPC, 'execute')
#dcbst_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbst_Instr)
#DCBT
opCode = cxx_writer.writer_code.Code("""
//dcbt(ea);
""")
dcbt_Instr = trap.Instruction('DCBT', True)
dcbt_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,0,0,0,1,0,1,1,0]}, ('dcbt r', '%ra', ' r', '%rb'))
dcbt_Instr.setCode(opCode,'execute')
dcbt_Instr.addBehavior(IncrementPC, 'execute')
#dcbt_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbt_Instr)
#DCBTST
opCode = cxx_writer.writer_code.Code("""
//dcbtst(ea);
""")
dcbtst_Instr = trap.Instruction('DCBTST', True)
dcbtst_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,1,1,1,1,0,1,1,0]}, ('dcbtst r', '%ra', ' r', '%rb'))
dcbtst_Instr.setCode(opCode,'execute')
dcbtst_Instr.addBehavior(IncrementPC, 'execute')
#dcbtst_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbtst_Instr)
#DCBZ
opCode = cxx_writer.writer_code.Code("""
//dcbz(ea);
""")
dcbz_Instr = trap.Instruction('DCBZ', True)
dcbz_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,1,1,1,0,1,1,0]}, ('dcbz r', '%ra', ' r', '%rb'))
dcbz_Instr.setCode(opCode,'execute')
dcbz_Instr.addBehavior(IncrementPC, 'execute')
#dcbz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dcbz_Instr)
#DCCCI
opCode = cxx_writer.writer_code.Code("""
//dcbtst(ea);
""")
dccci_Instr = trap.Instruction('DCCCI', True)
dccci_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,0,0,0,1,1,0]}, ('dccci r', '%ra', ' r', '%rb'))
dccci_Instr.setCode(opCode,'execute')
dccci_Instr.addBehavior(IncrementPC, 'execute')
#dccci_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dccci_Instr)
#DCREAD
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
dread_Instr = trap.Instruction('DCREAD', True)
dread_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,1,0,0,1,1,0]}, ('dread r','%ra', ' r', '%rb'))
dread_Instr.setCode(opCode,'execute')
dread_Instr.addBehavior(IncrementPC, 'execute')
#dread_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(dread_Instr)
#DIVW
opCode = cxx_writer.writer_code.Code("""
""")
divw_Instr = trap.Instruction('DIVW', True)
divw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,1,0,1,0,1,1]}, ('divw r', '%rt', ' r', '%ra', ' r', '%rb'))
divw_Instr.setCode(opCode,'execute')
divw_Instr.addBehavior(IncrementPC, 'execute')
#divw_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(divw_Instr)
#DIVWU
opCode = cxx_writer.writer_code.Code("""
""")
divwu_Instr = trap.Instruction('DIVWU', True)
divwu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,1,1,0,0,1,0,1,1]}, ('divwu r', '%rt', ' r', '%ra', ' r', '%rb'))
divwu_Instr.setCode(opCode,'execute')
divwu_Instr.addBehavior(IncrementPC, 'execute')
#divwu_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(divwu_Instr)
#EIEIO
opCode = cxx_writer.writer_code.Code("""
eieio_Instr = trap.Instruction('EIEIO', True)
eieio_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,0,1,0,1,0,1,1,0]}, ('TODO'))
eieio_Instr.setCode(opCode,'execute')
eieio_Instr.addBehavior(IncrementPC, 'execute')
#eieio_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(eieio_Instr)
#EQV
opCode = cxx_writer.writer_code.Code("""
""")
eqv_Instr = trap.Instruction('EQV', True)
eqv_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,1,1,1,1,1,0,0,0]}, ('eqv r', '%ra', ' r', '%rs', ' r', '%rb'))
eqv_Instr.setCode(opCode,'execute')
eqv_Instr.addBehavior(IncrementPC, 'execute')
#divwu_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(eqv_Instr)
#EXTSB
opCode = cxx_writer.writer_code.Code("""
""")
extsb_Instr = trap.Instruction('EXTSB', True)
extsb_Instr.setMachineCode(oper_Xform_13, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,0,1,1,1,0,1,0]}, ('extsb r', '%ra', ' r', '%rs'))
extsb_Instr.setCode(opCode,'execute')
extsb_Instr.addBehavior(IncrementPC, 'execute')
#extsb_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(extsb_Instr)
#EXTSH
opCode = cxx_writer.writer_code.Code("""
""")
extsh_Instr = trap.Instruction('EXTSH', True)
extsh_Instr.setMachineCode(oper_Xform_13, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,0,0,1,1,0,1,0]}, ('extsb r', '%ra', ' r', '%rs'))
extsh_Instr.setCode(opCode,'execute')
extsh_Instr.addBehavior(IncrementPC, 'execute')
#extsh_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(extsh_Instr)
#ICBI
opCode = cxx_writer.writer_code.Code("""
//icbi(ea);
""")
icbi_Instr = trap.Instruction('ICBI', True)
icbi_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,1,0,1,0,1,1,0]}, ('icbi r', '%ra', ' r', '%rb'))
icbi_Instr.setCode(opCode,'execute')
icbi_Instr.addBehavior(IncrementPC, 'execute')
#icbi_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(icbi_Instr)
#ICBT
opCode = cxx_writer.writer_code.Code("""
//icbt(ea);
""")
icbt_Instr = trap.Instruction('ICBT', True)
icbt_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,0,0,0,0,0,1,1,0]}, ('icbt r', '%ra', ' r', '%rb'))
icbt_Instr.setCode(opCode,'execute')
icbt_Instr.addBehavior(IncrementPC, 'execute')
#icbt_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(icbt_Instr)
#ICCCI
opCode = cxx_writer.writer_code.Code("""
//iccc(iccci cache array);
""")
iccci_Instr = trap.Instruction('ICCCI', True)
iccci_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,1,0,0,0,1,1,0]}, ('icbt r', '%ra', ' r', '%rb'))
iccci_Instr.setCode(opCode,'execute')
iccci_Instr.addBehavior(IncrementPC, 'execute')
#iccci_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(iccci_Instr)
#ICREAD
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
icread_Instr = trap.Instruction('ICREAD', True)
icread_Instr.setMachineCode(oper_Xform_23, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,1,1,1,0,0,1,1,0]}, ('icread r', '%ra', ' r', '%rb'))
icread_Instr.setCode(opCode,'execute')
icread_Instr.addBehavior(IncrementPC, 'execute')
#icread_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(icread_Instr)
#ISYNC
opCode = cxx_writer.writer_code.Code("""
""")
isync_Instr = trap.Instruction('ISYNC', True)
isync_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,0,0,1,1],'xo': [0,0,1,0,0,1,0,1,1,0]}, ('TODO'))
isync_Instr.setCode(opCode,'execute')
isync_Instr.addBehavior(IncrementPC, 'execute')
#isync_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(isync_Instr)
#LBZ
opCode = cxx_writer.writer_code.Code("""
""")
lbz_Instr = trap.Instruction('LBZ', True)
lbz_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,0,0,1,0]}, ('TODO'))
lbz_Instr.setCode(opCode,'execute')
lbz_Instr.addBehavior(IncrementPC, 'execute')
#lbz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lbz_Instr)
#LBZU
opCode = cxx_writer.writer_code.Code("""
""")
lbzu_Instr = trap.Instruction('LBZU', True)
lbzu_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,0,0,1,1]}, ('TODO'))
lbzu_Instr.setCode(opCode,'execute')
lbzu_Instr.addBehavior(IncrementPC, 'execute')
#lbz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lbzu_Instr)
#LBZUX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) rb);
//(int) ra = ea;
""")
lbzux_Instr = trap.Instruction('LBZUX', True)
lbzux_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,1,1,1,0,1,1,1]}, ('lbzux r', '%rt', ' r', '%ra', ' r', '%rb'))
lbzux_Instr.setCode(opCode,'execute')
lbzux_Instr.addBehavior(IncrementPC, 'execute')
#lbzux_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lbzux_Instr)
#LBZX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) rb);
//TODO (RT) ← 240 || MS(EA,1)
""")
lbzx_Instr = trap.Instruction('LBZX', True)
lbzx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,1,0,1,0,1,1,1]}, ('lbzx r', '%rt', ' r', '%ra', ' r', '%rb'))
lbzx_Instr.setCode(opCode,'execute')
lbzx_Instr.addBehavior(IncrementPC, 'execute')
#lbzx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lbzx_Instr)
#LHA
opCode = cxx_writer.writer_code.Code("""
//TODO (RT) ← exts(MS(EA,1));
""")
lha_Instr = trap.Instruction('LHA', True)
lha_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,1,0,1,0]}, ('TODO'))
lha_Instr.setCode(opCode,'execute')
lha_Instr.addBehavior(IncrementPC, 'execute')
#lbz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lha_Instr)
#LHAU
opCode = cxx_writer.writer_code.Code("""
//(int) ra = ea;
//TODO (RT) ← exts(MS(EA,2));
""")
lhau_Instr = trap.Instruction('LHAU', True)
lhau_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,1,0,1,1]}, ('TODO'))
lhau_Instr.setCode(opCode,'execute')
lhau_Instr.addBehavior(IncrementPC, 'execute')
#lbz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhau_Instr)
#LHAUX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra) + (int) rb);
//(int) ra = ea;
//TODO (RT) ← exts(MS(EA,2));
""")
lhaux_Instr = trap.Instruction('LHAUX', True)
lhaux_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,0,1,1,1,0,1,1,1]}, ('lhaux r', '%rt', ' r', '%ra', ' r', '%rb'))
lhaux_Instr.setCode(opCode,'execute')
lhaux_Instr.addBehavior(IncrementPC, 'execute')
#lhaux_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhaux_Instr)
#LHAX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) rb);
//TODO (RT) ← exts(MS(EA,2));
""")
lhax_Instr = trap.Instruction('LHAX', True)
lhax_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,0,1,0,1,0,1,1,1]}, ('lhax r', '%rt', ' r', '%ra', ' r', '%rb'))
lhax_Instr.setCode(opCode,'execute')
lhax_Instr.addBehavior(IncrementPC, 'execute')
#lhax_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhax_Instr)
#LHBRX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra|0) + (int) rb);
//TODO (RT) ← 160 || MS(EA +1,1) || MS(EA,1);
""")
lhbrx_Instr = trap.Instruction('LHBRX', True)
lhbrx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,1,0,0,0,1,0,1,1,0]}, ('lhbrx r', '%rt', ' r', '%ra', ' r', '%rb'))
lhbrx_Instr.setCode(opCode,'execute')
lhbrx_Instr.addBehavior(IncrementPC, 'execute')
#lhax_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhbrx_Instr)
#LHZ
opCode = cxx_writer.writer_code.Code("""
//TODO (RT) ← 160 || MS(EA,2);
""")
lhz_Instr = trap.Instruction('LHZ', True)
lhz_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,1,0,0,0]}, ('TODO'))
lhz_Instr.setCode(opCode,'execute')
lhz_Instr.addBehavior(IncrementPC, 'execute')
#lhz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhz_Instr)
#LHZU
opCode = cxx_writer.writer_code.Code("""
//(int) ra = ea;
//TODO (RT) ← 160 || MS(EA,2);
""")
lhzu_Instr = trap.Instruction('LHZU', True)
lhzu_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,1,0,0,1]}, ('TODO'))
lhzu_Instr.setCode(opCode,'execute')
lhzu_Instr.addBehavior(IncrementPC, 'execute')
#lhzu_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhzu_Instr)
#LHZUX
opCode = cxx_writer.writer_code.Code("""
ea = ((int) ra + (int) rb);
//(int) ra = ea;
//TODO (RT) ← 160 || MS(EA +1,1) || MS(EA,1);
""")
lhzux_Instr = trap.Instruction('LHZUX', True)
lhzux_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,0,0,0,1,1,0,1,1,1]}, ('lhzux r', '%rt', ' r', '%ra', ' r', '%rb'))
lhzux_Instr.setCode(opCode,'execute')
lhzux_Instr.addBehavior(IncrementPC, 'execute')
#lhzux_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhzux_Instr)
#LHZX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra |0) + (int) rb);
//(int) ra = ea;
//TODO (RT) ← 160 || MS(EA,2);
""")
lhzx_Instr = trap.Instruction('LHZX', True)
lhzx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,1,0,0,0,1,0,1,1,1]}, ('lhzx r', '%rt', ' r', '%ra', ' r', '%rb'))
lhzx_Instr.setCode(opCode,'execute')
lhzx_Instr.addBehavior(IncrementPC, 'execute')
#lhzx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lhzx_Instr)
#LMW
opCode = cxx_writer.writer_code.Code("""
//(int) r = ea;
//TODO 
//do while r ≤ 31
//if ((r ≠ RA) ∨ (r = 31)) then
//(GPR(r)) ← MS(EA,4)
//r ← r + 1
//EA ← EA + 4;
""")
lmw_Instr = trap.Instruction('LMW', True)
lmw_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,1,1,1,0]}, ('TODO'))
lmw_Instr.setCode(opCode,'execute')
lmw_Instr.addBehavior(IncrementPC, 'execute')
#lmw_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lmw_Instr)
#LSWI
opCode = cxx_writer.writer_code.Code("""
ea = ((int) ra |0);
//TODO LONG;
""")
lswi_Instr = trap.Instruction('LSWI', True)
lswi_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,0,0,1,0,1,0,1,0,1]}, ('lswi r', '%rt', ' r', '%ra', ' r', '%rb'))
lswi_Instr.setCode(opCode,'execute')
lswi_Instr.addBehavior(IncrementPC, 'execute')
#lhzx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lswi_Instr)
#LSWX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra |0) + (int) rb);
//TODO LONG;
""")
lswx_Instr = trap.Instruction('LSWX', True)
lswx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,0,0,0,0,1,0,1,0,1]}, ('lswx r', '%rt', ' r', '%ra', ' r', '%rb'))
lswx_Instr.setCode(opCode,'execute')
lswx_Instr.addBehavior(IncrementPC, 'execute')
#lswx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lswx_Instr)
#LWARX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra |0) + (int) rb);
//TODO RESERVE ← 1;
//(RT) ← MS(EA,4)
""")
lwarx_Instr = trap.Instruction('LWARX', True)
lwarx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,0,1,0,1,0,0]}, ('lwarx r', '%rt', ' r', '%ra', ' r', '%rb'))
lwarx_Instr.setCode(opCode,'execute')
lwarx_Instr.addBehavior(IncrementPC, 'execute')
#lwarx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lwarx_Instr)
#LWBRX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra |0) + (int) rb);
//TODO (RT) ← MS(EA+3,1) || MS(EA+2,1) || MS(EA+1,1) || MS(EA,1)
""")
lwbrx_Instr = trap.Instruction('LWBRX', True)
lwbrx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [1,0,0,0,0,1,0,1,1,0]}, ('lwbrx r', '%rt', ' r', '%ra', ' r', '%rb'))
lwbrx_Instr.setCode(opCode,'execute')
lwbrx_Instr.addBehavior(IncrementPC, 'execute')
#lwbrx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lwbrx_Instr)
#LWZ
opCode = cxx_writer.writer_code.Code("""
//TODO (rt) ← MS(EA,4)
""")
lwz_Instr = trap.Instruction('LWZ', True)
lwz_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,0,0,0,0]}, ('TODO'))
lwz_Instr.setCode(opCode,'execute')
lwz_Instr.addBehavior(IncrementPC, 'execute')
#lwz_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lwz_Instr)
#LWZU
opCode = cxx_writer.writer_code.Code("""
//(int) ra = ea;
//TODO (rt) ← MS(EA,4)
""")
lwzu_Instr = trap.Instruction('LWZU', True)
lwzu_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [1,0,0,0,0,1]}, ('TODO'))
lwzu_Instr.setCode(opCode,'execute')
lwzu_Instr.addBehavior(IncrementPC, 'execute')
#lwzu_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lwzu_Instr)
#LWZUX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra) + (int) rb);
//(int) ra = ea;
//TODO (rt) ← MS(EA,4)
""")
lwzux_Instr = trap.Instruction('LWZUX', True)
lwzux_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,1,1,0,1,1,1]}, ('lwzux r', '%rt', ' r', '%ra', ' r', '%rb'))
lwzux_Instr.setCode(opCode,'execute')
lwzux_Instr.addBehavior(IncrementPC, 'execute')
#lwzux_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lwzux_Instr)
#LWZX
opCode = cxx_writer.writer_code.Code("""
ea = (((int) ra) + (int) rb);
//TODO (rt) ← MS(EA,4)
""")
lwzx_Instr = trap.Instruction('LWZX', True)
lwzx_Instr.setMachineCode(oper_Xform_2, {'primary_opcode': [0,1,1,1,1,1],'xo': [0,0,0,0,0,1,0,1,1,1]}, ('lwzx r', '%rt', ' r', '%ra', ' r', '%rb'))
lwzx_Instr.setCode(opCode,'execute')
lwzx_Instr.addBehavior(IncrementPC, 'execute')
#lwzx_Instr.addTest({'bf': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 0xfd33, 'GPR[2]': 0xd6cc, 'GPR[3]': 0xfffff, 'PC':0x0, 'TARGET':0xffffffff}, {'GPR[3]': 0xffffd999, 'PC':0x4})
isa.addInstruction(lwzx_Instr)
#MACCHW
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
macchw_Instr = trap.Instruction('MACCHW', True)
macchw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,1,0,1,1,0,0]}, ('macchw r', '%rt', ' r', '%ra', ' r', '%rb'))
macchw_Instr.setCode(opCode,'execute')
macchw_Instr.addBehavior(IncrementPC, 'execute')
#macchw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(macchw_Instr)
#MACCHWS
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
macchws_Instr = trap.Instruction('MACCHWS', True)
macchws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,1,1,0,1,1,0,0]}, ('macchws r', '%rt', ' r', '%ra', ' r', '%rb'))
macchws_Instr.setCode(opCode,'execute')
macchws_Instr.addBehavior(IncrementPC, 'execute')
#macchw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(macchws_Instr)
#MACCHWSU
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
macchwsu_Instr = trap.Instruction('MACCHWSU', True)
macchwsu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,1,0,0,1,1,0,0]}, ('macchwsu r', '%rt', ' r', '%ra', ' r', '%rb'))
macchwsu_Instr.setCode(opCode,'execute')
macchwsu_Instr.addBehavior(IncrementPC, 'execute')
#macchwsu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(macchwsu_Instr)
#MACCHWU
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
macchwu_Instr = trap.Instruction('MACCHWU', True)
macchwu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,0,0,1,1,0,0]}, ('macchwu r', '%rt', ' r', '%ra', ' r', '%rb'))
macchwu_Instr.setCode(opCode,'execute')
macchwu_Instr.addBehavior(IncrementPC, 'execute')
#macchwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(macchwu_Instr)
#MACHHW
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
machhw_Instr = trap.Instruction('MACHHW', True)
machhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,1,0,1,1,0,0]}, ('machhw r', '%rt', ' r', '%ra', ' r', '%rb'))
machhw_Instr.setCode(opCode,'execute')
machhw_Instr.addBehavior(IncrementPC, 'execute')
#machhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(machhw_Instr)
#MACHHWS
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
machhws_Instr = trap.Instruction('MACHHWS', True)
machhws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,1,1,0,1,1,0,0]}, ('machhws r', '%rt', ' r', '%ra', ' r', '%rb'))
machhws_Instr.setCode(opCode,'execute')
machhws_Instr.addBehavior(IncrementPC, 'execute')
#machhws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(machhws_Instr)
#MACHHWSU
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
machhwsu_Instr = trap.Instruction('MACHHWSU', True)
machhwsu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,1,0,0,1,1,0,0]}, ('machhwsu r', '%rt', ' r', '%ra', ' r', '%rb'))
machhwsu_Instr.setCode(opCode,'execute')
machhwsu_Instr.addBehavior(IncrementPC, 'execute')
#machhws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(machhwsu_Instr)
#MACHHWU
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
machhwu_Instr = trap.Instruction('MACHHWU', True)
machhwu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,0,0,1,1,0,0]}, ('machhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
machhwu_Instr.setCode(opCode,'execute')
machhwu_Instr.addBehavior(IncrementPC, 'execute')
#machhu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(machhwu_Instr)
#MACLHW
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
maclhw_Instr = trap.Instruction('MACLHW', True)
maclhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,1,0,1,1,0,0]}, ('maclhw r', '%rt', ' r', '%ra', ' r', '%rb'))
maclhw_Instr.setCode(opCode,'execute')
maclhw_Instr.addBehavior(IncrementPC, 'execute')
#maclhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(maclhw_Instr)
#MACLHWS
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
maclhws_Instr = trap.Instruction('MACLHWS', True)
maclhws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,1,1,0,1,1,0,0]}, ('maclhws r', '%rt', ' r', '%ra', ' r', '%rb'))
maclhws_Instr.setCode(opCode,'execute')
maclhws_Instr.addBehavior(IncrementPC, 'execute')
#maclhws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(maclhws_Instr)
#MACLHWSU
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
maclhwsu_Instr = trap.Instruction('MACLHWSU', True)
maclhwsu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,1,0,0,1,1,0,0]}, ('maclhwsu r', '%rt', ' r', '%ra', ' r', '%rb'))
maclhwsu_Instr.setCode(opCode,'execute')
maclhwsu_Instr.addBehavior(IncrementPC, 'execute')
#maclhwsu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(maclhwsu_Instr)
#MACLHWU
opCode = cxx_writer.writer_code.Code("""
//TODO
""")
maclhwu_Instr = trap.Instruction('MACLHWU', True)
maclhwu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,0,0,1,1,0,0]}, ('maclhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
maclhwu_Instr.setCode(opCode,'execute')
maclhwu_Instr.addBehavior(IncrementPC, 'execute')
#maclhwsu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(maclhwu_Instr)
#MCRF
opCode = cxx_writer.writer_code.Code("""
m=(int) bfa;
n=(int) bf;
""")
mcrf_Instr = trap.Instruction('MCRF', True)
mcrf_Instr.setMachineCode(oper_XLform_3, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,0,0,0,0,0]}, ('TODO'))
mcrf_Instr.setCode(opCode,'execute')
mcrf_Instr.addBehavior(IncrementPC, 'execute')
#mcrf_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mcrf_Instr)
#MCRXR
opCode = cxx_writer.writer_code.Code("""
n=(int)bf;
//TODO
""")
mcrxr_Instr = trap.Instruction('MCRXR', True)
mcrxr_Instr.setMachineCode(oper_Xform_18, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,0,0,0,0,0,0]}, ('TODO'))
mcrxr_Instr.setCode(opCode,'execute')
mcrxr_Instr.addBehavior(IncrementPC, 'execute')
#mcrf_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mcrxr_Instr)
#MFCR
opCode = cxx_writer.writer_code.Code("""
n=(int)cr;
""")
mfcr_Instr = trap.Instruction('MFCR', True)
mfcr_Instr.setMachineCode(oper_Xform_6, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,1,0,0,1,1]}, ('TODO'))
mfcr_Instr.setCode(opCode,'execute')
mfcr_Instr.addBehavior(IncrementPC, 'execute')
#mfcr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mfcr_Instr)
#MFDCR
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mfdcr_Instr = trap.Instruction('MFDCR', True)
mfdcr_Instr.setMachineCode(oper_XFXForm_2, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,1,0,0,0,0,1,1]}, ('TODO'))
mfdcr_Instr.setCode(opCode,'execute')
mfdcr_Instr.addBehavior(IncrementPC, 'execute')
#mfdcr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mfdcr_Instr)
#MFMSR
opCode = cxx_writer.writer_code.Code("""
rt=(int)msr;
""")
mfmsr_Instr = trap.Instruction('MFMSR', True)
mfmsr_Instr.setMachineCode(oper_Xform_6, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,0,1,0,0,1,1]}, ('TODO'))
mfmsr_Instr.setCode(opCode,'execute')
mfmsr_Instr.addBehavior(IncrementPC, 'execute')
#mfcr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mfmsr_Instr)
#MFSPR
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mfspr_Instr = trap.Instruction('MFSPR', True)
mfspr_Instr.setMachineCode(oper_XFXForm_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,1,0,1,0,0,1,1]}, ('TODO'))
mfspr_Instr.setCode(opCode,'execute')
mfspr_Instr.addBehavior(IncrementPC, 'execute')
#mfspr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mfspr_Instr)
#MFTB
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mftb_Instr = trap.Instruction('MFTB', True)
mftb_Instr.setMachineCode(oper_XFXForm_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,1,1,1,0,0,1,1]}, ('TODO'))
mftb_Instr.setCode(opCode,'execute')
mftb_Instr.addBehavior(IncrementPC, 'execute')
#mftb_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mftb_Instr)
#MTCRF use rt inlue of rs
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mtcrf_Instr = trap.Instruction('MTCRF', True)
mtcrf_Instr.setMachineCode(oper_XFXForm_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,1,0,0,0,0]}, ('TODO'))
mtcrf_Instr.setCode(opCode,'execute')
mtcrf_Instr.addBehavior(IncrementPC, 'execute')
#mtcrf_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mtcrf_Instr)
#MTDCR
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mtdcr_Instr = trap.Instruction('MTDCR', True)
mtdcr_Instr.setMachineCode(oper_XFXForm_5, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,1,0,0,0,0,1,1]}, ('TODO'))
mtdcr_Instr.setCode(opCode,'execute')
mtdcr_Instr.addBehavior(IncrementPC, 'execute')
#mtdcr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mtdcr_Instr)
#MTMSR
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mtmsr_Instr = trap.Instruction('MTMSR', True)
mtmsr_Instr.setMachineCode(oper_Xform_15, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,1,0,0,1,0]}, ('TODO'))
mtmsr_Instr.setCode(opCode,'execute')
mtmsr_Instr.addBehavior(IncrementPC, 'execute')
#mtmsr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mtmsr_Instr)
#MTSPR
opCode = cxx_writer.writer_code.Code("""
//TODO;
""")
mtspr_Instr = trap.Instruction('MTSPR', True)
mtspr_Instr.setMachineCode(oper_XFXForm_4, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,1,0,1,0,0,1,1]}, ('TODO'))
mtspr_Instr.setCode(opCode,'execute')
mtspr_Instr.addBehavior(IncrementPC, 'execute')
#mtspr_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mtspr_Instr)

#MULCHW
opCode = cxx_writer.writer_code.Code("""
//(RT)0:31 ← (RA)16:31 x (RB)0:15 signed
int rt = (((int)ra & 0xffff0000) >> 16) * (((int)rb & 0x0000ffff) >> 0)
""")
mulchw_Instr = trap.Instruction('MULCHW', True)
mulchw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,1,0,1,0,0,0]}, ('mulchw r', '%rt', ' r', '%ra', ' r', '%rb'))
mulchw_Instr.setCode(opCode,'execute')
mulchw_Instr.addBehavior(IncrementPC, 'execute')
#mulchw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulchw_Instr)

#MULCHWU
opCode = cxx_writer.writer_code.Code("""
//(RT)0:31 ← (RA)16:31 x (RB)0:15 unsigned
int rt = (((int)ra & 0xffff0000) >> 16) * (((unsigned int)rb & 0x0000ffff) >> 0)
""")
mulchwu_Instr = trap.Instruction('MULCHWU', True)
mulchwu_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,0,0,1,0,0,0]}, ('mulchwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mulchwu_Instr.setCode(opCode,'execute')
mulchwu_Instr.addBehavior(IncrementPC, 'execute')
#mulchwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulchwu_Instr)

#MULHHW
opCode = cxx_writer.writer_code.Code("""
//(RT)0:31 ← (RA)0:15 x (RB)0:15 signed
int rt = (((int)ra & 0x0000ffff) >> 0) * (((int)rb & 0x0000ffff) >> 0)
""")
mulhhw_Instr = trap.Instruction('MULHHW', True)
mulhhw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,1,0,1,0,0,0]}, ('mulhhw r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhhw_Instr.setCode(opCode,'execute')
mulhhw_Instr.addBehavior(IncrementPC, 'execute')
#mulhhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhhw_Instr)

#MULHHWU
opCode = cxx_writer.writer_code.Code("""
//(RT)0:31 ← (RA)0:15 x (RB)0:15 unsigned
int rt = (((int)ra & 0x0000ffff) >> 0) * (((unsigned int)rb & 0x0000ffff) >> 0)
""")
mulhhwu_Instr = trap.Instruction('MULHHWU', True)
mulhhwu_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,0,0,1,0,0,0]}, ('mulhhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhhwu_Instr.setCode(opCode,'execute')
mulhhwu_Instr.addBehavior(IncrementPC, 'execute')
#mulhhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhhwu_Instr)

#MULHW
opCode = cxx_writer.writer_code.Code("""
//prod0:63 ← (RA) × (RB) signed
//(RT) ← prod0:31
long long prod = ((int)ra) * ((int)rb)
int rt = prod & 0x00000000ffffffff
""")
mulhw_Instr = trap.Instruction('MULHW', True)
mulhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,0,0,1,0,1,1]}, ('mulhw r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhw_Instr.setCode(opCode,'execute')
mulhw_Instr.addBehavior(IncrementPC, 'execute')
#mulhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhw_Instr)

#MULHWU
opCode = cxx_writer.writer_code.Code("""
//prod0:63 ← (RA) × (RB) unsigned
//(RT) ← prod0:31
long long prod = ((int)ra) * ((unsigned int)rb)
int rt = prod & 0x00000000ffffffff
""")
mulhwu_Instr = trap.Instruction('MULHWU', True)
mulhwu_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,0,1,1]}, ('mulhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mulhwu_Instr.setCode(opCode,'execute')
mulhwu_Instr.addBehavior(IncrementPC, 'execute')
#mulhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulhwu_Instr)

#MULLHW
opCode = cxx_writer.writer_code.Code("""
//(RT)0:31 ← (RA)16:31 x (RB)16:31 signed
int rt = ((int)ra & 0xffff0000) * ((int)rb & 0xffff0000) 
""")
mullhw_Instr = trap.Instruction('MULLHW', True)
mullhw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,1,0,1,0,0,0]}, ('mullhw r', '%rt', ' r', '%ra', ' r', '%rb'))
mullhw_Instr.setCode(opCode,'execute')
mullhw_Instr.addBehavior(IncrementPC, 'execute')
#mulhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mullhw_Instr)

#MULLHWU
opCode = cxx_writer.writer_code.Code("""
int rt = ((int)ra & 0xffff0000) * ((unsigned int)rb & 0xffff0000)
//(RT)0:31 ← (RA)16:31 x (RB)16:31 unsigned
""")
mullhwu_Instr = trap.Instruction('MULLHWU', True)
mullhwu_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,0,0,1,0,0,0]}, ('mullhwu r', '%rt', ' r', '%ra', ' r', '%rb'))
mullhwu_Instr.setCode(opCode,'execute')
mullhwu_Instr.addBehavior(IncrementPC, 'execute')
#mullhwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mullhwu_Instr)

#MULLI
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * exts(im); 
//prod0:47 ← (RA) × EXTS(IM) signed
//(RT) ← prod16:47
""")
mulli_Instr = trap.Instruction('MULLI', True)
mulli_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [0,0,0,1,1,1] }, ('mulli r', '%rt', ' r', '%ra'))
mulli_Instr.setCode(opCode,'execute')
mulli_Instr.addBehavior(IncrementPC, 'execute')
#mulli_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mulli_Instr)

#MULLW
opCode = cxx_writer.writer_code.Code("""
rt = (int)ra * (int)(signed)rb; 
//prod0:63 ← (RA) × (RB) signed
//(RT) ← prod32:63
""")
mullw_Instr = trap.Instruction('MULLW', True)
mullw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,0,1,1]}, ('mullw r', '%rt', ' r', '%ra', ' r', '%rb'))
mullw_Instr.setCode(opCode,'execute')
mullw_Instr.addBehavior(IncrementPC, 'execute')
#mullw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(mullw_Instr)

#NAND
opCode = cxx_writer.writer_code.Code("""
ra = !((int)rs && (int)rb); 
//(RA) ← ¬((RS) ∧ (RB))
""")
nand_Instr = trap.Instruction('NAND', True)
nand_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,1,1,0,0]}, ('nand r', '%rt', ' r', '%ra', ' r', '%rb'))
nand_Instr.setCode(opCode,'execute')
nand_Instr.addBehavior(IncrementPC, 'execute')
#nand_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nand_Instr)

#NEG
opCode = cxx_writer.writer_code.Code("""
rt = !((int)ra) + 1; 
//(RT) ← ¬(RA) + 1
""")
neg_Instr = trap.Instruction('NEG', True)
neg_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,0,1,0,0,0]}, ('neg r', '%rt', ' r', '%ra'))
neg_Instr.setCode(opCode,'execute')
neg_Instr.addBehavior(IncrementPC, 'execute')
#neg_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(neg_Instr)

#NMACCHW
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)0:15) signed
//temp0:32 ← nprod0:31 + (RT)
//(RT) ← temp1:32
""")
nmacchw_Instr = trap.Instruction('NMACCHW', True)
nmacchw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,0,1,0,1,1,1,0]}, ('nmacchw r', '%rt', ' r', '%ra', ' r', '%rb'))
nmacchw_Instr.setCode(opCode,'execute')
nmacchw_Instr.addBehavior(IncrementPC, 'execute')
#nmacchw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmacchw_Instr)

#NMACCHWS
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)0:15 signed
//temp0:32 ← nprod0:31 + (RT)
//if ((nprod0 = RT0) ∧ (RT0 ≠ temp1)) then (RT) ← (RT0 || 31(¬RT0))
//else (RT) ← temp1:32
""")
nmacchws_Instr = trap.Instruction('NMACCHWS', True)
nmacchws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,1,1,1,0,1,1,1,0]}, ('nmacchws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmacchws_Instr.setCode(opCode,'execute')
nmacchws_Instr.addBehavior(IncrementPC, 'execute')
#nmacchws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmacchws_Instr)

#NMACHHW
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)0:15 x (RB)0:15) signed
//temp0:32 ← nprod0:31 + (RT)
//(RT) ← temp1:32
""")
nmachhw_Instr = trap.Instruction('NMACHHW', True)
nmachhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,0,1,0,1,1,1,0]}, ('nmacchws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmachhw_Instr.setCode(opCode,'execute')
nmachhw_Instr.addBehavior(IncrementPC, 'execute')
#nmacchws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmachhw_Instr)

#NMACHHWS
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)0:15 x (RB)0:15) signed
//temp0:32 ← nprod0:31 + (RT)
//if ((nprod0 = RT0) ∧ (RT0 ≠ temp1)) then (RT) ← (RT0 || 31(¬RT0))
//else (RT) ← temp1:32
""")
nmachhws_Instr = trap.Instruction('NMACHHWS', True)
nmachhws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [0,0,1,1,0,1,1,1,0]}, ('nmacchws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmachhws_Instr.setCode(opCode,'execute')
nmachhws_Instr.addBehavior(IncrementPC, 'execute')
#nmacchws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmachhws_Instr)

#NMACLHW
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)16:31) signed
//temp0:32 ← nprod0:31 + (RT)
//(RT) ← temp1:32
""")
nmaclhw_Instr = trap.Instruction('NMACLHW', True)
nmaclhw_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,0,1,0,1,1,1,0]}, ('nmaclhw r', '%rt', ' r', '%ra', ' r', '%rb'))
nmaclhw_Instr.setCode(opCode,'execute')
nmaclhw_Instr.addBehavior(IncrementPC, 'execute')
#nmaclhw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmaclhw_Instr)

#NMACLHWS
opCode = cxx_writer.writer_code.Code("""
//nprod0:31 ← –((RA)16:31 x (RB)16:31) signed
//temp0:32 ← nprod0:31 + (RT)
//if ((nprod0 = RT0) ∧ (RT0 ≠ temp1)) then (RT) ← (RT0 || 31(¬RT0))
//else (RT) ← temp1:32
""")
nmaclhws_Instr = trap.Instruction('NMACLHWS', True)
nmaclhws_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,0,0,1,0,0], 'xo': [1,1,1,1,0,1,1,1,0]}, ('nmaclhws r', '%rt', ' r', '%ra', ' r', '%rb'))
nmaclhws_Instr.setCode(opCode,'execute')
nmaclhws_Instr.addBehavior(IncrementPC, 'execute')
#nmaclhws_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nmaclhws_Instr)

#NOR
opCode = cxx_writer.writer_code.Code("""
ra = !((int)rs || (int)rb)
//(RA) ← ¬((RS) ∨ (RB))
""")
nor_Instr = trap.Instruction('NOR', True)
nor_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,1,1,1,1,1,0,0]}, ('nor r', '%rt', ' r', '%ra', ' r', '%rb'))
nor_Instr.setCode(opCode,'execute')
nor_Instr.addBehavior(IncrementPC, 'execute')
#nor_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(nor_Instr)

#OR
opCode = cxx_writer.writer_code.Code("""
ra = ((int)rs || (int)rb)
//(RA) ← (RS) ∨ (RB)
""")
or_Instr = trap.Instruction('OR', True)
or_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,0,1,1,1,1,0,0]}, ('or r', '%rs', ' r', '%ra', ' r', '%rb'))
or_Instr.setCode(opCode,'execute')
or_Instr.addBehavior(IncrementPC, 'execute')
#or_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(or_Instr)

#ORC
opCode = cxx_writer.writer_code.Code("""
ra = ((int)rs || !(int)rb)
//(RA) ← (RS) ∨ ¬(RB)
""")
orc_Instr = trap.Instruction('ORC', True)
orc_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,0,0,1,1,1,0,0]}, ('orc r', '%rt', ' r', '%ra', ' r', '%rb'))
orc_Instr.setCode(opCode,'execute')
orc_Instr.addBehavior(IncrementPC, 'execute')
#orc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(orc_Instr)

#ORI
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ∨ (16:0 || IM)
""")
ori_Instr = trap.Instruction('ORI', True)
ori_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [0,1,1,0,0,0] }, ('ori r', '%rs', ' r', '%ra'))
ori_Instr.setCode(opCode,'execute')
ori_Instr.addBehavior(IncrementPC, 'execute')
#ori_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(ori_Instr)

#ORIS
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ∨ (IM || 16:0)
""")
oris_Instr = trap.Instruction('ORIS', True)
oris_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [0,1,1,0,0,1] }, ('oris r', '%rs', ' r', '%ra'))
oris_Instr.setCode(opCode,'execute')
oris_Instr.addBehavior(IncrementPC, 'execute')
#oris_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(oris_Instr)

#RFCI
opCode = cxx_writer.writer_code.Code("""
//(PC) ← (SRR2)
//(MSR) ← (SRR3)
""")
rfci_Instr = trap.Instruction('RFCI', True)
rfci_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,1,1,0,0,1,1] }, ())
rfci_Instr.setCode(opCode,'execute')
rfci_Instr.addBehavior(IncrementPC, 'execute')
#rfci_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rfci_Instr)

#RFI
opCode = cxx_writer.writer_code.Code("""
//(PC) ← (SRR0)
//(MSR) ← (SRR1)
""")
rfi_Instr = trap.Instruction('RFI', True)
rfi_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,0,0,1,1], 'xo': [0,0,0,0,1,1,0,0,1,0] }, ())
rfi_Instr.setCode(opCode,'execute')
rfi_Instr.addBehavior(IncrementPC, 'execute')
#rfi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rfi_Instr)

#RLWIMI
opCode = cxx_writer.writer_code.Code("""
//r ← ROTL((RS), SH)
//m ← MASK(MB, ME)
//(RA) ← (r ∧ m) ∨ ((RA) ∧ ¬m)
""")
rlwimi_Instr = trap.Instruction('RLWIMI', True)
rlwimi_Instr.setMachineCode(oper_Mform_2, {'primary_opcode': [0,1,0,1,0,0] }, ('rlwimi r', '%rs', ' r', '%ra'))
rlwimi_Instr.setCode(opCode,'execute')
rlwimi_Instr.addBehavior(IncrementPC, 'execute')
#rlwimi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rlwimi_Instr)

#RLWINM
opCode = cxx_writer.writer_code.Code("""
//r ← ROTL((RS), SH)
//m ← MASK(MB, ME)
//(RA) ← r ∧ m
""")
rlwinm_Instr = trap.Instruction('RLWINM', True)
rlwinm_Instr.setMachineCode(oper_Mform_2, {'primary_opcode': [0,1,0,1,0,1] }, ('rlwinm r', '%rs', ' r', '%ra'))
rlwinm_Instr.setCode(opCode,'execute')
rlwinm_Instr.addBehavior(IncrementPC, 'execute')
#rlwinm_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rlwinm_Instr)

#RLWNM
opCode = cxx_writer.writer_code.Code("""
//r ← ROTL((RS), SH)
//m ← MASK(MB, ME)
//(RA) ← r ∧ m
""")
rlwnm_Instr = trap.Instruction('RLWNM', True)
rlwnm_Instr.setMachineCode(oper_Mform_2, {'primary_opcode': [0,1,0,1,1,1] }, ('rlwnm r', '%rs', ' r', '%ra'))
rlwnm_Instr.setCode(opCode,'execute')
rlwnm_Instr.addBehavior(IncrementPC, 'execute')
#rlwnm_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(rlwnm_Instr)

#SC
opCode = cxx_writer.writer_code.Code("""
//(SRR1) ← (MSR)
//(SRR0) ← (PC)
//PC ← EVPR0:15 || 0x0C00
//(MSR[WE, EE, PR, DR, IR]) ← 0
""")
sc_Instr = trap.Instruction('SC', True)
sc_Instr.setMachineCode(oper_SCform, {'primary_opcode': [0,1,0,0,0,1] , '1':[1] }, ())
sc_Instr.setCode(opCode,'execute')
sc_Instr.addBehavior(IncrementPC, 'execute')
#sc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sc_Instr)

#SLW
opCode = cxx_writer.writer_code.Code("""
//n ← (RB)27:31
//r ← ROTL((RS), n)
//if (RB)26 = 0 then
//    m ← MASK(0, 31 – n)
//else
//    m ← 320
//(RA) ← r ∧ m
""")
slw_Instr = trap.Instruction('SLW', True)
slw_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,1,0,0,0] }, ('slw r', '%rs', ' r', '%ra', ' r', '%rb'))
slw_Instr.setCode(opCode,'execute')
slw_Instr.addBehavior(IncrementPC, 'execute')
#slw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(slw_Instr)

#SRAWI
opCode = cxx_writer.writer_code.Code("""
//n ← SH
//r ← ROTL((RS), 32 – n)
//m ← MASK(n, 31)
//s ← (RS)0
//(RA) ← (r ∧ m) ∨ (32s ∧ ¬m)
//XER[CA] ← s ∧ ((r ∧ ¬m)≠0)
""")
srawi_Instr = trap.Instruction('SRAWI', True)
srawi_Instr.setMachineCode(oper_Xform_12, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,0,0,1,1,1,0,0,0] }, ('srawi r', '%rs', ' r', '%ra', ' s', '%sh'))
srawi_Instr.setCode(opCode,'execute')
srawi_Instr.addBehavior(IncrementPC, 'execute')
#srawi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(srawi_Instr)

#SRW
opCode = cxx_writer.writer_code.Code("""
//n ← (RB)27:31
//r ← ROTL((RS), 32 – n)
//if (RB)26 = 0 then
//    m ← MASK(n, 31)
//else
//    m ← 320
//(RA) ← r ∧ m
""")
srw_Instr = trap.Instruction('SRW', True)
srw_Instr.setMachineCode(oper_Xform_7, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,0,0,1,1,0,0,0] }, ('srw r', '%rs', ' r', '%ra', ' r', '%rb'))
srw_Instr.setCode(opCode,'execute')
srw_Instr.addBehavior(IncrementPC, 'execute')
#srw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(srw_Instr)

#STB
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + EXTS(D)
//MS(EA, 1) ← (RS)24:31
""")
stb_Instr = trap.Instruction('STB', True)
stb_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,0,1,1,0] }, ('stb r', '%rs', ' r', '%ra'))
stb_Instr.setCode(opCode,'execute')
stb_Instr.addBehavior(IncrementPC, 'execute')
#stb_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stb_Instr)

#STBU
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA) + EXTS(D)
//MS(EA, 1) ← (RS)24:31
//(RA) ← EA
""")
stbu_Instr = trap.Instruction('STBU', True)
stbu_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,0,1,1,1] }, ('stbu r', '%rs', ' r', '%ra'))
stbu_Instr.setCode(opCode,'execute')
stbu_Instr.addBehavior(IncrementPC, 'execute')
#stbu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stbu_Instr)

#STBUX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA) + EXTS(D)
//MS(EA, 1) ← (RS)24:31
//(RA) ← EA
""")
stbux_Instr = trap.Instruction('STBUX', True)
stbux_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,1,1,0,1,1,1] }, ('stbux r', '%rs', ' r', '%ra' , ' r', '%rb'))
stbux_Instr.setCode(opCode,'execute')
stbux_Instr.addBehavior(IncrementPC, 'execute')
#stbux_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stbux_Instr)

#STBX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA, 1) ← (RS)24:31
""")
stbx_Instr = trap.Instruction('STBX', True)
stbx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,1,0,1,0,1,1,1] }, ('stbx r', '%rs', ' r', '%ra' , ' r', '%rb'))
stbx_Instr.setCode(opCode,'execute')
stbx_Instr.addBehavior(IncrementPC, 'execute')
#stbx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stbx_Instr)

#STH
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA, 1) ← (RS)24:31
""")
sth_Instr = trap.Instruction('STH', True)
sth_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,1,1,0,0]}, ('sth r', '%rs', ' r', '%ra' ))
sth_Instr.setCode(opCode,'execute')
sth_Instr.addBehavior(IncrementPC, 'execute')
#sth_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sth_Instr)

#STHBRX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA, 2) ← (RS)24:31 || (RS)16:23
""")
sthbrx_Instr = trap.Instruction('STHBRX', True)
sthbrx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1] , 'xo': [1,1,1,0,0,1,0,1,1,0] }, ('sthbrx r', '%rs', ' r', '%ra', ' r', '%rb' ))
sthbrx_Instr.setCode(opCode,'execute')
sthbrx_Instr.addBehavior(IncrementPC, 'execute')
#sthbrx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sthbrx_Instr)

#STHU
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA) + EXTS(D)
//MS(EA, 2) ← (RS)16:31
//(RA) ← EA
""")
sthu_Instr = trap.Instruction('STHU', True)
sthu_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,1,1,0,1]}, ('sthu r', '%rs', ' r', '%ra' ))
sthu_Instr.setCode(opCode,'execute')
sthu_Instr.addBehavior(IncrementPC, 'execute')
#sthu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sthu_Instr)

#STHUX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA, 2) ← (RS)24:31 || (RS)16:23
""")
sthux_Instr = trap.Instruction('STHUX', True)
sthux_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1] , 'xo': [0,1,1,0,1,1,0,1,1,1] }, ('sthux r', '%rs', ' r', '%ra', ' r', '%rb' ))
sthux_Instr.setCode(opCode,'execute')
sthux_Instr.addBehavior(IncrementPC, 'execute')
#sthux_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sthux_Instr)

#STHX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA, 2) ← (RS)16:31
""")
sthx_Instr = trap.Instruction('STHX', True)
sthx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1] , 'xo': [0,1,1,0,0,1,0,1,1,1] }, ('sthx r', '%rs', ' r', '%ra', ' r', '%rb' ))
sthx_Instr.setCode(opCode,'execute')
sthx_Instr.addBehavior(IncrementPC, 'execute')
#sthx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sthx_Instr)

#STMW
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + EXTS(D)
//r ← RS
//do while r ≤ 31
//  MS(EA, 4) ← (GPR(r))
//  r ← r + 1
//  EA ← EA + 4
""")
stmw_Instr = trap.Instruction('STMW', True)
stmw_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,1,1,1,1]}, ('stmw r', '%rs', ' r', '%ra' ))
stmw_Instr.setCode(opCode,'execute')
stmw_Instr.addBehavior(IncrementPC, 'execute')
#stmw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stmw_Instr)

#STSWI
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0)
//if NB = 0 then
   //n ← 32
//else
//   n ← NB
//r ← RS – 1
//i ← 0
//do while n > 0
//   if i = 0 then
//       r ← r + 1
//   if r = 32 then
//       r ← 0
//   MS(EA,1) ← (GPR(r)i:i+7)
//   i ← i + 8
//   if i = 32 then
//       i ← 0
//   EA ← EA + 1
//   n ← n – 1
""")
stswi_Instr = trap.Instruction('STSWI', True)
stswi_Instr.setMachineCode(oper_Xform_10, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,1,1,0,1,0,1,0,1] }, ('stswi r', '%rs', ' r', '%ra' ))
stswi_Instr.setCode(opCode,'execute')
stswi_Instr.addBehavior(IncrementPC, 'execute')
#stswi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stswi_Instr)

#STSWX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//n ← XER[TBC]
//r ← RS – 1
//i ← 0
//do while n > 0
//   if i = 0 then
//       r ← r + 1
//   if r = 32 then
//       r ← 0
//   MS(EA, 1) ← (GPR(r)i:i+7)
//   i ← i + 8
//   if i = 32 then
//       i ← 0
//   EA ← EA + 1
//   n ← n – 1
""")
stswx_Instr = trap.Instruction('STSWX', True)
stswx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,1,0,0,1,0,1,0,1] }, ('stswx r', '%rs', ' r', '%ra', ' r', '%rb' ))
stswx_Instr.setCode(opCode,'execute')
stswx_Instr.addBehavior(IncrementPC, 'execute')
#stswx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stswx_Instr)

#STW
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + EXTS(D)
//MS(EA, 4) ← (RS)
""")
stw_Instr = trap.Instruction('STW', True)
stw_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,0,1,0,0] }, ('stw r', '%rs', ' r', '%ra'))
stw_Instr.setCode(opCode,'execute')
stw_Instr.addBehavior(IncrementPC, 'execute')
#stw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stw_Instr)

#STWBRX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA, 4) ← (RS)24:31 || (RS)16:23 || (RS)8:15 || (RS)0:7
""")
stwbrx_Instr = trap.Instruction('STWBRX', True)
stwbrx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,1,0,0,1,0,1,1,0] }, ('stwbrx r', '%rs', ' r', '%ra', ' r', '%rb' ))
stwbrx_Instr.setCode(opCode,'execute')
stwbrx_Instr.addBehavior(IncrementPC, 'execute')
#stwbrx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stwbrx_Instr)

#STWCX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//if RESERVE = 1 then
//   MS(EA, 4) ← (RS)
//   RESERVE ← 0
//   (CR[CR0]) ← 20 || 1 || XERso
//else
//   (CR[CR0]) ← 20 || 0 || XERso
""")
stwcx_Instr = trap.Instruction('STWCX', True)
stwcx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,0,0,1,0,1,1,0] }, ('stwcx r', '%rs', ' r', '%ra', ' r', '%rb' ))
stwcx_Instr.setCode(opCode,'execute')
stwcx_Instr.addBehavior(IncrementPC, 'execute')
#stwcx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stwcx_Instr)

#STWU
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA) + EXTS(D)
//MS(EA, 4) ← (RS)
//(RA) ← EA
""")
stwu_Instr = trap.Instruction('STWU', True)
stwu_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [1,0,0,1,0,1] }, ('stwu r', '%rs', ' r', '%ra'))
stwu_Instr.setCode(opCode,'execute')
stwu_Instr.addBehavior(IncrementPC, 'execute')
#stwu_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stwu_Instr)

#STWUX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA) + (RB)
//MS(EA, 4) ← (RS)
//(RA) ← EA
""")
stwux_Instr = trap.Instruction('STWUX', True)
stwux_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,0,1,1,0,1,1,1] }, ('stwux r', '%rs', ' r', '%ra', ' r', '%rb' ))
stwux_Instr.setCode(opCode,'execute')
stwux_Instr.addBehavior(IncrementPC, 'execute')
#stwux_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stwux_Instr)

#STWX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//MS(EA,4) ← (RS)
""")
stwx_Instr = trap.Instruction('STWX', True)
stwx_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,0,0,1,0,1,1,1] }, ('stwx r', '%rs', ' r', '%ra', ' r', '%rb' ))
stwx_Instr.setCode(opCode,'execute')
stwx_Instr.addBehavior(IncrementPC, 'execute')
#stwx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(stwx_Instr)

#SUBF
opCode = cxx_writer.writer_code.Code("""
//(RT) ← ¬(RA) + (RB) + 1
""")
subf_Instr = trap.Instruction('SUBF', True)
subf_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,1,0,1,0,0,0] }, ('subf r', '%rt', ' r', '%ra', ' r', '%rb' ))
subf_Instr.setCode(opCode,'execute')
subf_Instr.addBehavior(IncrementPC, 'execute')
#subf_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(subf_Instr)

#SUBFC
opCode = cxx_writer.writer_code.Code("""
//(RT) ← ¬(RA) + (RB) + 1
""")
subfc_Instr = trap.Instruction('SUBFC', True)
subfc_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,1,0,0,0] }, ('subfc r', '%rt', ' r', '%ra', ' r', '%rb' ))
subfc_Instr.setCode(opCode,'execute')
subfc_Instr.addBehavior(IncrementPC, 'execute')
#subfc_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(subfc_Instr)

#SUBFE
opCode = cxx_writer.writer_code.Code("""
//(RT) ← ¬(RA) + (RB) + 1
""")
subfe_Instr = trap.Instruction('SUBFE', True)
subfe_Instr.setMachineCode(oper_X0form_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,0,1,0,0,0] }, ('subfe r', '%rt', ' r', '%ra', ' r', '%rb' ))
subfe_Instr.setCode(opCode,'execute')
subfe_Instr.addBehavior(IncrementPC, 'execute')
#subfe_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(subfe_Instr)

#SUBFIC
opCode = cxx_writer.writer_code.Code("""
//(RT) ← ¬(RA) + EXTS(IM) + 1
//if ¬(RA) + EXTS(IM) + 1 > 232 – 1 then
//                        u
//    XER[CA] ← 1
//else
//    XER[CA] ← 0
""")
subfic_Instr = trap.Instruction('SUBFIC', True)
subfic_Instr.setMachineCode(oper_Dform_1, {'primary_opcode': [0,0,1,0,0,0] }, ('subfic r', '%rt', ' r', '%ra'))
subfic_Instr.setCode(opCode,'execute')
subfic_Instr.addBehavior(IncrementPC, 'execute')
#subfic_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(subfic_Instr)

#SUBFME
opCode = cxx_writer.writer_code.Code("""
//(RT) ← ¬(RA) – 1 + XER[CA]
//if ¬(RA) + 0xFFFF FFFF + XER[CA] > 232 – 1 then
//                                 u
//    XER[CA] ← 1
//else
//    XER[CA] ← 0
""")
subfme_Instr = trap.Instruction('SUBFME', True) 
subfme_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,1,0,1,0,0,0] }, ('subfme r', '%rt', ' r', '%ra'))
subfme_Instr.setCode(opCode,'execute')
subfme_Instr.addBehavior(IncrementPC, 'execute')
#subfme_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(subfme_Instr)


#SUBFZE
opCode = cxx_writer.writer_code.Code("""
//(RT) ← ¬(RA) + XER[CA]
//if ¬(RA) + XER[CA] > 232 – 1 then
//                   u
//    XER[CA] ← 1
//else
//    XER[CA] ← 0
""")
subfze_Instr = trap.Instruction('SUBFZE', True) 
subfze_Instr.setMachineCode(oper_X0form_3, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,1,0,0,1,0,0,0] }, ('subfze r', '%rt', ' r', '%ra'))
subfze_Instr.setCode(opCode,'execute')
subfze_Instr.addBehavior(IncrementPC, 'execute')
#subfze_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(subfze_Instr)

#SYNC
opCode = cxx_writer.writer_code.Code("""
//None
""")
sync_Instr = trap.Instruction('SYNC', True) 
sync_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,1,0,1,0,1,1,0] }, ())
sync_Instr.setCode(opCode,'execute')
sync_Instr.addBehavior(IncrementPC, 'execute')
#sync_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(sync_Instr)


#TLBIA
opCode = cxx_writer.writer_code.Code("""
//None
""")
tlbia_Instr = trap.Instruction('TLBIA', True) 
tlbia_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,1,1,1,0,0,1,0] }, ())
tlbia_Instr.setCode(opCode,'execute')
tlbia_Instr.addBehavior(IncrementPC, 'execute')
#tlbia_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(tlbia_Instr)

#TLBRE
opCode = cxx_writer.writer_code.Code("""
//if WS4 = 1
//    (RT) ← TLBLO[(RA26:31)]
//else
//    (RT) ← TLBHI[(RA26:31)]
//    (PID) ← TID from TLB[(RA26:31)]
""")
tlbre_Instr = trap.Instruction('TLBRE', True) 
tlbre_Instr.setMachineCode(oper_Xform_4, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,1,0,1,1,0,0,1,0] }, ('tlbre r', '%rt', ' r', '%ra'))
tlbre_Instr.setCode(opCode,'execute')
tlbre_Instr.addBehavior(IncrementPC, 'execute')
#tlbre_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(tlbre_Instr)

#TLBSX
opCode = cxx_writer.writer_code.Code("""
//EA ← (RA|0) + (RB)
//if Rc = 1
//    CR[CR0]LT ← 0
//    CR[CR0]GT ← 0
//    CR[CR0]SO ← XER[SO]
//if Valid TLB entry matching EA and PID is in the TLB then
//    (RT) ← Index of matching TLB Entry
//    if Rc = 1
//        CR[CR0]EQ ← 1
//else
//    (RT) Undefined
//    if Rc = 1
//        CR[CR0]EQ ← 0
""")
tlbsx_Instr = trap.Instruction('TLBSX', True) 
tlbsx_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,1,0,0,1,0,0,1,0] }, ('tlbsx r', '%rt', ' r', '%ra', ' r', '%rb'))
tlbsx_Instr.setCode(opCode,'execute')
tlbsx_Instr.addBehavior(IncrementPC, 'execute')
#tlbsx_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(tlbsx_Instr)

#TLBSYNC
opCode = cxx_writer.writer_code.Code("""
//None
""")
tlbsync_Instr = trap.Instruction('TLBSYNC', True)
tlbsync_Instr.setMachineCode(oper_Xform_24, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,0,0,0,1,1,0,1,1,0] }, ())
tlbsync_Instr.setCode(opCode,'execute')
tlbsync_Instr.addBehavior(IncrementPC, 'execute')
#tlbsync_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(tlbsync_Instr)

#TLBWE
opCode = cxx_writer.writer_code.Code("""
//if WS4 = 1
//    TLBLO[(RA26:31)] ← (RS)
//else
//    TLBHI[(RA26:31)] ← (RS)
//    TID of TLB[(RA26:31)] ← (PID24:31)
""")
tlbwe_Instr = trap.Instruction('TLBWE', True) 
tlbwe_Instr.setMachineCode(oper_Xform_4, {'primary_opcode': [0,1,1,1,1,1], 'xo': [1,1,1,1,0,1,0,0,1,0] }, ('tlbwe r', '%rt', ' r', '%ra'))
tlbwe_Instr.setCode(opCode,'execute')
tlbwe_Instr.addBehavior(IncrementPC, 'execute')
#tlbre_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(tlbwe_Instr)

#TW
opCode = cxx_writer.writer_code.Code("""
//TODO Little complicated
""")
tw_Instr = trap.Instruction('TW', True) 
tw_Instr.setMachineCode(oper_Xform_1, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,0,0,0,0,1,0,0] }, ('tw r', '%rt', ' r', '%ra', ' r', '%rb'))
tw_Instr.setCode(opCode,'execute')
tw_Instr.addBehavior(IncrementPC, 'execute')
#tw_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(tw_Instr)

#TWI
opCode = cxx_writer.writer_code.Code("""
//TODO Little complicated
""")
twi_Instr = trap.Instruction('TWI', True) 
twi_Instr.setMachineCode(oper_Dform_7, {'primary_opcode': [0,0,0,0,1,1] }, ('twi r', '%to', ' r', '%ra'))
twi_Instr.setCode(opCode,'execute')
twi_Instr.addBehavior(IncrementPC, 'execute')
#twi_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(twi_Instr)

#WRTEE
opCode = cxx_writer.writer_code.Code("""
//MSR[EE] ← (RS)16
""")
wrtee_Instr = trap.Instruction('WRTEE', True)
wrtee_Instr.setMachineCode(oper_Xform_15, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,1,0,0,0,0,0,1,1] }, ('wrtee r', '%rs'))
wrtee_Instr.setCode(opCode,'execute')
wrtee_Instr.addBehavior(IncrementPC, 'execute')
#wrtee_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(wrtee_Instr)

#WRTEEI
opCode = cxx_writer.writer_code.Code("""
//MSR[EE] ← E
""")
wrteei_Instr = trap.Instruction('WRTEEI', True)
wrteei_Instr.setMachineCode(oper_Xform_25, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,0,0,1,1,1,0,0,1,1] }, ())
wrteei_Instr.setCode(opCode,'execute')
wrteei_Instr.addBehavior(IncrementPC, 'execute')
#wrteei_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(wrteei_Instr)

#XOR
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ⊕ (RB)
""")
xor_Instr = trap.Instruction('XOR', True)
xor_Instr.setMachineCode(oper_Xform_9, {'primary_opcode': [0,1,1,1,1,1], 'xo': [0,1,0,0,1,1,1,1,0,0] }, ('xor r', '%rs', ' r', '%ra', ' r', '%rb'))
xor_Instr.setCode(opCode,'execute')
xor_Instr.addBehavior(IncrementPC, 'execute')
#xor_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(xor_Instr)

#XORI
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ⊕ (160 || IM)
""")
xori_Instr = trap.Instruction('XORI', True)
xori_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [0,1,1,0,1,0] }, ('xori r', '%rs', ' r', '%ra'))
xori_Instr.setCode(opCode,'execute')
xori_Instr.addBehavior(IncrementPC, 'execute')
#xori_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(xori_Instr)

#XORIS
opCode = cxx_writer.writer_code.Code("""
//(RA) ← (RS) ⊕ (IM || 16
//                       0)
""")
xoris_Instr = trap.Instruction('XORIS', True)
xoris_Instr.setMachineCode(oper_Dform_3, {'primary_opcode': [0,1,1,0,1,1] }, ('xoris r', '%rs', ' r', '%ra'))
xoris_Instr.setCode(opCode,'execute')
xoris_Instr.addBehavior(IncrementPC, 'execute')
#xoris_Instr.addTest({'rt': 3, 'ra': 1, 'rb': 2}, {'GPR[1]': 4, 'GPR[2]': 6, 'GPR[3]': 0xfffff, 'PC':0x0, 'GPR[4]':0x00000000, 'GPR[5]':0xffffffff}, {'GPR[3]': 10, 'PC':0x4, 'GPR[4]':0x00000000})
isa.addInstruction(xoris_Instr)