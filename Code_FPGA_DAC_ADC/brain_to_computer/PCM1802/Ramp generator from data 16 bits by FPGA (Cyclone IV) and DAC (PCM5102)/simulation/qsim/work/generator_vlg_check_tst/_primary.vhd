library verilog;
use verilog.vl_types.all;
entity generator_vlg_check_tst is
    port(
        BCK             : in     vl_logic;
        DIN             : in     vl_logic;
        LCK             : in     vl_logic;
        sampler_rx      : in     vl_logic
    );
end generator_vlg_check_tst;
