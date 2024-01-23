module i2s_tx (
    input wire clk,
    input wire reset,
    input wire [7:0] audio_data[31:0],
    output reg bclk,
    output reg [15:0] lrclk,
    output reg sdata
);

parameter CLOCK_FREQ = 50000000;
parameter SAMPLE_RATE = 100;
parameter BIT_DEPTH = 8;

localparam BCLK_FREQ = SAMPLE_RATE * BIT_DEPTH * 2;
localparam CLOCK_DIVISOR = CLOCK_FREQ / BCLK_FREQ;

reg [31:0] bclk_counter = 0;
reg [4:0] bit_counter = 0;
reg [4:0] pair_counter = 0;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        bclk_counter <= 0;
        bclk <= 0;
    end else begin
        if (bclk_counter >= CLOCK_DIVISOR/2 - 1) begin
            bclk_counter <= 0;
            bclk <= ~bclk;
        end else begin
            bclk_counter <= bclk_counter + 1;
        end
    end
end

always @(posedge bclk or posedge reset) begin
    if (reset) begin
        lrclk <= 16'b0;
        bit_counter <= 0;
        sdata <= 1'b0;
        pair_counter <= 0;
    end else begin
        if (bit_counter == BIT_DEPTH - 1) begin
            bit_counter <= 0;
            lrclk <= ~lrclk;
            if (lrclk) begin
                pair_counter <= (pair_counter == 15) ? 0 : pair_counter + 1;
            end
        end else begin
            bit_counter <= bit_counter + 1;
        end
        // Calculate the audio_idx based on bit_counter and pair_counter
        if (pair_counter + bit_counter < 32)
            sdata <= audio_data[pair_counter + bit_counter][7];
        else
            sdata <= audio_data[pair_counter + bit_counter - 32][7];
    end
end

endmodule
