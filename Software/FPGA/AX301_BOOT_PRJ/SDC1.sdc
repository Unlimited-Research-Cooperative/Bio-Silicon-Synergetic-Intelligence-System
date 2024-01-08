create_clock -name clk -period 20 [get_ports {clk}]

create_clock -name cmos_clk -period 15.38 [get_ports {cmos_pclk}]




derive_pll_clocks -create_base_clocks


set_false_path -from [get_clocks {cmos_clk}] -to [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[1]}]
set_false_path -from [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[1]}] -to [get_clocks {cmos_clk}]

set_false_path -from [get_clocks {video_pll_m0|altpll_component|auto_generated|pll1|clk[0]}] -to [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[1]}]
set_false_path -from [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[1]}] -to [get_clocks {video_pll_m0|altpll_component|auto_generated|pll1|clk[0]}]

#set_false_path -from [get_clocks {clk}] -to [get_clocks {video_pll_m0|altpll_component|auto_generated|pll1|clk[0]}]
#set_false_path -from [get_clocks {video_pll_m0|altpll_component|auto_generated|pll1|clk[0]}] -to [get_clocks {clk}]
#
#set_false_path -from [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[0]}] -to [get_clocks {clk}]
#set_false_path -from [get_clocks {clk}] -to [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[0]}]

set_false_path -from [get_clocks {clk}] -to [get_clocks {video_pll_m0|altpll_component|auto_generated|pll1|clk[0]}]
set_false_path -from [get_clocks {video_pll_m0|altpll_component|auto_generated|pll1|clk[0]}] -to [get_clocks {clk}]

set_false_path -from [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[1]}] -to [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[0]}]
set_false_path -from [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[0]}] -to [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[1]}]

#set_false_path -from {sdbmp_rst_n} -to {sdbmp_top:sdbmp_dut|sd_card_bmp:sd_card_bmp_m0|bmp_read:bmp_read_m0|width[*]}
#set_false_path -from {sdbmp_top:sdbmp_dut|sd_card_bmp:sd_card_bmp_m0|bmp_read:bmp_read_m0|state_code[*]} -to {sdbmp_top:sdbmp_dut|seg_scan:seg_scan_m0|seg_data[*]}
#set_false_path -from {ax_debounce:ax_debounce_a2|button_negedge} -to {current_state.idle}
#set_false_path -from {ax_debounce:ax_debounce_a2|button_negedge} -to {current_state.sd_mode}
#
#set_false_path -from {ax_debounce:ax_debounce_a2|button_negedge} -to {sdram_rst_n}
#set_false_path -from {ax_debounce:ax_debounce_a2|button_negedge} -to {current_state.ledflash_mode}
#set_false_path -from {ax_debounce:ax_debounce_a2|button_negedge} -to {current_state.eeprom_mode}

set_false_path -from [get_clocks {clk}] -to [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[0]}]
set_false_path -from [get_clocks {sys_pll_m0|altpll_component|auto_generated|pll1|clk[0]}] -to [get_clocks {clk}]


set_false_path -from [get_clocks {clk}] -to [get_clocks {cmos_clk}]
set_false_path -from [get_clocks {cmos_clk}] -to [get_clocks {clk}]


