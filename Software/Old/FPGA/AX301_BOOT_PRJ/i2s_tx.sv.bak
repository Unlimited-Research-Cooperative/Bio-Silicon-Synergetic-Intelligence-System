module i2s_tx (
    input wire clk,                     // Main clock input
    input wire reset,                   // Reset input
    input wire [7:0] audio_data[31:0],  // Array of 32 channels (16 pairs) of audio data
    output reg bclk,                    // Bit clock
    output reg [15:0] lrclk,            // Left/Right clock for each DAC pair
    output reg [15:0] sdata             // Serial audio data output for each DAC pair
);

// Parameters
parameter CLOCK_FREQ = 50000000;       // Main clock frequency in Hz
parameter SAMPLE_RATE = 100;           // Audio sample rate in samples per second 
parameter BIT_DEPTH = 8;               // Bit depth per audio sample

// Derived parameters
localparam BCLK_FREQ = SAMPLE_RATE * BIT_DEPTH * 2; // Bit clock frequency
localparam CLOCK_DIVISOR = CLOCK_FREQ / BCLK_FREQ;  // Clock division factor

// Counters
reg [31:0] bclk_counter = 0;           // Bit clock counter
reg [4:0] bit_counter = 0;             // Bit counter for serializing audio sample
reg [4:0] pair_counter = 0;            // Counter to cycle through pairs of channels

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

// lrclk and sdata logic for multiple DACs
always @(posedge bclk or posedge reset) begin
    if (reset) begin
        // Reset logic
        lrclk <= 16'b0;
        bit_counter <= 0;
        sdata <= 16'b0;
        pair_counter <= 0;
    end else begin
        if (bit_counter == BIT_DEPTH - 1) begin
            bit_counter <= 0;
            lrclk <= ~lrclk; // Toggle lrclk for each DAC pair
            if (&lrclk) begin  // All lrclk bits are high
                pair_counter <= (pair_counter == 15) ? 0 : pair_counter + 1;
            end
        end else begin
            bit_counter <= bit_counter + 1;
        end
        // Shift out the bits of the audio samples
        if (bit_counter == BIT_DEPTH - 1) begin
            bit_counter <= 0;
            lrclk <= ~lrclk;
            if (&lrclk) begin
                pair_counter <= (pair_counter == 15) ? 0 : pair_counter + 1;
            end
        end else begin
            bit_counter <= bit_counter + 1;
        end
    end
end
// Use generate block to assign audio data bits to sdata
genvar i;
generate
    for (i = 0; i < 16; i = i + 1) begin: gen_audio_output
        always @(posedge bclk or posedge reset) begin
            if (reset) begin
                sdata[i] <= 0;
            end else begin
                // Correctly index the audio_data bits
                int start_idx = pair_counter * 16 + i * 8;
                sdata[i] <= audio_data[start_idx +: 8][BIT_DEPTH - 1 - bit_counter]; // [+:] is a part-select operator
            end
        end
    end
endgenerate

endmodule