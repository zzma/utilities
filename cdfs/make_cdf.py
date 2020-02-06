import argparse
import sys 


parser = argparse.ArgumentParser(description='Generate a gnuplot CDF file')
parser.add_argument('input_file', help='input file')
parser.add_argument('data_file', help='output data file')
parser.add_argument('gnuplot_file', help='output gnuplot file')
parser.add_argument('--categorical', help='input file contains categorical data', action="store_true")
parser.add_argument('--log_scale', help='log-scale', action="store_true")
args = parser.parse_args()


if args.categorical: 
    print("Categorical ASN unimplemented")
else:
    values = []
    
    with open(args.input_file) as f:
        for line in f:
            value = float(line.rstrip())
            values.append(value)
    
    values = sorted(values)
    total = len(values)
    
    with open(args.data_file, 'w') as f: 
        current_value = 0
        for i in range(len(values)):
            if values[i] > current_value:
                f.write(f"{current_value},{float(i)/total}\n")
                current_value = values[i]
    
        f.write(f"{values[-1]},{float(1)}\n")


gnuplot_template = f'''set term pdf enhanced font "Helvetica,20" size 6in, 3in
output_filename = "{args.gnuplot_file}.pdf"
set output output_filename

set key autotitle columnheader
set datafile commentschars "#%"
set datafile separator ","

set xlabel "CHANGEME"
set ylabel "CDF"
set style data points
set autoscale fix
set ytics nomirror  font ",20"
set xlabel font ",20"
set ylabel font ",20"
set grid x y
{"#" if not args.log_scale else ""} set logscale x
set yrange [0:1]
set ytics 0,0.1,1

set key bottom right box width 3 height 1
set key font ",20"

set for [i=1:6] linetype i pointtype i lw 2

plot "{args.data_file}" using 1:2 with lines title "CHANGEME";

set output
system 'pdfcrop '.output_filename.' temp >/dev/null && mv temp '.output_filename.' && open '.output_filename
'''


with open(args.gnuplot_file, 'w') as f: 
    f.write(gnuplot_template)



