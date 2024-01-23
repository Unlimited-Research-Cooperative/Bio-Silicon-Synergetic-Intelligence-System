module uart_rx
#(
    parameter CLK_FRE = 50,      // Clock frequency (MHz)
    parameter BAUD_RATE = 128000 // Serial baud rate
)
(
    input clk,                    // Clock input
    input rst_n,                  // Asynchronous reset input, low active
    input rx_pin,                 // Serial data input
    output reg [7:0] out_channel_data[31:0], // Buffered channel data output
    output reg data_ready,                    // Data ready signal for i2s_tx
    input data_acknowledge                    // Data acknowledge from i2s_tx
);

localparam CYCLE = CLK_FRE * 1000000 / BAUD_RATE;

// State machine states
localparam S_IDLE = 1;
localparam S_START = 2;
localparam S_REC_BYTE = 3;
localparam S_STOP = 4;
localparam S_DATA = 5;
localparam S_PACKET_START = 6;
localparam S_CHANNEL_ID = 7;

reg [2:0] state, next_state;
reg rx_d0, rx_d1;
wire rx_negedge;
reg [7:0] rx_bits;
reg [15:0] cycle_cnt;
reg [2:0] bit_cnt;
reg [7:0] channel_id;

// Channel data buffer and new data flag
reg [7:0] channel_data_buffer[31:0];
reg new_data_flag;
reg [5:0] buffer_index;  // Used to iterate through buffers

assign rx_negedge = rx_d1 && ~rx_d0;

// Detect negative edge on rx_pin
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        rx_d0 <= 1'b1;
        rx_d1 <= 1'b1;
    end else begin
        rx_d0 <= rx_pin;
        rx_d1 <= rx_d0;
    end
end

// State machine for UART reception
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= S_IDLE;
    end else begin
        state <= next_state;
    end
end

// State transitions
always @(*) begin
    case (state)
        S_IDLE:
            if (rx_negedge)
                next_state <= S_START;
            else
                next_state <= S_IDLE;
        S_START:
            if (cycle_cnt == CYCLE/2 - 1)
                next_state <= S_REC_BYTE;
            else
                next_state <= S_START;
        S_REC_BYTE:
            if (cycle_cnt == CYCLE - 1 && bit_cnt == 7)
                next_state <= S_STOP;
            else
                next_state <= S_REC_BYTE;
        S_STOP:
            if (cycle_cnt == CYCLE/2 - 1)
                next_state <= S_DATA;
            else
                next_state <= S_STOP;
        S_DATA:
            if (rx_bits == 8'hAA)
                next_state <= S_PACKET_START;
            else
                next_state <= S_IDLE;
        S_PACKET_START:
            next_state <= S_CHANNEL_ID;
        S_CHANNEL_ID:
            next_state <= S_IDLE;
        default:
            next_state <= S_IDLE;
    endcase
end

// Receive bits and cycle count
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        cycle_cnt <= 0;
        bit_cnt <= 0;
        rx_bits <= 0;
        channel_id <= 0;
        new_data_flag <= 1'b0;
        data_ready <= 1'b0;
        buffer_index <= 0;
    end else begin
        if (state != next_state) begin
            cycle_cnt <= 0;
            if (state == S_REC_BYTE && cycle_cnt == CYCLE - 1)
                bit_cnt <= bit_cnt + 1;
            if (state == S_STOP)
                bit_cnt <= 0;
            if (state == S_REC_BYTE && cycle_cnt == CYCLE/2 - 1)
                rx_bits[bit_cnt] <= rx_pin;
            if (state == S_CHANNEL_ID && next_state == S_IDLE)
                channel_id <= rx_bits;
            if (state == S_CHANNEL_ID && next_state == S_IDLE && channel_id < 32) begin
                channel_data_buffer[channel_id] <= rx_bits;
                new_data_flag <= 1'b1;
            end
            if (new_data_flag) begin
                data_ready <= 1'b1;
                new_data_flag <= 1'b0;
            end
            if (data_acknowledge) begin
                data_ready <= 1'b0;
                out_channel_data[buffer_index] <= channel_data_buffer[buffer_index];
                buffer_index <= (buffer_index + 1) % 32;
            end
        end else begin
            cycle_cnt <= cycle_cnt + 1;
        end
    end
end

endmodule
