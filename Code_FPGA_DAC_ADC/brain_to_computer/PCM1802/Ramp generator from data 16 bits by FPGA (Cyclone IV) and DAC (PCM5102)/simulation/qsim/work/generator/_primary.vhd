library verilog;
use verilog.vl_types.all;
entity generator is
    port(
        CLK             : in     vl_logic;
        BCK             : out    vl_logic;
        DIN             : out    vl_logic;
        LCK             : out    vl_logic
    );
end generator;
