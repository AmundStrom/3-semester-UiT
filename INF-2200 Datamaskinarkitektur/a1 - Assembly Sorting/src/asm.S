#include "asmdef.h"

DECLARE_GLOBAL(asm_function)


################################################################################
# name:         asm_function
# action:       cocktail sort
# in:           int array[], int length(of array)
#
# out:			
# modifies:		int array[]
# notes:
################################################################################

FUNC(asm_function):
	pushl %ebp				# Preserve old stackframe
	movl %esp, %ebp			# Create new stackframe

	pushl %eax				# Preserve callee saved registers,
	pushl %ebx				# so we can use them

	# NB! MOST OF THESE REGISTERS ARE EMPTY TO BEGIN WITH
	pushl %ecx
	pushl %edx
	pushl %edi
	pushl %esi

	movl 8(%ebp), %eax		# EAX holds the array
	movl $0, %ebx			# EBX will be temp
	movl $0, %ecx			# ECX will be i
	movl $0, %edx			# EDX will be a second temp
	movl $0, %edi			# EDI will be left side of array
	movl 12(%ebp), %esi		# ESI will be right side of array
	decl %esi

# Start of while-loop
while:

##### Start of for-loop
	movl %edi, %ecx			# i = left
loop_start_1:
	cmpl %esi, %ecx	 		# if ECX(i)...
	jge loop_end_1			# ...is greater or equal to ESI(right), jump

	movl (%eax, %ecx, 4), %edx		# temp(EDX) = a[i]
	movl 4(%eax, %ecx, 4), %ebx		# temp(EBX) = a[i+1]
	cmpl %ebx, %edx					# if EDX(a[i])...
	jle if_end_1					# ...is less or equal to EBX(a[i+1]), jump
	movl %ebx, (%eax, %ecx, 4)		# a[i] = temp(EBX)
	movl %edx, 4(%eax, %ecx, 4)		# a[i+1] = temp(EDX)
if_end_1:

	incl %ecx				# i++
	jmp loop_start_1		# Jump to start of for-loop
loop_end_1:
##### End of for-loop

decl %esi					# right--

##### Start of for-loop
	movl %esi, %ecx			# i = right
loop_start_2:
	cmpl %edi, %ecx	 		# if ECX(i)...
	jle loop_end_2			# ...is less or equal to EDI(left), jump

	movl (%eax, %ecx, 4), %edx		# temp(EDX) = a[i]
	movl -4(%eax, %ecx, 4), %ebx	# temp(EBX) = a[i-1]
	cmpl %edx, %ebx					# if EBX(a[i-1])...
	jle if_end_2					# ...is less or equal to EDX(a[i]), jump
	movl %ebx, (%eax, %ecx, 4)		# a[i] = temp(EBX)
	movl %edx, -4(%eax, %ecx, 4)	# a[i-1] = temp(EDX)
if_end_2:

	decl %ecx				# i--
	jmp loop_start_2		# Jump to start of For-loop
loop_end_2:
##### End of for-loop

incl %edi					# left++

cmpl %esi, %edi				# if EDI(left)...
jle while					# ...is less or equal to ESI(right), jump
# End of while-loop

	popl %esi				# Restore callee saved registers
	popl %edi
	popl %edx
	popl %ecx
	popl %ebx
	popl %eax
	popl %ebp				# Restore caller's stack frame
	ret