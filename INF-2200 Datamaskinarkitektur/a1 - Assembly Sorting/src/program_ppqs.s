# 1 "asmqs.S"
# 1 "/home/amund/Docs/INF-2200-1 22H Datamaskinarkitektur/assignment-1-amund/src//"
# 1 "<built-in>"
# 1 "<command-line>"
# 31 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 32 "<command-line>" 2
# 1 "asmqs.S"
# 1 "asmdef.h" 1
# 2 "asmqs.S" 2

.globl asmqs_function; .type asmqs_function, @function


################################################################################
# name: asmqs_function
# action: quicksort
# in: int array[]

# out:
# modifies: int array[]
# notes: only in test atm.
################################################################################

asmqs_function:

    pushl %ebp # Pushing Base Pointer on the stack
    movl %esp, %ebp # Copy current stack pointer to EBP, meaning we can now access base pointer and function arguments no matter what is pushed on stack. We have "bookmarked" the stack, and a new stackframe is "created"

    pushl %ebx # Values that need to be preserved, EBX assuming we are running PIC code, which i am guessing the gcc compiler is using, as it appears to be normal.
    pushl %esi # Registers ESI and EDI also, according to x86 calling convention.
    pushl %edi

    movl 8(%ebp), %eax # Moves the address of the first element in the array to EAX

    call _qsPreFirst

    jmp _exit # Jump to exit

_qsPreFirst:

    movl 12(%ebp), %esi # Moves the correct low and high parameters into the right registers, first time
    movl 16(%ebp), %edi

    call _quicksortCheck
    ret
# 8 2 4 8 9 8 14 2 3 1 13 14 0 0 6
# 2 8 4 8 9 8 ...
# 2 4 8 8 9 8 14 2 3 ...
# 2 4 2 8 9 8 14 8 3 1 13 ...
# 2 4 2 3 9 8 14 8 8 1 13 ...
# 2 4 2 3 1 8 14 8 8 9 13 14 0 0 6
# 2 4 2 3 1 0 14 8 8 9 13 14 8 0 6
# 2 4 2 3 1 0 0 8 8 9 13 14 8 14 6
# 2 4 2 3 1 0 0 6 8 9 13 14 8 14 6
_quicksortCheck:

    cmpl %edi, %esi # Compares low to high
    jl _quicksortMain

    ret


# array is ALWAYS in EAX, low in ESI and high in EDI
_partition:

    movl (%eax, %edi, 4), %edx # EDX now contains the pivot, located at array[high]
    movl %esi, %ecx # ECX now contains ECX = low
    decl %ecx # Decrements so that it starts one behind, needs this to work, since i = low - 1
    pushl %esi # Pushing 'low' on stack, not needed until return
    call _partForLoop
    popl %esi # Pops 'low' back from stack into ESI
    ret # ECX now contains return value, i+1, or the new pivot



_partForLoop:

    # Here we use ESI as 'j', ECX as 'i', EDI as 'high' and EDX as 'pivot', EBX is the only free one here, so pushes need to happen

    # Way out of for loop
    cmpl %edi, %esi
    jg _partForLoopRet

    movl (%eax, %esi, 4), %ebx # EBX now contains array[j]

    cmpl %edx, %ebx # jump to If statement body
    jl _partForLoopIfBody

    incl %esi # j++
    jmp _partForLoop # Jump to start of for loop



_partForLoopIfBody:

    incl %ecx # i++

    # Here we are swapping

    pushl %ebx # Pushing EBX containing array[j] on stack
    movl (%eax, %ecx, 4), %ebx # Retreiving array[i], putting it in EBX
    movl %ebx, (%eax, %esi, 4) # Storing array[i] on array[j]

    popl %ebx # Popping array[j] from stack into EBX
    movl %ebx, (%eax, %ecx, 4) # EBX contains array[j], and storing it in array[i]

    incl %esi # j++
    jmp _partForLoop



_partForLoopRet:

    # Going in EBX is now considered garbage and free to use. ESI, or 'j' is not used anymore, and can be used.

    incl %ecx
    movl (%eax, %ecx, 4), %ebx # EBX and ESI now contain array[i+1] and array[high] respectively
    movl (%eax, %edi, 4), %esi

    movl %ebx, (%eax, %edi, 4) # array[i+1] and array[high] switch places
    movl %esi, (%eax, %ecx, 4)

    ret # We return to caller, to _partition, ECX now contains i+1


_quicksortMain:

    call _partition # Calls partition, pushin the current EIP pointer plus ONE instruction (I believe), so that it will return to the NEXT instruction
                                # When returning, ECX should contain the new pivot
    pushl %edi # Pushing EDI on stack, it contains 'high' and we're going to need it when we return from however many function calls are left
    movl %ecx, %edi # EDI now contains the new 'high', the pivot we find from _partition,
    decl %edi # pi-1

    call _quicksortCheck

    movl %edi, %esi # ESI now contains EDI, what used to be pi-1, this should be
    incl %esi
    incl %esi
    popl %edi # Recover previous 'high' into EDI

    call _quicksortCheck

    ret

_correctNegativeHigh:
    # In case, which does happen, that partition returns 0, the high for the next partition will be < 0, and give garbage values

    movl %edi, %ecx

    ret


_exit:

    popl %edi # Restore callee saved registers, including base pointer.
    popl %esi
    popl %ebx

    popl %ebp
    ret
