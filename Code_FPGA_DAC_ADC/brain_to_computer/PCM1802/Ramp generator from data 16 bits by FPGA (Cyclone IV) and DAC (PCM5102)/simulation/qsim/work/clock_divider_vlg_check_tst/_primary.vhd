library verilog;
use verilog.vl_types.all;
entity clock_divider_vlg_check_tst is
    port(
        CLK_OUT         : in     vl_logic;
        sampler_rx      : in     vl_logic
    );
end clock_divider_vlg_check_tst;
