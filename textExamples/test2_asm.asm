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
	_factor dw 0
	_n dw 0
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
	mov ds:[_i],ax
_2:	call _read
	mov es:[0],ax
_3:	mov ax,es:[0]
	mov ds:[_n],ax
_4:	mov dx,1
	mov ax,ds:[_n]
	cmp ax,1
	jb _4_n
	mov dx,0
_4_n:	mov es:[2],dx
_5:	mov ax,es:[2]
	cmp ax,0
	jne _5_n
	jmp far ptr _8
_5_n:	nop
_6:	mov ax,0
	mov ds:[_factor],ax
_7:	jmp far ptr _9
_8:	mov ax,1
	mov ds:[_factor],ax
_9:	mov dx,1
	mov ax,ds:[_i]
	cmp ax,ds:[_n]
	jb _9_n
	mov dx,0
_9_n:	mov es:[4],dx
_10:	mov ax,es:[4]
	cmp ax,0
	jne _10_n
	jmp far ptr _16
_10_n:	nop
_11:	mov ax,ds:[_i]
	add ax,1
	mov es:[6],ax
_12:	mov ax,es:[6]
	mov ds:[_i],ax
_13:	mov ax,ds:[_factor]
	mov bx,ds:[_i]
	mul bx
	mov es:[8],ax
_14:	mov ax,es:[8]
	mov ds:[_factor],ax
_15:	jmp far ptr _9
_16:	mov ax,ds:[_factor]
	push ax
_17:	call _write
	mov es:[10],ax
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

