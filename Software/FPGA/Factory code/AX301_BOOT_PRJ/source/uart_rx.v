module uart_rx
#(
    parameter CLK_FRE = 50,      //clock frequency(Mhz)
    parameter BAUD_RATE = 115200 //serial baud rate
)
(
    input                        clk,              //clock input
    input                        rst_n,            //asynchronous reset input, low active 
    output reg[7:0]              rx_data,          //received serial data
    output reg                   rx_data_valid,    //received serial data is valid
    input                        rx_data_ready,    //data receiver module ready
    input                        rx_pin            //serial data input
);
//calculates the clock cycle for baud rate 
localparam                       CYCLE = CLK_FRE * 1000000 / BAUD_RATE;
//state machine code
localparam                       S_IDLE      = 1;
localparam                       S_START     = 2; //start bit
localparam                       S_REC_BYTE  = 3; //data bits
localparam                       S_STOP      = 4; //stop bit
localparam                       S_DATA      = 5;
localparam                       S_PACKET_START = 6; // New state for packet start
localparam                       S_CHANNEL_ID   = 7; // New state for channel ID

reg[2:0]                         state;
reg[2:0]                         next_state;
reg                              rx_d0;            //delay 1 clock for rx_pin
reg                              rx_d1;            //delay 1 clock for rx_d0
wire                             rx_negedge;       //negedge of rx_pin
reg[7:0]                         rx_bits;          //temporary storage of received data
reg[15:0]                        cycle_cnt;        //baud counter
reg[2:0]                         bit_cnt;          //bit counter
reg[7:0]                         channel_id;       // New variable for channel ID

assign rx_negedge = rx_d1 && ~rx_d0;

always@(posedge clk or negedge rst_n)
begin
    if(rst_n == 1'b0)
    begin
        rx_d0 <= 1'b0;
        rx_d1 <= 1'b0; 
    end
    else
    begin
        rx_d0 <= rx_pin;
        rx_d1 <= rx_d0;
    end
end

always@(posedge clk or negedge rst_n)
begin
    if(rst_n == 1'b0)
        state <= S_IDLE;
    else
        state <= next_state;
end

always@(*)
begin
    case(state)
        S_IDLE:
            if(rx_negedge)
                next_state <= S_START;
            else
                next_state <= S_IDLE;
        S_START:
            if(cycle_cnt == CYCLE - 1) //one data cycle 
                next_state <= S_REC_BYTE;
            else
                next_state <= S_START;
        S_REC_BYTE:
            if(cycle_cnt == CYCLE - 1 && bit_cnt == 3'd7)  //receive 8bit data
                next_state <= S_STOP;
            else
                next_state <= S_REC_BYTE;
        S_STOP:
            if(cycle_cnt == CYCLE/2 - 1) //half bit cycle,to avoid missing the next byte receiver
                next_state <= S_DATA;
            else
                next_state <= S_STOP;
        S_DATA:
            if(rx_data_ready) //data receive complete
            begin
                if(rx_bits == 8'hAA) // Start byte
                    next_state <= S_PACKET_START;
                else
                    next_state <= S_IDLE;
            end
            else
                next_state <= S_DATA;
        S_PACKET_START:
            next_state <= S_CHANNEL_ID;
        S_CHANNEL_ID:
            begin
                channel_id <= rx_bits; // Capture the channel identifier
                next_state <= S_IDLE;  // Or next state to handle data
            end
        default:
            next_state <= S_IDLE;
    endcase
end


always@(posedge clk or negedge rst_n)
begin
	if(rst_n == 1'b0)
		rx_data_valid <= 1'b0;
	else if(state == S_STOP && next_state != state)
		rx_data_valid <= 1'b1;
	else if(state == S_DATA && rx_data_ready)
		rx_data_valid <= 1'b0;
end

always@(posedge clk or negedge rst_n)
begin
	if(rst_n == 1'b0)
		rx_data <= 8'd0;
	else if(state == S_STOP && next_state != state)
		rx_data <= rx_bits;//latch received data
end

always@(posedge clk or negedge rst_n)
begin
	if(rst_n == 1'b0)
		begin
			bit_cnt <= 3'd0;
		end
	else if(state == S_REC_BYTE)
		if(cycle_cnt == CYCLE - 1)
			bit_cnt <= bit_cnt + 3'd1;
		else
			bit_cnt <= bit_cnt;
	else
		bit_cnt <= 3'd0;
end


always@(posedge clk or negedge rst_n)
begin
	if(rst_n == 1'b0)
		cycle_cnt <= 16'd0;
	else if((state == S_REC_BYTE && cycle_cnt == CYCLE - 1) || next_state != state)
		cycle_cnt <= 16'd0;
	else
		cycle_cnt <= cycle_cnt + 16'd1;	
end
//receive serial data bit data
always@(posedge clk or negedge rst_n)
begin
	if(rst_n == 1'b0)
		rx_bits <= 8'd0;
	else if(state == S_REC_BYTE && cycle_cnt == CYCLE/2 - 1)
		rx_bits[bit_cnt] <= rx_pin;
	else
		rx_bits <= rx_bits; 
end

// Logic for handling channel_id and rx_bits
reg [7:0] channel_1_data, channel_2_data; // Registers for each channel's data

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // Reset logic for channel data
        channel_1_data <= 8'd0;
        channel_2_data <= 8'd0;
    end else if (state == S_CHANNEL_ID && next_state == S_IDLE) begin
        // Store received data in corresponding channel register
        case (channel_id)
            8'h01: channel_1_data <= rx_bits; // Channel 1 identifier
            8'h02: channel_2_data <= rx_bits; // Channel 2 identifier
            // Add cases for more channels if needed
            default: ; // Do nothing for unrecognized channel IDs
        endcase
    end
end

// Output or further processing of channel data
// Here, you can add logic to output the data or send it to another module for further processing.
// For instance, you might output the data to another part of your system:
output reg [7:0] out_channel_1_data, out_channel_2_data;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        out_channel_1_data <= 8'd0;
        out_channel_2_data <= 8'd0;
    end else begin
        // Update output registers with the latest data
        out_channel_1_data <= channel_1_data;
        out_channel_2_data <= channel_2_data;
    end
end
// ... (rest of the module)
endmodule 
