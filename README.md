![Natrium Logo](./assets/gthub-header-dark.svg#gh-dark-mode-only)
![Natrium Logo](./assets/gthub-header-light.svg#gh-light-mode-only)

A compiled language designed with the simplicity of Python, syntax of Basic and fine control & performance of C in mind. The language is still under-development, hence I do not recommend that you use it now. The language is scheduled to enter open beta by September. Documentation and tutorials will be out soon!

But if you do want to play around with it, the syntax highlighting is currently available for vscode, in the language directly. To install it, use the 'Developer: Install Extension From Location...' command from the command palette, and select the 'language' directory

Until then, here are some previews of Nartium (files in the examples directory):

Hello world:

```
load core

~ The main function is called automatically during runtime

task main(*string[] args) (returns int) do
  let *string hello = allocate 14 ~ Allocate 14 bytes for the hello world string
  move "Hello, world!\n" into hello

  write(hello, stdout)

  free hello

  return 0
end
```

Fibonacci:

```
load core
load fmt

~ This is a simple fibonacci program written in the natrium language

task fib (int range) (returns *int64)  do
  let *uint64 a = allocate dynamic
  let *uint64 b = allocate dynamic
  let *uint64 c = allocate dynamic

  ~ Use the dynamic keyword when allocating memory, if the variable is modified in the runtime.
  ~ Only do this if the maximum memory required is unkown

  move 1 into a
  move 0 into b
  move 0 into c

  for i in [0:range:1] do
    move &a into c
    move &b + &c into a
    move &c into b
  end

  return a
end

task main (string[] *args) (returns int) do
  let *int64 fib_res = fib(10)
  write (fmt(&fib_res), stdout)
  return 0
end
```

Line counter:
```
load core
load fmt

task get_lines(*string path) (returns *int) do
  ~ Allocate memory for a string that is 1 KB long
  let *string input = allocate 1024
  let *uint64 lines = allocate dynamic

  ~ Load file at path
  move read(&path, "utf-8", 1024) into input

  ~ Count lines
  for i in input do
    if i == "\n" then
      move &lines + 1 into lines
    end
  end

  ~ Free variables
  free input

  ~ Return line count
  return lines
end

task main(string[] args) (returns int) do
  ~ Get path from args
  let *string path = allocate 512

  ~ Check if path exists
  if args[1] == nil then
    throw ("Expected path!")
    return 0
  end

  move args[1] into path

  ~ Call get_lines function and store the value
  let *int lines = get_lines(path)

  ~ Print the number of lines
  write(fmt(&lines), stdout)

  ~ Free variables
  free lines
  free path

  ~ Return success
  return 0
end 
```
