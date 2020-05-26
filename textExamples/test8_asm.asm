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
	_a dw 0
	_N dw 0
	_M dw 0
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

_1:	mov ax,1
	mov ds:[_a],ax
_2:	call _read
	mov es:[0],ax
_3:	mov ax,es:[0]
	mov ds:[_N],ax
_4:	call _read
	mov es:[2],ax
_5:	mov ax,es:[2]
	mov ds:[_M],ax
_6:	mov ax,ds:[_M]
	push ax
_7:	mov ax,ds:[_N]
	push ax
_8:	call _max
	mov es:[4],ax
_9:	mov ax,es:[4]
	push ax
_10:	mov ax,100
	push ax
_11:	call _sum
	mov es:[6],ax
_12:	mov ax,es:[6]
	mov ds:[_a],ax
_13:	mov ax,ds:[_a]
	push ax
_14:	call _write
	mov es:[8],ax
quit:	mov ah,4ch
	int 21h


_sum:	push bp
	mov bp,sp
	sub sp,2
_17:	mov ax,ss:[bp+6]
	add ax,ss:[bp+4]
	mov es:[10],ax
_18:	mov ax,es:[10]
	mov ss:[bp-2],ax
_19:	mov ax,ss:[bp-2]
	mov sp,bp
	pop bp
	ret 4
_20:	mov sp,bp
	pop bp
	ret 4

_max:	push bp
	mov bp,sp
	sub sp,2
_22:	mov dx,1
	mov ax,ss:[bp+6]
	cmp ax,ss:[bp+4]
	jnb _22_n
	mov dx,0
_22_n:	mov es:[12],dx
_23:	mov ax,es:[12]
	cmp ax,0
	jne _23_n
	jmp far ptr _26
_23_n:	nop
_24:	mov ax,ss:[bp+6]
	mov ss:[bp-2],ax
_25:	jmp far ptr _27
_26:	mov ax,ss:[bp+4]
	mov ss:[bp-2],ax
_27:	mov ax,ss:[bp-2]
	mov sp,bp
	pop bp
	ret 4
_28:	mov sp,bp
	pop bp
	ret 4

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

