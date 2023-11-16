library verilog;
use verilog.vl_types.all;
entity Parallel_Serial_Converter_vlg_sample_tst is
    port(
        CLK             : in     vl_logic;
        parallel_in     : in     vl_logic_vector(15 downto 0);
        sampler_tx      : out    vl_logic
    );
end Parallel_Serial_Converter_vlg_sample_tst;
