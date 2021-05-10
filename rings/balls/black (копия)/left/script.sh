for file in `find -type f -name "*.png"`
do
	convert -fuzz 35% -fill $1 -opaque $2 ${file} ${file}
done
