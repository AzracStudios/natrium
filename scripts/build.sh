echo "Compiling the following files...\n"
cd ~/Desktop/natrium/src
go list -f={{.GoFiles}}
go build -o ~/Desktop/natrium/natrium *.go 
echo "\nDone!!"