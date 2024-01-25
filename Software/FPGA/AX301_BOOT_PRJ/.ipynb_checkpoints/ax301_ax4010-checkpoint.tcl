

set_location_assignment PIN_E1 -to clk

#key
set_location_assignment PIN_E16 -to key4
set_location_assignment PIN_M16 -to key3

set_location_assignment PIN_M15 -to key2
set_location_assignment PIN_N13 -to rst_n
#eeprom
set_location_assignment PIN_E6 -to i2c_sda
set_location_assignment PIN_D1 -to i2c_scl
#led 

set_location_assignment PIN_D9 -to led[3]
set_location_assignment PIN_C9 -to led[2]
set_location_assignment PIN_F9 -to led[1]
set_location_assignment PIN_E10 -to led[0]
#buzzer
set_location_assignment PIN_C11 -to buzzer
#buzzer
set_location_assignment PIN_P6 -to rtc_sclk
set_location_assignment PIN_M8 -to rtc_data
set_location_assignment PIN_N8 -to rtc_ce
#uart
set_location_assignment PIN_N1 -to uart_tx
set_location_assignment PIN_M2 -to uart_rx
#digital led display

set_location_assignment PIN_R16 -to seg_data[7]
set_location_assignment PIN_N15 -to seg_data[6]
set_location_assignment PIN_N12 -to seg_data[5]
set_location_assignment PIN_P15 -to seg_data[4]
set_location_assignment PIN_T15 -to seg_data[3]
set_location_assignment PIN_P16 -to seg_data[2]
set_location_assignment PIN_N16 -to seg_data[1]
set_location_assignment PIN_R14 -to seg_data[0]
set_location_assignment PIN_M11 -to seg_sel[5]
set_location_assignment PIN_P11 -to seg_sel[4]
set_location_assignment PIN_N11 -to seg_sel[3]
set_location_assignment PIN_M10 -to seg_sel[2]
set_location_assignment PIN_P9 -to seg_sel[1]
set_location_assignment PIN_N9 -to seg_sel[0]

#sd card spi mode

set_location_assignment PIN_D12 -to SD_DCLK
set_location_assignment PIN_E15 -to SD_MISO
set_location_assignment PIN_F10 -to SD_MOSI
set_location_assignment PIN_D11 -to SD_nCS

#16bit sdram

set_location_assignment PIN_F15 -to sdram_addr[12]
set_location_assignment PIN_D16 -to sdram_addr[11]
set_location_assignment PIN_F14 -to sdram_addr[10]
set_location_assignment PIN_D15 -to sdram_addr[9]
set_location_assignment PIN_C16 -to sdram_addr[8]
set_location_assignment PIN_C15 -to sdram_addr[7]
set_location_assignment PIN_B16 -to sdram_addr[6]
set_location_assignment PIN_A15 -to sdram_addr[5]
set_location_assignment PIN_A14 -to sdram_addr[4]
set_location_assignment PIN_C14 -to sdram_addr[3]
set_location_assignment PIN_D14 -to sdram_addr[2]
set_location_assignment PIN_E11 -to sdram_addr[1]
set_location_assignment PIN_F11 -to sdram_addr[0]
set_location_assignment PIN_F13 -to sdram_ba[1]
set_location_assignment PIN_G11 -to sdram_ba[0]
set_location_assignment PIN_J12 -to sdram_cas_n
set_location_assignment PIN_F16 -to sdram_cke
set_location_assignment PIN_B14 -to sdram_clk
set_location_assignment PIN_K10 -to sdram_cs_n
set_location_assignment PIN_L15 -to sdram_dq[15]
set_location_assignment PIN_L16 -to sdram_dq[14]
set_location_assignment PIN_K15 -to sdram_dq[13]
set_location_assignment PIN_K16 -to sdram_dq[12]
set_location_assignment PIN_J15 -to sdram_dq[11]
set_location_assignment PIN_J16 -to sdram_dq[10]
set_location_assignment PIN_J11 -to sdram_dq[9]
set_location_assignment PIN_G16 -to sdram_dq[8]
set_location_assignment PIN_K12 -to sdram_dq[7]
set_location_assignment PIN_L11 -to sdram_dq[6]
set_location_assignment PIN_L14 -to sdram_dq[5]
set_location_assignment PIN_L13 -to sdram_dq[4]
set_location_assignment PIN_L12 -to sdram_dq[3]
set_location_assignment PIN_N14 -to sdram_dq[2]
set_location_assignment PIN_M12 -to sdram_dq[1]
set_location_assignment PIN_P14 -to sdram_dq[0]
set_location_assignment PIN_G15 -to sdram_dqm[1]
set_location_assignment PIN_J14 -to sdram_dqm[0]
set_location_assignment PIN_K11 -to sdram_ras_n
set_location_assignment PIN_J13 -to sdram_we_n

# 16bit vga output

set_location_assignment PIN_F6 -to vga_out_b[4]
set_location_assignment PIN_E5 -to vga_out_b[3]
set_location_assignment PIN_D3 -to vga_out_b[2]
set_location_assignment PIN_D4 -to vga_out_b[1]
set_location_assignment PIN_C3 -to vga_out_b[0]
set_location_assignment PIN_J6 -to vga_out_g[5]
set_location_assignment PIN_L8 -to vga_out_g[4]
set_location_assignment PIN_K8 -to vga_out_g[3]
set_location_assignment PIN_F7 -to vga_out_g[2]
set_location_assignment PIN_G5 -to vga_out_g[1]
set_location_assignment PIN_F5 -to vga_out_g[0]
set_location_assignment PIN_L6 -to vga_out_hs
set_location_assignment PIN_L4 -to vga_out_r[4]
set_location_assignment PIN_L3 -to vga_out_r[3]
set_location_assignment PIN_L7 -to vga_out_r[2]
set_location_assignment PIN_K5 -to vga_out_r[1]
set_location_assignment PIN_K6 -to vga_out_r[0]
set_location_assignment PIN_N3 -to vga_out_vs

#cmos an5640 module 

set_location_assignment PIN_J2 -to cmos_db[7]
set_location_assignment PIN_J1 -to cmos_db[6]
set_location_assignment PIN_N5 -to cmos_db[5]
set_location_assignment PIN_L1 -to cmos_db[4]
set_location_assignment PIN_M1 -to cmos_db[3]
set_location_assignment PIN_G2 -to cmos_db[2]
set_location_assignment PIN_M6 -to cmos_db[1]
set_location_assignment PIN_L2 -to cmos_db[0]
set_location_assignment PIN_K1 -to cmos_href
set_location_assignment PIN_G1 -to cmos_pclk
set_location_assignment PIN_F1 -to cmos_scl
set_location_assignment PIN_F3 -to cmos_sda
set_location_assignment PIN_F2 -to cmos_vsync
set_location_assignment PIN_K2 -to cmos_xclk
set_location_assignment PIN_N6 -to cmos_rst_n
set_location_assignment PIN_M7 -to cmos_pwdn

#wm8731 audio module an831 on J2

# set_location_assignment pin_b4 -to wm8731_adcdat
# set_location_assignment pin_a2 -to wm8731_bclk
# set_location_assignment pin_b3 -to wm8731_dacdat
# set_location_assignment pin_a3 -to wm8731_daclrc
# set_location_assignment pin_b1 -to wm8731_scl
# set_location_assignment pin_c2 -to wm8731_sda
# set_location_assignment pin_b5 -to wm8731_adclrc

#neuromimetic stimulation module

# Bit Clock which is the clock signal that toggles on each bit of the audio data, controls CS4344
set_location_assignment pin_a2 -to SCLK 
# Word Select or Left/Right Clock (LRCLK) which indicates whether the current audio data word is for the left or right channel, should map to LRCLK on the CS4344
set_location_assignment pin_a3 -to LRCLK 
# Master Clock for CS4344
set_location_assignment pin_b5 -to MCLK 
set_location_assignment PIN_A5 -to audio_signal_1
set_location_assignment PIN_B6 -to audio_signal_2
set_location_assignment PIN_A6 -to audio_signal_3
set_location_assignment PIN_B7 -to audio_signal_4
set_location_assignment PIN_A7 -to audio_signal_5
set_location_assignment PIN_B8 -to audio_signal_6
set_location_assignment PIN_A8 -to audio_signal_7
set_location_assignment PIN_B9 -to audio_signal_8
set_location_assignment PIN_A9 -to audio_signal_9
set_location_assignment PIN_B10 -to audio_signal_10
set_location_assignment PIN_A10 -to audio_signal_11
set_location_assignment PIN_B11 -to audio_signal_12
set_location_assignment PIN_A11 -to audio_signal_13
set_location_assignment PIN_B12 -to audio_signal_14
set_location_assignment PIN_A12 -to audio_signal_15
set_location_assignment PIN_B13 -to audio_signal_16
set_location_assignment PIN_A13 -to audio_signal_17
set_location_assignment PIN_D5 -to audio_signal_18
set_location_assignment PIN_D6 -to audio_signal_19
set_location_assignment PIN_C6 -to audio_signal_20
set_location_assignment PIN_E7 -to audio_signal_21
set_location_assignment PIN_F8 -to audio_signal_22
set_location_assignment PIN_C8 -to audio_signal_23
set_location_assignment PIN_D8 -to audio_signal_24
set_location_assignment PIN_P1 -to audio_signal_25
set_location_assignment PIN_N2 -to audio_signal_26
set_location_assignment PIN_R1 -to audio_signal_27
set_location_assignment PIN_P2 -to audio_signal_28
set_location_assignment PIN_K9 -to audio_signal_29
set_location_assignment PIN_R8 -to audio_signal_30
set_location_assignment PIN_L10 -to audio_signal_31
set_location_assignment PIN_L9 -to audio_signal_32

# set_location_assignment pin_b4 -to wm8731_adcdat
# set_location_assignment pin_b3 -to wm8731_dacdat # DAC Data Input (SDIN on some DACs) which carries the actual audio data to be converted to an analog signal
# set_location_assignment pin_b1 -to wm8731_scl # SCL line for I2C communication, used for control settings of the codec
# set_location_assignment pin_c2 -to wm8731_sda # SDA line for I2C communication, used for control settings of the codec



#lcd an430 J2

# set_location_assignment PIN_A12 -to lcd_b[7]
# set_location_assignment PIN_B13 -to lcd_b[6]
# set_location_assignment PIN_A11 -to lcd_b[5]
# set_location_assignment PIN_B12 -to lcd_b[4]
# set_location_assignment PIN_A10 -to lcd_b[3]
# set_location_assignment PIN_B11 -to lcd_b[2]
# set_location_assignment PIN_A9 -to lcd_b[1]
# set_location_assignment PIN_B10 -to lcd_b[0]
# set_location_assignment PIN_D5 -to lcd_dclk
# set_location_assignment PIN_D6 -to lcd_de
# set_location_assignment PIN_A8 -to lcd_g[7]
# set_location_assignment PIN_B9 -to lcd_g[6]
# set_location_assignment PIN_A7 -to lcd_g[5]
# set_location_assignment PIN_B8 -to lcd_g[4]
# set_location_assignment PIN_A6 -to lcd_g[3]
# set_location_assignment PIN_B7 -to lcd_g[2]
# set_location_assignment PIN_A5 -to lcd_g[1]
# set_location_assignment PIN_B6 -to lcd_g[0]
# set_location_assignment PIN_A13 -to lcd_hs
# set_location_assignment PIN_A4 -to lcd_r[7]
# set_location_assignment PIN_B5 -to lcd_r[6]
# set_location_assignment PIN_A3 -to lcd_r[5]
# set_location_assignment PIN_B4 -to lcd_r[4]
# set_location_assignment PIN_A2 -to lcd_r[3]
# set_location_assignment PIN_B3 -to lcd_r[2]
# set_location_assignment PIN_C2 -to lcd_r[1]
# set_location_assignment PIN_B1 -to lcd_r[0]
# set_location_assignment PIN_C6 -to lcd_vs

# lcd AN070 J2

# set_location_assignment PIN_A5 -to lcd_b[7]
# set_location_assignment PIN_B6 -to lcd_b[6]
# set_location_assignment PIN_A6 -to lcd_b[5]
# set_location_assignment PIN_B7 -to lcd_b[4]
# set_location_assignment PIN_A7 -to lcd_b[3]
# set_location_assignment PIN_B8 -to lcd_b[2]
# set_location_assignment PIN_A8 -to lcd_b[1]
# set_location_assignment PIN_B9 -to lcd_b[0]
# set_location_assignment PIN_A9 -to lcd_g[7]
# set_location_assignment PIN_B10 -to lcd_g[6]
# set_location_assignment PIN_A10 -to lcd_g[5]
# set_location_assignment PIN_B11 -to lcd_g[4]
# set_location_assignment PIN_A11 -to lcd_g[3]
# set_location_assignment PIN_B12 -to lcd_g[2]
# set_location_assignment PIN_A12 -to lcd_g[1]
# set_location_assignment PIN_B13 -to lcd_g[0]
# set_location_assignment PIN_A13 -to lcd_r[7]
# set_location_assignment PIN_D5 -to lcd_r[6]
# set_location_assignment PIN_D6 -to lcd_r[5]
# set_location_assignment PIN_C6 -to lcd_r[4]
# set_location_assignment PIN_E7 -to lcd_r[3]
# set_location_assignment PIN_F8 -to lcd_r[2]
# set_location_assignment PIN_C8 -to lcd_r[1]
# set_location_assignment PIN_D8 -to lcd_r[0]

# set_location_assignment PIN_B5 -to lcd_dclk
# set_location_assignment PIN_A4 -to lcd_de
# set_location_assignment PIN_B4 -to lcd_hs
# set_location_assignment PIN_C2 -to lcd_pwm
# set_location_assignment PIN_A3 -to lcd_vs





