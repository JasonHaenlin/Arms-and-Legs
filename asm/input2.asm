.data
	A: .word 0xf0
	B: .word 0xf0
	PRODUIT: .word 0x00
.end

.text
	LDR R0,A
	LDR R1,B
	LDR R2,B
	MOV R3,#0
	MOV R4,#1 
	MOV R5,#0
	
	CMP R0,R3
	BE fin
	CMP R1,R3
	BE fin
  
  again:
	ADD R5,R5,R0
	SUB R2,R2,R4
	CMP R2,R3
	BNE again
	
  fin:
	STR R5,PRODUIT
.end