library verilog;
use verilog.vl_types.all;
entity Parallel_Serial_Converter_vlg_check_tst is
    port(
        serial_out      : in     vl_logic;
        sampler_rx      : in     vl_logic
    );
end Parallel_Serial_Converter_vlg_check_tst;
