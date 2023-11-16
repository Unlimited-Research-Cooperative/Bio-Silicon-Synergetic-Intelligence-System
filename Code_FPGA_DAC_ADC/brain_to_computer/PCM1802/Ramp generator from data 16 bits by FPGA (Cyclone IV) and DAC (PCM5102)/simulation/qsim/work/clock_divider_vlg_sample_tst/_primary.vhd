library verilog;
use verilog.vl_types.all;
entity clock_divider_vlg_sample_tst is
    port(
        CLK_IN          : in     vl_logic;
        sampler_tx      : out    vl_logic
    );
end clock_divider_vlg_sample_tst;
