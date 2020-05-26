assume cs:code,ds:data,ss:stack,es:extended

extended segment
	db 1024 dup (0)
extended ends

stack segment
	db 1024 dup (0)
stack ends

data segment
	_buff_p db 256 dup (24h)
	_buff_s db 256 dup (0)
	_msg_p db 0ah,'Output:',0
	_msg_s db 0ah,'Input:',0
	_i dw 0
	_N dw 0
	_sum dw 0
	_choice dw 0
data ends

code segment
start:	mov ax,extended
	mov es,ax
	mov ax,stack
	mov ss,ax
	mov sp,1024
	mov bp,sp
	mov ax,data
	mov ds,ax

_1:	mov ax,0
	mov ds:[_sum],ax
_2:	mov ax,0
	mov ds:[_choice],ax
_3:	call _read
	mov es:[0],ax
_4:	mov ax,es:[0]
	mov ds:[_N],ax
_5:	call _read
	mov es:[2],ax
_6:	mov ax,es:[2]
	mov ds:[_choice],ax
_7:	mov dx,1
	mov ax,ds:[_choice]
	cmp ax,1
	je _7_n
	mov dx,0
_7_n:	mov es:[4],dx
_8:	mov ax,es:[4]
	cmp ax,0
	jne _8_n
	jmp far ptr _23
_8_n:	nop
_9:	mov ax,1
	mov ds:[_i],ax
_10:	mov dx,1
	mov ax,ds:[_i]
	cmp ax,ds:[_N]
	jna _10_n
	mov dx,0
_10_n:	mov es:[6],dx
_11:	mov ax,es:[6]
	cmp ax,0
	jne _11_n
	jmp far ptr _22
_11_n:	nop
_12:	mov ax,es:[6]
	cmp ax,0
	je _12_n
	jmp far ptr _16
_12_n:	nop
_13:	mov ax,ds:[_i]
	add ax,1
	mov es:[8],ax
_14:	mov ax,es:[8]
	mov ds:[_i],ax
_15:	jmp far ptr _10
_16:	mov ax,ds:[_i]
	mov dx,0
	mov bx,2
	div bx
	mov es:[10],dx
_17:	mov dx,1
	mov ax,es:[10]
	cmp ax,1
	je _17_n
	mov dx,0
_17_n:	mov es:[12],dx
_18:	mov ax,es:[12]
	cmp ax,0
	jne _18_n
	jmp far ptr _21
_18_n:	nop
_19:	mov ax,ds:[_sum]
	add ax,ds:[_i]
	mov es:[14],ax
_20:	mov ax,es:[14]
	mov ds:[_sum],ax
_21:	jmp far ptr _13
_22:	jmp far ptr _33
_23:	mov dx,1
	mov ax,ds:[_choice]
	cmp ax,2
	je _23_n
	mov dx,0
_23_n:	mov es:[16],dx
_24:	mov ax,es:[16]
	cmp ax,0
	jne _24_n
	jmp far ptr _33
_24_n:	nop
_25:	mov ax,0
	mov ds:[_i],ax
_26:	mov dx,1
	mov ax,ds:[_i]
	cmp ax,ds:[_N]
	jb _26_n
	mov dx,0
_26_n:	mov es:[18],dx
_27:	mov ax,es:[18]
	cmp ax,0
	jne _27_n
	jmp far ptr _33
_27_n:	nop
_28:	mov ax,ds:[_sum]
	add ax,ds:[_i]
	mov es:[20],ax
_29:	mov ax,es:[20]
	mov ds:[_sum],ax
_30:	mov ax,ds:[_i]
	add ax,2
	mov es:[22],ax
_31:	mov ax,es:[22]
	mov ds:[_i],ax
_32:	jmp far ptr _26
_33:	mov ax,ds:[_sum]
	push ax
_34:	call _write
	mov es:[24],ax
quit:	mov ah,4ch
	int 21h


_read:	push bp
	mov bp,sp
	mov bx,offset _msg_s
	call _print
	mov bx,offset _buff_s
	mov di,0
_r_lp_1:	mov ah,1
	int 21h
	cmp al,0dh
	je _r_brk_1
	mov ds:[bx+di],al
	inc di
	jmp short _r_lp_1
_r_brk_1:	mov ah,2
	mov dl,0ah
	int 21h
	mov ax,0
	mov si,0
	mov cx,10
_r_lp_2:	mov dl,ds:[bx+si]
	cmp dl,30h
	jb _r_brk_2
	cmp dl,39h
	ja _r_brk_2
	sub dl,30h
	mov ds:[bx+si],dl
	mul cx
	mov dl,ds:[bx+si]
	mov dh,0
	add ax,dx
	inc si
	jmp short _r_lp_2
_r_brk_2:	mov cx,di
	mov si,0
_r_lp_3:	mov byte ptr ds:[bx+si],0
	loop _r_lp_3
	mov sp,bp
	pop bp
	ret

_write:	push bp
	mov bp,sp
	mov bx,offset _msg_p
	call _print
	mov ax,ss:[bp+4]
	mov bx,10
	mov cx,0
_w_lp_1:	mov dx,0
	div bx
	push dx
	inc cx
	cmp ax,0
	jne _w_lp_1
	mov di ,offset _buff_p
_w_lp_2:	pop ax
	add ax,30h
	mov ds:[di],al
	inc di
	loop _w_lp_2
	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,di
	sub cx,offset _buff_p
	mov di,offset _buff_p
_w_lp_3:	mov al,24h
	mov ds:[di],al
	inc di
	loop _w_lp_3
	mov ax,di
	sub ax,offset _buff_p
	mov sp,bp
	pop bp
	ret 2
_print:	mov si,0
	mov di,offset _buff_p
_p_lp_1:	mov al,ds:[bx+si]
	cmp al,0
	je _p_brk_1
	mov ds:[di],al
	inc si
	inc di
	jmp short _p_lp_1
_p_brk_1:	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,si
	mov di,offset _buff_p
_p_lp_2:	mov al,24h
	mov ds:[di],al
	inc di
	loop _p_lp_2
	ret
code ends

end start

