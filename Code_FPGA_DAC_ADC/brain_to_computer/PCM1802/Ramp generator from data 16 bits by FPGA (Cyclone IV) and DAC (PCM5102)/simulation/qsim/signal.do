onerror {exit -code 1}
vlib work
vlog -work work signal.vo
vlog -work work test.vwf.vt
vsim -novopt -c -t 1ps -L cycloneive_ver -L altera_ver -L altera_mf_ver -L 220model_ver -L sgate work.generator_vlg_vec_tst -voptargs="+acc"
vcd file -direction signal.msim.vcd
vcd add -internal generator_vlg_vec_tst/*
vcd add -internal generator_vlg_vec_tst/i1/*
run -all
quit -f
