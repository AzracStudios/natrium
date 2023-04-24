
section .bss
digitSpace resb 100
digitSpacePos resb 8
section .text
global _start
_printNum:
mov rcx, digitSpace
mov rbx, 10
mov [rcx], rbx
inc rcx
mov [digitSpacePos], rcx
_printNumLoop:
mov rdx, 0
mov rbx, 10
div rbx
push rax
add rdx, 48
mov rcx, [digitSpacePos]
mov [rcx], dl
inc rcx
mov [digitSpacePos], rcx
pop rax
cmp rax, 0
jne _printNumLoop
_printNumLoop2:
mov rcx, [digitSpacePos]
mov rax, 1
mov rdi, 1
mov rsi, rcx
mov rdx, 1
syscall
mov rcx, [digitSpacePos]
dec rcx
mov [digitSpacePos], rcx
cmp rcx, digitSpace
jge _printNumLoop2
ret
_start:
mov rax, 35
mov rbx, 2
div rbx

mov rax, rdx
call _printNum
mov rax, 60
mov rdi, 0
syscall
