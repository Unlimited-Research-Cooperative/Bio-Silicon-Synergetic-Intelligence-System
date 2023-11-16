library verilog;
use verilog.vl_types.all;
entity clock_divider is
    port(
        CLK_IN          : in     vl_logic;
        CLK_OUT         : out    vl_logic
    );
end clock_divider;
