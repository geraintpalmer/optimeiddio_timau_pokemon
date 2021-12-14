for had in {0..99}
do
	enwffeil='haptim_'${had}'.csv'
	echo "Gwerthudo gyda ffeil: ${had}"
	python gwerthuso.py $enwffeil base
done