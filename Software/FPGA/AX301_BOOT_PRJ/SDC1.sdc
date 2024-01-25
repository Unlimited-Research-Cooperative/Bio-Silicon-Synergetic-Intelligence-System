create_clock -name clk -period 20 [get_ports {clk}]


# Assume 'clk' is already defined as mentioned earlier
# Now create constraints for the derived clocks


# Constraint for LRCLK (Left Right Clock)
create_generated_clock -name lrclk -source [get_pins {<i2s_tx_instance_name>/bclk}] [get_pins {<i2s_tx_instance_name>/lrclk}]

# Constraint for Bit Clock (BCLK)
create_generated_clock -name bclk -source [get_ports clk] -divide_by <CLOCK_DIVISOR> [get_pins <instance_name>/bclk]

# Constraint for Master Clock (MCLK)
create_generated_clock -name mclk -source [get_ports clk] -divide_by <MCLK_DIVISOR> [get_pins <instance_name>/mclk]
