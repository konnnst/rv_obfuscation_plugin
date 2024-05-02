CC=gcc
RV=riscv64-linux-gnu-gcc

all: bubel bubel_rv clean

bubel: bubble.o main.o
	cc bubble.o main.o -o bubel

bubble.o: bubble.c
	cc -c bubble.c -o bubble.o

main.o: main.c
	cc -c main.c -o main.o

bubel_rv: bubble_rv.o main_rv.o
	$(RV) bubble_rv.o main_rv.o -o bubel_rv

bubble.s: bubble.c
	$(RV) -S bubble.c

main.s: main.c
	$(RV) -S main.c

bubble_rv.o: bubble.s
	$(RV) bubble.s -o bubble_rv.o

main_rv.o: main.s
	$(RV) main.s -o main_rv.o

clean:
	rm *.o
