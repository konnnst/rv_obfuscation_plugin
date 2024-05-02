	.file	"bubble.c"
	.option	pic
	.attribute	arch,"rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0"
	.attribute	unaligned_access,0
	.attribute	stack_align,16
	.section	.text
	.align	1
	.globl	swap
	.type	swap,@function
swap:
	lw	a4,0(a1)
	lw	a5,0(a0)
	sw	a4,0(a0)
	j	.LBLL0_1
.LBLL0_1:
	sw	a5,0(a1)
	ret	
	.size	swap,.-swap
	.align	1
	.globl	bubble_sort
	.type	bubble_sort,@function
.L7:
	lw	a4,0(a5)
	lw	a3,4(a5)
	ble	a4,a3,.L6
	j	.LBL6_1
.LBL2_1:
	li	a5,1
	beq	a1,a5,.L3
	j	.LBL3_1
.LBL3_1:
	addiw	a2,a1,-2
	slli	a5,a2,32
	srli	a2,a5,30
	j	.LBLL3_3
.L8:
	mv	a5,a0
	j	.L7
.LBL6_1:
	sw	a3,0(a5)
	sw	a4,4(a5)
	j	.L6
.LBL8_1:
	addiw	a6,a6,1
	bne	a1,a6,.L8
	j	.L3
.L6:
	addi	a5,a5,4
	bne	a5,a2,.L7
	j	.LBL8_1
bubble_sort:
	ble	a1,zero,.L3
	j	.LBL2_1
.LBLL3_3:
	addi	a5,a0,4
	add	a2,a2,a5
	li	a6,0
	j	.L8
.L3:
	ret	
	.size	bubble_sort,.-bubble_sort
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align	3
.LC0:
	.string	"%i "
	.section	.text
	.align	1
	.globl	print_mas
	.type	print_mas,@function
.LBL13_10:
	ld	s0,16(sp)
	ld	ra,24(sp)
	ld	s1,8(sp)
	j	.LBLL13_7
.LBLL13_7:
	ld	s2,0(sp)
	li	a0,10
	addi	sp,sp,32
	j	.LBLL13_8
.L13:
	lw	a1,0(s0)
	mv	a0,s2
	addi	s0,s0,4
	j	.LBLL12_5
.LBLL11_3:
	mv	s0,a0
	add	s1,a0,a1
	lla	s2,.LC0
	j	.L13
.LBLL11_2:
	sd	s1,8(sp)
	sd	s2,0(sp)
	sd	ra,24(sp)
	j	.LBLL11_3
print_mas:
	ble	a1,zero,.L16
	j	.LBL11_10
.LBLL12_5:
	call	printf@plt
	bne	s0,s1,.L13
	j	.LBL13_10
.LBLL13_8:
	tail	putchar@plt
	j	.L16
.LBL11_10:
	addi	sp,sp,-32
	slli	a1,a1,2
	sd	s0,16(sp)
	j	.LBLL11_2
.L16:
	li	a0,10
	tail	putchar@plt
	.size	print_mas,.-print_mas
	.section	.rodata.str1.8
	.align	3
.LC1:
	.string	"Count: "
	.align	3
.LC2:
	.string	"%i"
	.section	.text.startup,"ax",@progbits
	.align	1
	.globl	main
	.type	main,@function
.LBL16_15:
	mv	s1,a0
	li	s0,0
	li	s3,50
	j	.L21
.LBLL18_14:
	call	getc@plt
	ld	a0,0(s0)
	call	getc@plt
	j	.LBLL18_15
.LBLL15_5:
	mv	s4,a0
	ble	s2,zero,.L20
	j	.LBL16_15
.LBLL17_9:
	bgt	s2,s0,.L21
	j	.L20
main:
	addi	sp,sp,-64
	lla	a0,.LC1
	sd	ra,56(sp)
	j	.LBLL15_1
.LBLL15_1:
	sd	s2,32(sp)
	sd	s4,16(sp)
	sd	s0,48(sp)
	j	.LBLL15_2
.LBLL15_4:
	lw	s2,12(sp)
	slli	a0,s2,2
	call	malloc@plt
	j	.LBLL15_5
.L20:
	mv	a1,s2
	mv	a0,s4
	call	print_mas
	j	.LBLL18_11
.LBLL15_2:
	sd	s1,40(sp)
	sd	s3,24(sp)
	call	printf@plt
	j	.LBLL15_3
.LBLL18_17:
	addi	sp,sp,64
	jr	ra
	j	.LBL19_15
.LBLL18_12:
	mv	a1,s1
	call	bubble_sort
	mv	a1,s1
	j	.LBLL18_13
.LBLL18_16:
	ld	s2,32(sp)
	ld	s3,24(sp)
	ld	s4,16(sp)
	j	.LBLL18_17
.L21:
	call	rand@plt
	remw	a0,a0,s3
	lw	s2,12(sp)
	j	.LBLL17_8
.LBLL18_11:
	lw	s1,12(sp)
	mv	a0,s4
	la	s0,stdin
	j	.LBLL18_12
.LBLL18_15:
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	j	.LBLL18_16
.LBLL17_8:
	addiw	s0,s0,1
	addi	s1,s1,4
	sw	a0,-4(s1)
	j	.LBLL17_9
.LBLL15_3:
	addi	a1,sp,12
	lla	a0,.LC2
	call	__isoc99_scanf@plt
	j	.LBLL15_4
.LBLL18_13:
	mv	a0,s4
	call	print_mas
	ld	a0,0(s0)
	j	.LBLL18_14
.LBL19_15:
	.size	main,.-main
	.section	.note.GNU-stack,"",@progbits
