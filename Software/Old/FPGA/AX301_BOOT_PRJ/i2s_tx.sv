module i2s_tx (
    input wire clk,
    input wire reset,
    input wire [7:0] audio_data[31:0],
    output reg bclk,
    output reg [15:0] lrclk,
    output reg sdata,
    output reg mclk // Added output for MCLK
);

parameter CLOCK_FREQ = 50000000;
parameter SAMPLE_RATE = 100;
parameter BIT_DEPTH = 8;

localparam BCLK_FREQ = SAMPLE_RATE * BIT_DEPTH * 2;
localparam MCLK_FREQ = SAMPLE_RATE * 256; // MCLK is 256x LRCLK
localparam CLOCK_DIVISOR = CLOCK_FREQ / BCLK_FREQ;
localparam MCLK_DIVISOR = CLOCK_FREQ / MCLK_FREQ; // Divider for MCLK

reg [31:0] bclk_counter = 0;
reg [31:0] mclk_counter = 0; // Counter for MCLK
reg [4:0] bit_counter = 0;
reg [4:0] pair_counter = 0;

// Generate BCLK
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

// Generate LRCLK
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
        sdata <= audio_data[pair_counter][bit_counter];
    end
end

// Generate MCLK
always @(posedge clk or posedge reset) begin
    if (reset) begin
        mclk_counter <= 0;
        mclk <= 0;
    end else begin
        if (mclk_counter >= MCLK_DIVISOR/2 - 1) begin
            mclk_counter <= 0;
            mclk <= ~mclk;
        end else begin
            mclk_counter <= mclk_counter + 1;
        end
    end
end

endmodule
