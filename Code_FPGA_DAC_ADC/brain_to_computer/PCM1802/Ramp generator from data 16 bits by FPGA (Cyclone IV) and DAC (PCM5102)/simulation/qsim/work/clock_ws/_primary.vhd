library verilog;
use verilog.vl_types.all;
entity clock_ws is
    port(
        BCK             : in     vl_logic;
        LCK             : out    vl_logic
    );
end clock_ws;
