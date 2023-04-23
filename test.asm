DATA segment
	Var db 0fLh
	Var2 dw 0340h
	Var3 dd 0a7f5ch
	Var4 db 01b
	Var5 db 5
DATA ends
CODE Segment
label1 :
	stosb
	push ax

	mul Var[si]
    mul Var1[si]

	add ax, Var2[di]

	and ax, bx
    and ax, bl

	cmp Var[bx], bx

	Jne label2
	
label2:
	
	mov ax , ES:Var2[si]
    mov ax , KS:Var2[si]

    sub al, ( 124 + 23 * ( 98 / 45 ) - 62 )
   
	test Var[bx, 01b
	
	Jne label
	
CODE ends
END
