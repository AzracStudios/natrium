![Natrium Logo](./assets/gthub-header-dark.svg#gh-dark-mode-only)
![Natrium Logo](./assets/gthub-header-light.svg#gh-light-mode-only)

A compiled language designed with the simplicity of Python, syntax of Basic and fine control & performance of C in mind. The language is still under-development, so I do not recommend that you use it now. Documentation and tutorials will be out soon!

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

task fib (int n) (returns int)  do
  let int a = 1
  let int b = 0
  let int c = 0

  for i in range(0, n) do
    a = b + c
    b = c
    c = a
  end

  free b
  free c

  return a
end


task main (string[] args) (returns int) do 
  let int fib_res : allocate 64 = fib(10)
  
  write (fmt(fib_res), stdout)

  return 0
end

```

Calculator:
```
task main(string[] args) (returns int) do
    
    write("num 1: ", stdout)
    let int num1 = read(stdin) cast int

    write("num 2: ", stdout)
    let int num2 = read(stdin) cast int

    write("operation: ", stdout)
    let string operation = read(stdin)

    let int res = 0

    switch operation do
        case "+" do
            res = num1 + num2
        end

        case "-" do 
            res = num1 - num2
        end

        case "*" do
            res = num1 * num2
        end

        case "/" do
            if num2 == 0 then
                throw ("Division by 0!")
            end

            res = num1 / num2
        end
    end

    write (fmt(res), stdout)
    return 0
    
end
```
