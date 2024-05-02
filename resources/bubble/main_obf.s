	.file	"main.c"
	.option	pic
	.attribute	arch, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.section	.text
	.section	.rodata
	.align	3
.LC0:
	.string	"Count: "
	.align	3
.LC1:
	.string	"%i"
	.size	main, .-main
	.section	.text
	.align	1
	.globl	main
	.type	main, @function
.LBLL0_2:

	lw	a5, -36(s0)
	slli	a5, a5, 2
	mv	a0, a5
	call	malloc@plt
	mv	a5, a0
	j	.LBLL0_3
.LBLL1_6:

	sw	a4, 0(a5)
	lw	a5, -20(s0)
	addiw	a5, a5, 1
	sw	a5, -20(s0)
	j	.L2
.LBLL0_3:

	sd	a5, -32(s0)
	sw	zero, -20(s0)
	j	.L2
	j	.L3
main:

	addi	sp, sp, -48
	sd	ra, 40(sp)
	sd	s0, 32(sp)
	addi	s0, sp, 48
	lla	a0, .LC0
	j	.LBLL0_1
.LBLL3_9:

	mv	a1, a5
	ld	a0, -32(s0)
	call	bubble_sort@plt
	lw	a5, -36(s0)
	mv	a1, a5
	j	.LBLL3_10
.LBLL3_10:

	ld	a0, -32(s0)
	call	print_mas@plt
	call	getchar@plt
	call	getchar@plt
	nop	
	j	.LBLL3_11
.LBLL0_1:

	call	printf@plt
	addi	a5, s0, -36
	mv	a1, a5
	lla	a0, .LC1
	call	__isoc99_scanf@plt
	j	.LBLL0_2
.LBLL1_5:

	ld	a4, -32(s0)
	add	a5, a4, a5
	li	a4, 50
	remw	a4, a3, a4
	sext.w	a4, a4
	j	.LBLL1_6
.L3:

	call	rand@plt
	mv	a5, a0
	mv	a3, a5
	lw	a5, -20(s0)
	slli	a5, a5, 2
	j	.LBLL1_5
.L2:

	lw	a4, -36(s0)
	lw	a5, -20(s0)
	sext.w	a5, a5
	blt	a5, a4, .L3
	j	.LBL3_0
.LBL3_0:

	lw	a5, -36(s0)
	mv	a1, a5
	ld	a0, -32(s0)
	call	print_mas@plt
	lw	a5, -36(s0)
	j	.LBLL3_9
.LBLL3_11:

	ld	ra, 40(sp)
	ld	s0, 32(sp)
	addi	sp, sp, 48
	jr	ra
	.size	main, .-main
	.section	.note.GNU-stack
