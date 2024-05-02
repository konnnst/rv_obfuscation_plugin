	.file	"hw.c"
	.option	pic
	.attribute	arch,"rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"
	.attribute	unaligned_access,0
	.attribute	stack_align,16
	.section	.text
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align	3
.LC0:
	.string	"Hello world! "
	.section	.text.startup,"ax",@progbits
	.align	1
	.globl	main
	.type	main,@function
.LBL2_0:
	ld	s0,16(sp)
	ld	ra,24(sp)
	ld	s1,8(sp)
	j	.LBLL2_4
.LBLL0_1:
	sd	ra,24(sp)
	li	s0,5
	lla	s1,.LC0
	j	.L2
.L2:
	addiw	s0,s0,-1
	mv	a0,s1
	call	printf@plt
	bne	s0,zero,.L2
	j	.LBL2_0
main:
	addi	sp,sp,-32
	sd	s0,16(sp)
	sd	s1,8(sp)
	j	.LBLL0_1
.LBLL2_4:
	li	a0,10
	addi	sp,sp,32
	tail	putchar@plt
	.size	main,.-main
	.section	.note.GNU-stack,"",@progbits
