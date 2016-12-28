
basepath=$(cd `dirname $0`; pwd)
cd $basepath
python alipayar_1.py input/ output
rm -f input/*
