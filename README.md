![Natrium Logo](./assets/gthub-header-dark.svg#gh-dark-mode-only)
![Natrium Logo](./assets/gthub-header-light.svg#gh-light-mode-only)

A compiled language designed with the simplicity of Python, syntax of Basic and fine control & performance of C in mind. The language is still under-development, hence I do not recommend that you use it now. The language is scheduled to enter open beta by September. Documentation and tutorials will be out soon!

But if you do want to play around with it, the syntax highlighting is currently available for vscode, in the language directly. To install it, use the 'Developer: Install Extension From Location...' command from the command palette, and select the 'language' directory

Until then, here are some previews of Nartium (files in the examples directory):

Hello world:

```
load core

~ The main function is called automatically during runtime

task main(string[] args) (returns int) do
  let string hello = "Hello world!"  
  write(hello, stdout)
  
  return 0
end
```

Fibonacci:

```
load core
load fmt

~ This is a simple fibonacci program written in the natrium language

task fib (uint64 n) (returns uint64)  do
  let uint64 a = 1
  let uint64 b = 0
  let uint64 c = 0

  for i in range(0, n) do
    a = c
    b + c = a
    c = b 
  end

  return a
end


task main (string[] args) (returns int) do 
  let int64 fib_res = fib(10)
  write (fmt(fib_res), stdout)
  return 0
end
```

Calculator:
```
task main(string[] args) (returns int) do
    
    write("num 1: ", stdout)
    let int num1 = allocate 32
    move read(stdin) cast int into num1

    write("num 2: ", stdout)
    let int num2 = allocate 32
    move read(stdin) cast int into num2

    write("operation: ", stdout)
    let string operation = allocate 4
    move read(stdin) into operation

    let int res = allocate 64

    switch operation do
        case "+" do
            move num1 + num2 into res
        end

        case "-" do
            move num1 - num2 into res
        end

        case "*" do
            move num1 * num2 into res
        end

        case "/" do
            if num2 == 0 then
                throw ("Division by 0!")
            end

            move num1 / num2 into res
        end
    end

    write (fmt(res), stdout)
    return 0
    
end
```
