library verilog;
use verilog.vl_types.all;
entity clock_ws_vlg_sample_tst is
    port(
        BCK             : in     vl_logic;
        sampler_tx      : out    vl_logic
    );
end clock_ws_vlg_sample_tst;
