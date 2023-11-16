-- Copyright (C) 1991-2013 Altera Corporation
-- Your use of Altera Corporation's design tools, logic functions 
-- and other software and tools, and its AMPP partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Altera Program License 
-- Subscription Agreement, Altera MegaCore Function License 
-- Agreement, or other applicable license agreement, including, 
-- without limitation, that your use is for the sole purpose of 
-- programming logic devices manufactured by Altera and sold by 
-- Altera or its authorized distributors.  Please refer to the 
-- applicable agreement for further details.

-- VENDOR "Altera"
-- PROGRAM "Quartus II 64-Bit"
-- VERSION "Version 13.1.0 Build 162 10/23/2013 SJ Web Edition"

-- DATE "10/19/2020 16:45:13"

-- 
-- Device: Altera EP4CE10E22C8 Package TQFP144
-- 

-- 
-- This VHDL file should be used for ModelSim-Altera (VHDL) only
-- 

LIBRARY ALTERA;
LIBRARY CYCLONEIVE;
LIBRARY IEEE;
USE ALTERA.ALTERA_PRIMITIVES_COMPONENTS.ALL;
USE CYCLONEIVE.CYCLONEIVE_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	Parallel_Serial_Converter IS
    PORT (
	CLK : IN std_logic;
	parallel_in : IN std_logic_vector(16 DOWNTO 0);
	serial_out : OUT std_logic
	);
END Parallel_Serial_Converter;

-- Design Ports Information
-- serial_out	=>  Location: PIN_10,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[0]	=>  Location: PIN_43,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[6]	=>  Location: PIN_28,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[7]	=>  Location: PIN_39,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[8]	=>  Location: PIN_38,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[5]	=>  Location: PIN_30,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[11]	=>  Location: PIN_33,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[10]	=>  Location: PIN_11,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[12]	=>  Location: PIN_32,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[9]	=>  Location: PIN_44,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[14]	=>  Location: PIN_34,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[15]	=>  Location: PIN_31,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[16]	=>  Location: PIN_24,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[13]	=>  Location: PIN_25,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[3]	=>  Location: PIN_42,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[2]	=>  Location: PIN_50,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[4]	=>  Location: PIN_49,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- parallel_in[1]	=>  Location: PIN_46,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- CLK	=>  Location: PIN_23,	 I/O Standard: 2.5 V,	 Current Strength: Default


ARCHITECTURE structure OF Parallel_Serial_Converter IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_CLK : std_logic;
SIGNAL ww_parallel_in : std_logic_vector(16 DOWNTO 0);
SIGNAL ww_serial_out : std_logic;
SIGNAL \CLK~inputclkctrl_INCLK_bus\ : std_logic_vector(3 DOWNTO 0);
SIGNAL \serial_out~output_o\ : std_logic;
SIGNAL \CLK~input_o\ : std_logic;
SIGNAL \CLK~inputclkctrl_outclk\ : std_logic;
SIGNAL \parallel_in[0]~input_o\ : std_logic;
SIGNAL \count[0]~5_combout\ : std_logic;
SIGNAL \LessThan0~0_combout\ : std_logic;
SIGNAL \LessThan0~1_combout\ : std_logic;
SIGNAL \count[0]~6\ : std_logic;
SIGNAL \count[1]~7_combout\ : std_logic;
SIGNAL \count[1]~8\ : std_logic;
SIGNAL \count[2]~9_combout\ : std_logic;
SIGNAL \count[2]~10\ : std_logic;
SIGNAL \count[3]~11_combout\ : std_logic;
SIGNAL \count[3]~12\ : std_logic;
SIGNAL \count[4]~13_combout\ : std_logic;
SIGNAL \parallel_in[5]~input_o\ : std_logic;
SIGNAL \parallel_in[6]~input_o\ : std_logic;
SIGNAL \parallel_in[8]~input_o\ : std_logic;
SIGNAL \parallel_in[7]~input_o\ : std_logic;
SIGNAL \Mux0~0_combout\ : std_logic;
SIGNAL \Mux0~1_combout\ : std_logic;
SIGNAL \parallel_in[3]~input_o\ : std_logic;
SIGNAL \parallel_in[1]~input_o\ : std_logic;
SIGNAL \parallel_in[4]~input_o\ : std_logic;
SIGNAL \parallel_in[2]~input_o\ : std_logic;
SIGNAL \Mux0~7_combout\ : std_logic;
SIGNAL \Mux0~8_combout\ : std_logic;
SIGNAL \parallel_in[14]~input_o\ : std_logic;
SIGNAL \parallel_in[13]~input_o\ : std_logic;
SIGNAL \parallel_in[15]~input_o\ : std_logic;
SIGNAL \parallel_in[16]~input_o\ : std_logic;
SIGNAL \Mux0~4_combout\ : std_logic;
SIGNAL \Mux0~5_combout\ : std_logic;
SIGNAL \parallel_in[9]~input_o\ : std_logic;
SIGNAL \parallel_in[11]~input_o\ : std_logic;
SIGNAL \parallel_in[12]~input_o\ : std_logic;
SIGNAL \parallel_in[10]~input_o\ : std_logic;
SIGNAL \Mux0~2_combout\ : std_logic;
SIGNAL \Mux0~3_combout\ : std_logic;
SIGNAL \Mux0~6_combout\ : std_logic;
SIGNAL \Mux0~9_combout\ : std_logic;
SIGNAL \Mux0~10_combout\ : std_logic;
SIGNAL \serial_out~reg0_q\ : std_logic;
SIGNAL count : std_logic_vector(4 DOWNTO 0);

BEGIN

ww_CLK <= CLK;
ww_parallel_in <= parallel_in;
serial_out <= ww_serial_out;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\CLK~inputclkctrl_INCLK_bus\ <= (vcc & vcc & vcc & \CLK~input_o\);

-- Location: IOOBUF_X0_Y18_N16
\serial_out~output\ : cycloneive_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \serial_out~reg0_q\,
	devoe => ww_devoe,
	o => \serial_out~output_o\);

-- Location: IOIBUF_X0_Y11_N8
\CLK~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_CLK,
	o => \CLK~input_o\);

-- Location: CLKCTRL_G2
\CLK~inputclkctrl\ : cycloneive_clkctrl
-- pragma translate_off
GENERIC MAP (
	clock_type => "global clock",
	ena_register_mode => "none")
-- pragma translate_on
PORT MAP (
	inclk => \CLK~inputclkctrl_INCLK_bus\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	outclk => \CLK~inputclkctrl_outclk\);

-- Location: IOIBUF_X5_Y0_N22
\parallel_in[0]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(0),
	o => \parallel_in[0]~input_o\);

-- Location: LCCOMB_X1_Y4_N6
\count[0]~5\ : cycloneive_lcell_comb
-- Equation(s):
-- \count[0]~5_combout\ = count(0) $ (VCC)
-- \count[0]~6\ = CARRY(count(0))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101010110101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => count(0),
	datad => VCC,
	combout => \count[0]~5_combout\,
	cout => \count[0]~6\);

-- Location: LCCOMB_X1_Y4_N0
\LessThan0~0\ : cycloneive_lcell_comb
-- Equation(s):
-- \LessThan0~0_combout\ = (count(0)) # ((count(1)) # ((count(3)) # (count(2))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111111111110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => count(0),
	datab => count(1),
	datac => count(3),
	datad => count(2),
	combout => \LessThan0~0_combout\);

-- Location: LCCOMB_X1_Y4_N30
\LessThan0~1\ : cycloneive_lcell_comb
-- Equation(s):
-- \LessThan0~1_combout\ = (count(4) & \LessThan0~0_combout\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => count(4),
	datad => \LessThan0~0_combout\,
	combout => \LessThan0~1_combout\);

-- Location: FF_X1_Y4_N7
\count[0]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \CLK~inputclkctrl_outclk\,
	d => \count[0]~5_combout\,
	sclr => \LessThan0~1_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => count(0));

-- Location: LCCOMB_X1_Y4_N8
\count[1]~7\ : cycloneive_lcell_comb
-- Equation(s):
-- \count[1]~7_combout\ = (count(1) & (!\count[0]~6\)) # (!count(1) & ((\count[0]~6\) # (GND)))
-- \count[1]~8\ = CARRY((!\count[0]~6\) # (!count(1)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0011110000111111",
	sum_lutc_input => "cin")
-- pragma translate_on
PORT MAP (
	datab => count(1),
	datad => VCC,
	cin => \count[0]~6\,
	combout => \count[1]~7_combout\,
	cout => \count[1]~8\);

-- Location: FF_X1_Y4_N9
\count[1]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \CLK~inputclkctrl_outclk\,
	d => \count[1]~7_combout\,
	sclr => \LessThan0~1_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => count(1));

-- Location: LCCOMB_X1_Y4_N10
\count[2]~9\ : cycloneive_lcell_comb
-- Equation(s):
-- \count[2]~9_combout\ = (count(2) & (\count[1]~8\ $ (GND))) # (!count(2) & (!\count[1]~8\ & VCC))
-- \count[2]~10\ = CARRY((count(2) & !\count[1]~8\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010010100001010",
	sum_lutc_input => "cin")
-- pragma translate_on
PORT MAP (
	dataa => count(2),
	datad => VCC,
	cin => \count[1]~8\,
	combout => \count[2]~9_combout\,
	cout => \count[2]~10\);

-- Location: FF_X1_Y4_N11
\count[2]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \CLK~inputclkctrl_outclk\,
	d => \count[2]~9_combout\,
	sclr => \LessThan0~1_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => count(2));

-- Location: LCCOMB_X1_Y4_N12
\count[3]~11\ : cycloneive_lcell_comb
-- Equation(s):
-- \count[3]~11_combout\ = (count(3) & (!\count[2]~10\)) # (!count(3) & ((\count[2]~10\) # (GND)))
-- \count[3]~12\ = CARRY((!\count[2]~10\) # (!count(3)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101101001011111",
	sum_lutc_input => "cin")
-- pragma translate_on
PORT MAP (
	dataa => count(3),
	datad => VCC,
	cin => \count[2]~10\,
	combout => \count[3]~11_combout\,
	cout => \count[3]~12\);

-- Location: FF_X1_Y4_N13
\count[3]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \CLK~inputclkctrl_outclk\,
	d => \count[3]~11_combout\,
	sclr => \LessThan0~1_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => count(3));

-- Location: LCCOMB_X1_Y4_N14
\count[4]~13\ : cycloneive_lcell_comb
-- Equation(s):
-- \count[4]~13_combout\ = count(4) $ (!\count[3]~12\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100001111000011",
	sum_lutc_input => "cin")
-- pragma translate_on
PORT MAP (
	datab => count(4),
	cin => \count[3]~12\,
	combout => \count[4]~13_combout\);

-- Location: FF_X1_Y4_N15
\count[4]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \CLK~inputclkctrl_outclk\,
	d => \count[4]~13_combout\,
	sclr => \LessThan0~1_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => count(4));

-- Location: IOIBUF_X0_Y8_N15
\parallel_in[5]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(5),
	o => \parallel_in[5]~input_o\);

-- Location: IOIBUF_X0_Y9_N8
\parallel_in[6]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(6),
	o => \parallel_in[6]~input_o\);

-- Location: IOIBUF_X1_Y0_N22
\parallel_in[8]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(8),
	o => \parallel_in[8]~input_o\);

-- Location: IOIBUF_X1_Y0_N15
\parallel_in[7]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(7),
	o => \parallel_in[7]~input_o\);

-- Location: LCCOMB_X1_Y4_N22
\Mux0~0\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~0_combout\ = (count(1) & (((count(0))))) # (!count(1) & ((count(0) & ((\parallel_in[7]~input_o\))) # (!count(0) & (\parallel_in[8]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110000001010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[8]~input_o\,
	datab => \parallel_in[7]~input_o\,
	datac => count(1),
	datad => count(0),
	combout => \Mux0~0_combout\);

-- Location: LCCOMB_X1_Y4_N4
\Mux0~1\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~1_combout\ = (\Mux0~0_combout\ & ((\parallel_in[5]~input_o\) # ((!count(1))))) # (!\Mux0~0_combout\ & (((\parallel_in[6]~input_o\ & count(1)))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010110011110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[5]~input_o\,
	datab => \parallel_in[6]~input_o\,
	datac => \Mux0~0_combout\,
	datad => count(1),
	combout => \Mux0~1_combout\);

-- Location: IOIBUF_X3_Y0_N1
\parallel_in[3]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(3),
	o => \parallel_in[3]~input_o\);

-- Location: IOIBUF_X7_Y0_N1
\parallel_in[1]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(1),
	o => \parallel_in[1]~input_o\);

-- Location: IOIBUF_X13_Y0_N15
\parallel_in[4]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(4),
	o => \parallel_in[4]~input_o\);

-- Location: IOIBUF_X13_Y0_N1
\parallel_in[2]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(2),
	o => \parallel_in[2]~input_o\);

-- Location: LCCOMB_X2_Y4_N0
\Mux0~7\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~7_combout\ = (count(0) & (((count(1))))) # (!count(0) & ((count(1) & ((\parallel_in[2]~input_o\))) # (!count(1) & (\parallel_in[4]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110000001010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[4]~input_o\,
	datab => \parallel_in[2]~input_o\,
	datac => count(0),
	datad => count(1),
	combout => \Mux0~7_combout\);

-- Location: LCCOMB_X2_Y4_N30
\Mux0~8\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~8_combout\ = (count(0) & ((\Mux0~7_combout\ & ((\parallel_in[1]~input_o\))) # (!\Mux0~7_combout\ & (\parallel_in[3]~input_o\)))) # (!count(0) & (((\Mux0~7_combout\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100111110100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[3]~input_o\,
	datab => \parallel_in[1]~input_o\,
	datac => count(0),
	datad => \Mux0~7_combout\,
	combout => \Mux0~8_combout\);

-- Location: IOIBUF_X0_Y5_N15
\parallel_in[14]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(14),
	o => \parallel_in[14]~input_o\);

-- Location: IOIBUF_X0_Y11_N22
\parallel_in[13]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(13),
	o => \parallel_in[13]~input_o\);

-- Location: IOIBUF_X0_Y7_N1
\parallel_in[15]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(15),
	o => \parallel_in[15]~input_o\);

-- Location: IOIBUF_X0_Y11_N15
\parallel_in[16]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(16),
	o => \parallel_in[16]~input_o\);

-- Location: LCCOMB_X1_Y4_N20
\Mux0~4\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~4_combout\ = (count(1) & (((count(0))))) # (!count(1) & ((count(0) & (\parallel_in[15]~input_o\)) # (!count(0) & ((\parallel_in[16]~input_o\)))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111101000001100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[15]~input_o\,
	datab => \parallel_in[16]~input_o\,
	datac => count(1),
	datad => count(0),
	combout => \Mux0~4_combout\);

-- Location: LCCOMB_X1_Y4_N26
\Mux0~5\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~5_combout\ = (count(1) & ((\Mux0~4_combout\ & ((\parallel_in[13]~input_o\))) # (!\Mux0~4_combout\ & (\parallel_in[14]~input_o\)))) # (!count(1) & (((\Mux0~4_combout\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100111110100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[14]~input_o\,
	datab => \parallel_in[13]~input_o\,
	datac => count(1),
	datad => \Mux0~4_combout\,
	combout => \Mux0~5_combout\);

-- Location: IOIBUF_X5_Y0_N15
\parallel_in[9]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(9),
	o => \parallel_in[9]~input_o\);

-- Location: IOIBUF_X0_Y6_N22
\parallel_in[11]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(11),
	o => \parallel_in[11]~input_o\);

-- Location: IOIBUF_X0_Y6_N15
\parallel_in[12]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(12),
	o => \parallel_in[12]~input_o\);

-- Location: IOIBUF_X0_Y18_N22
\parallel_in[10]~input\ : cycloneive_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_parallel_in(10),
	o => \parallel_in[10]~input_o\);

-- Location: LCCOMB_X1_Y4_N28
\Mux0~2\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~2_combout\ = (count(1) & (((\parallel_in[10]~input_o\) # (count(0))))) # (!count(1) & (\parallel_in[12]~input_o\ & ((!count(0)))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000011001010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \parallel_in[12]~input_o\,
	datab => \parallel_in[10]~input_o\,
	datac => count(1),
	datad => count(0),
	combout => \Mux0~2_combout\);

-- Location: LCCOMB_X1_Y4_N18
\Mux0~3\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~3_combout\ = (count(0) & ((\Mux0~2_combout\ & (\parallel_in[9]~input_o\)) # (!\Mux0~2_combout\ & ((\parallel_in[11]~input_o\))))) # (!count(0) & (((\Mux0~2_combout\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1101110110100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => count(0),
	datab => \parallel_in[9]~input_o\,
	datac => \parallel_in[11]~input_o\,
	datad => \Mux0~2_combout\,
	combout => \Mux0~3_combout\);

-- Location: LCCOMB_X1_Y4_N24
\Mux0~6\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~6_combout\ = (count(2) & ((count(3)) # ((\Mux0~3_combout\)))) # (!count(2) & (!count(3) & (\Mux0~5_combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1011101010011000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => count(2),
	datab => count(3),
	datac => \Mux0~5_combout\,
	datad => \Mux0~3_combout\,
	combout => \Mux0~6_combout\);

-- Location: LCCOMB_X1_Y4_N2
\Mux0~9\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~9_combout\ = (count(3) & ((\Mux0~6_combout\ & ((\Mux0~8_combout\))) # (!\Mux0~6_combout\ & (\Mux0~1_combout\)))) # (!count(3) & (((\Mux0~6_combout\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111010110001000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => count(3),
	datab => \Mux0~1_combout\,
	datac => \Mux0~8_combout\,
	datad => \Mux0~6_combout\,
	combout => \Mux0~9_combout\);

-- Location: LCCOMB_X1_Y4_N16
\Mux0~10\ : cycloneive_lcell_comb
-- Equation(s):
-- \Mux0~10_combout\ = (count(4) & (\parallel_in[0]~input_o\)) # (!count(4) & ((\Mux0~9_combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100111111000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \parallel_in[0]~input_o\,
	datac => count(4),
	datad => \Mux0~9_combout\,
	combout => \Mux0~10_combout\);

-- Location: FF_X1_Y4_N17
\serial_out~reg0\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \CLK~inputclkctrl_outclk\,
	d => \Mux0~10_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \serial_out~reg0_q\);

ww_serial_out <= \serial_out~output_o\;
END structure;


