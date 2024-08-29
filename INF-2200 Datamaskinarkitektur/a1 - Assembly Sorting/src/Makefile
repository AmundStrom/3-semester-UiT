# Makefile for compiling and linking .C files with asm files

# -m32 compiles .C to 32bit assembly (Needs package gcc-multilib)
# -masm=att Compiles .C with at&t assembly syntax

CC = gcc -g
CFLAGS = -m32 -masm=att

all: program

# To change optimization levels on .C file change -O0 to either -O1, -O2, -O3
# Optimization levels GCC https://gcc.gnu.org/onlinedocs/gnat_ugn/Optimization-Levels.html
main: main.c Makefile
	$(CC) $(CFLAGS) -O3 -S -o $@.s $<

# asm.S and main has to exist before executing compilation targets
program: asm.S asmqs.S main
	$(CC) $(CFLAGS) -E $< > $@_pp.s
	$(CC) $(CFLAGS) -E $(word 2,$^) > $@_ppqs.s
	$(CC) $(CFLAGS) main.s $@_pp.s $@_ppqs.s -o $@
# Linje 19 skal definere compilerings flaggan til asmqs.S, kunne skrevet asmqs.S istedenfor $(word 2,$^)
# Å legge til en ekstra assembly fil dro mæ lengre ned i kaninhullet enn alice i eventryland, skjønte til slutt av det er _pp.s som brukes til å kompilere programmet.

clean: 
	rm -rf *.o program program_pp.s program_ppqs.s main.s
