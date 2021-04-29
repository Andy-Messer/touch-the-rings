for file in `find -type f -name "*.png"`
do
	convert -fill $1 -opaque $2 ${file} ${file}
done
