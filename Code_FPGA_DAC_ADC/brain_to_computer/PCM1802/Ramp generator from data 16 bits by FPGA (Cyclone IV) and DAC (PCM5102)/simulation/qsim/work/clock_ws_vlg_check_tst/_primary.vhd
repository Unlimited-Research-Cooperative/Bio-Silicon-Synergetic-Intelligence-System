library verilog;
use verilog.vl_types.all;
entity clock_ws_vlg_check_tst is
    port(
        LCK             : in     vl_logic;
        sampler_rx      : in     vl_logic
    );
end clock_ws_vlg_check_tst;
