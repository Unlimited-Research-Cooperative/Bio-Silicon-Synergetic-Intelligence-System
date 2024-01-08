# Copyright (C) 2017  Intel Corporation. All rights reserved.
# Your use of Intel Corporation's design tools, logic functions 
# and other software and tools, and its AMPP partner logic 
# functions, and any output files from any of the foregoing 
# (including device programming or simulation files), and any 
# associated documentation or information are expressly subject 
# to the terms and conditions of the Intel Program License 
# Subscription Agreement, the Intel Quartus Prime License Agreement,
# the Intel FPGA IP License Agreement, or other applicable license
# agreement, including, without limitation, that your use is for
# the sole purpose of programming logic devices manufactured by
# Intel and sold by Intel or its authorized distributors.  Please
# refer to the applicable agreement for further details.

# Quartus Prime Version 17.1.0 Build 590 10/25/2017 SJ Lite Edition
# File: D:\intel_project\AX1025\CD\demo\tcl文件\06_spi_flash_test.tcl
# Generated on: Wed Jan 24 15:15:54 2018

package require ::quartus::project

set_location_assignment PIN_E1 -to clk
set_location_assignment PIN_M15 -to rst_n
set_location_assignment PIN_N16 -to led[3]
set_location_assignment PIN_N15 -to led[2]
set_location_assignment PIN_P16 -to led[1]
set_location_assignment PIN_R16 -to led[0]
set_location_assignment PIN_T7 -to led1
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to clk
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to led[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to led[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to led[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to led[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to led1
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rst_n
#spi flash pins
set_location_assignment PIN_M16 -to key2
set_location_assignment PIN_H1 -to DCLK
set_location_assignment PIN_H2 -to MISO
set_location_assignment PIN_C1 -to MOSI
set_location_assignment PIN_D2 -to nCS
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to key2
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to DCLK
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to MISO
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to MOSI
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to nCS
#rtc pins
set_location_assignment PIN_E1 -to clk
set_location_assignment PIN_G15 -to rtc_sclk
set_location_assignment PIN_J15 -to rtc_data
set_location_assignment PIN_J16 -to rtc_ce
set_location_assignment PIN_M15 -to rst_n
set_location_assignment PIN_M1 -to uart_rx
set_location_assignment PIN_R6 -to uart_tx
#i2c eeprom pins
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to i2c_scl
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to i2c_sda
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to key3
set_location_assignment PIN_K1 -to i2c_scl
set_location_assignment PIN_K2 -to i2c_sda
set_location_assignment PIN_E16 -to key3
#sd audio pins
set_location_assignment PIN_L16 -to sd_dclk
set_location_assignment PIN_L15 -to sd_miso
set_location_assignment PIN_K15 -to sd_mosi
set_location_assignment PIN_K16 -to sd_ncs
set_location_assignment PIN_T12 -to wm8731_adcdat
set_location_assignment PIN_T13 -to wm8731_adclrc
set_location_assignment PIN_R11 -to wm8731_bclk
set_location_assignment PIN_T11 -to wm8731_dacdat
set_location_assignment PIN_R12 -to wm8731_daclrc
set_location_assignment PIN_R10 -to wm8731_scl
set_location_assignment PIN_T10 -to wm8731_sda
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sd_dclk
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sd_miso
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sd_mosi
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sd_ncs
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_adcdat
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_adclrc
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_bclk
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_dacdat
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_daclrc
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_scl
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to wm8731_sda
set_location_assignment PIN_E15 -to key4
#ov5640pins
set_location_assignment PIN_J1 -to tmds_clk_n
set_location_assignment PIN_J2 -to tmds_clk_p
set_location_assignment PIN_P1 -to tmds_data_n[2]
set_location_assignment PIN_N1 -to tmds_data_n[1]
set_location_assignment PIN_L1 -to tmds_data_n[0]
set_location_assignment PIN_P2 -to tmds_data_p[2]
set_location_assignment PIN_N2 -to tmds_data_p[1]
set_location_assignment PIN_L2 -to tmds_data_p[0]
set_location_assignment PIN_F9 -to sdram_addr[12]
set_location_assignment PIN_F8 -to sdram_addr[11]
set_location_assignment PIN_A5 -to sdram_addr[10]
set_location_assignment PIN_E8 -to sdram_addr[9]
set_location_assignment PIN_C8 -to sdram_addr[8]
set_location_assignment PIN_D8 -to sdram_addr[7]
set_location_assignment PIN_E7 -to sdram_addr[6]
set_location_assignment PIN_C6 -to sdram_addr[5]
set_location_assignment PIN_D6 -to sdram_addr[4]
set_location_assignment PIN_A2 -to sdram_addr[3]
set_location_assignment PIN_B4 -to sdram_addr[2]
set_location_assignment PIN_A4 -to sdram_addr[1]
set_location_assignment PIN_B5 -to sdram_addr[0]
set_location_assignment PIN_B6 -to sdram_ba[1]
set_location_assignment PIN_A6 -to sdram_ba[0]
set_location_assignment PIN_B10 -to sdram_cas_n
set_location_assignment PIN_C9 -to sdram_cke
set_location_assignment PIN_D3 -to sdram_clk
set_location_assignment PIN_A7 -to sdram_cs_n
set_location_assignment PIN_D14 -to sdram_dq[15]
set_location_assignment PIN_E11 -to sdram_dq[14]
set_location_assignment PIN_C14 -to sdram_dq[13]
set_location_assignment PIN_D12 -to sdram_dq[12]
set_location_assignment PIN_D11 -to sdram_dq[11]
set_location_assignment PIN_E10 -to sdram_dq[10]
set_location_assignment PIN_C11 -to sdram_dq[9]
set_location_assignment PIN_E9 -to sdram_dq[8]
set_location_assignment PIN_B11 -to sdram_dq[7]
set_location_assignment PIN_A12 -to sdram_dq[6]
set_location_assignment PIN_B12 -to sdram_dq[5]
set_location_assignment PIN_A13 -to sdram_dq[4]
set_location_assignment PIN_B13 -to sdram_dq[3]
set_location_assignment PIN_A14 -to sdram_dq[2]
set_location_assignment PIN_B14 -to sdram_dq[1]
set_location_assignment PIN_A15 -to sdram_dq[0]
set_location_assignment PIN_D9 -to sdram_dqm[1]
set_location_assignment PIN_A11 -to sdram_dqm[0]
set_location_assignment PIN_B7 -to sdram_ras_n
set_location_assignment PIN_A10 -to sdram_we_n
set_location_assignment PIN_D1 -to cmos_db[7]
set_location_assignment PIN_C3 -to cmos_db[6]
set_location_assignment PIN_L3 -to cmos_db[5]
set_location_assignment PIN_G2 -to cmos_db[4]
set_location_assignment PIN_C2 -to cmos_db[3]
set_location_assignment PIN_B1 -to cmos_db[2]
set_location_assignment PIN_K5 -to cmos_db[1]
set_location_assignment PIN_G1 -to cmos_db[0]
set_location_assignment PIN_B8 -to cmos_pclk
set_location_assignment PIN_B3 -to cmos_scl
set_location_assignment PIN_A3 -to cmos_sda
set_location_assignment PIN_A8 -to cmos_vsync
set_location_assignment PIN_F3 -to cmos_xclk
set_location_assignment PIN_E6 -to cmos_href

#FT232H
set_location_assignment PIN_M2 -to ft_clk
set_location_assignment PIN_N3 -to ft_data[7]
set_location_assignment PIN_R5 -to ft_data[6]
set_location_assignment PIN_N6 -to ft_data[5]
set_location_assignment PIN_T4 -to ft_data[4]
set_location_assignment PIN_R4 -to ft_data[3]
set_location_assignment PIN_T3 -to ft_data[2]
set_location_assignment PIN_R3 -to ft_data[1]
set_location_assignment PIN_T2 -to ft_data[0]
set_location_assignment PIN_T6 -to ft_oe_n
set_location_assignment PIN_P3 -to ft_rd_n
set_location_assignment PIN_N5 -to ft_rxf_n
set_location_assignment PIN_T5 -to ft_txe_n
set_location_assignment PIN_P8 -to ft_wr_n

#ETHERNET
set_location_assignment PIN_R1 -to e_mdio
set_location_assignment PIN_P6 -to e_mdc
set_location_assignment PIN_R8 -to rgmii_rxc
set_location_assignment PIN_B9 -to rgmii_rxctl
set_location_assignment PIN_T8 -to rgmii_rxd[3]
set_location_assignment PIN_T9 -to rgmii_rxd[2]
set_location_assignment PIN_R9 -to rgmii_rxd[1]
set_location_assignment PIN_A9 -to rgmii_rxd[0]
set_location_assignment PIN_L8 -to rgmii_txc
set_location_assignment PIN_M8 -to rgmii_txctl
set_location_assignment PIN_M7 -to rgmii_txd[3]
set_location_assignment PIN_M6 -to rgmii_txd[2]
set_location_assignment PIN_L4 -to rgmii_txd[1]
set_location_assignment PIN_L7 -to rgmii_txd[0]

set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to e_mdc
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to e_mdio
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_rxc
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_rxctl
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_rxd[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_rxd[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_rxd[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_rxd[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_txc
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_txctl
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_txd[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_txd[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_txd[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rgmii_txd[0]