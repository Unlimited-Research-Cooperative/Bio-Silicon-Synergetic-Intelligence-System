module i2s_tx (
    input wire clk,            // Main clock input
    input wire reset,          // Reset input
    input wire [7:0] audio_l,  // Left audio data input
    input wire [7:0] audio_r,  // Right audio data input
    output reg bclk,           // Bit clock
    output reg lrclk,          // Left/Right clock
    output reg sdata           // Serial audio data output
);

// Parameters
parameter CLOCK_FREQ = 50000000;  // Main clock frequency in Hz
parameter SAMPLE_RATE = 48000;    // Audio sample rate in samples per second
parameter BIT_DEPTH = 8;          // Bit depth per audio sample

// Derived parameters
localparam BCLK_FREQ = SAMPLE_RATE * BIT_DEPTH * 2; // Bit clock frequency
localparam CLOCK_DIVISOR = CLOCK_FREQ / BCLK_FREQ;  // Clock division factor

// Counters
reg [31:0] bclk_counter = 0;      // Bit clock counter
reg [4:0] bit_counter = 0;        // Bit counter for serializing audio sample
reg [7:0] audio_sample = 0;       // Current audio sample being transmitted

// Main clock division for bclk generation
always @(posedge clk or posedge reset) begin
    if (reset) begin
        bclk_counter <= 0;
        bclk <= 0;
    end else begin
        if (bclk_counter >= CLOCK_DIVISOR/2 - 1) begin
            bclk_counter <= 0;
            bclk <= ~bclk; // Toggle bclk
        end else begin
            bclk_counter <= bclk_counter + 1;
        end
    end
end

// lrclk and sdata logic
always @(posedge bclk or posedge reset) begin
    if (reset) begin
        lrclk <= 1'b0;  // Start with left channel
        bit_counter <= 0;
        sdata <= 1'b0;
    end else begin
        if (bit_counter == (BIT_DEPTH * 2) - 1) begin
            bit_counter <= 0;
            lrclk <= ~lrclk; // Toggle lrclk on each new sample
        end else begin
            bit_counter <= bit_counter + 1;
        end

        // Choose the appropriate audio sample (left or right) and bit
        if (lrclk) begin
            audio_sample <= audio_l;
        end else begin
            audio_sample <= audio_r;
        end

        // Shift out the audio sample bits on sdata
        sdata <= audio_sample[BIT_DEPTH - 1 - (bit_counter % BIT_DEPTH)];
    end
end

endmodule

