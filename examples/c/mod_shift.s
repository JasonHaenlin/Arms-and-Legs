	.arch armv5t
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 2
	.eabi_attribute 30, 6
	.eabi_attribute 34, 0
	.eabi_attribute 18, 4
	.file	"mod_shift.c"
	.text
	.align	2
	.global	main
	.syntax unified
	.arm
	.fpu softvfp
	.type	main, %function
main:
	@ args = 0, pretend = 0, frame = 16
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!
	add	fp, sp, #0
	sub	sp, sp, #20
	mov	r3, #10
	str	r3, [fp, #-16]
	mov	r3, #16
	str	r3, [fp, #-12]
	mov	r3, #4
	str	r3, [fp, #-8]
	mov	r3, #1
	str	r3, [fp, #-20]
	ldr	r3, [fp, #-12]
	and	r3, r3, #1
	cmp	r3, #0
	bne	.L2
	ldr	r2, [fp, #-16]
	ldr	r3, [fp, #-8]
	lsl	r3, r2, r3
	str	r3, [fp, #-20]
	b	.L3
.L2:
	ldr	r3, [fp, #-16]
	ldr	r2, [fp, #-12]
	mul	r1, r2, r3
	str	r1, [fp, #-20]
.L3:
	ldr	r3, [fp, #-20]
	mov	r0, r3
	add	sp, fp, #0
	@ sp needed
	ldr	fp, [sp], #4
	bx	lr
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.3.0-27ubuntu1~18.04) 7.3.0"
	.section	.note.GNU-stack,"",%progbits
