module top_module (
    input wire clk,             // Main system clock
    input wire rst_n,           // Asynchronous reset, active low
    input wire uart_rx,         // UART receive line from FT232RL
    output wire uart_tx,        // UART transmit line to FT232RL
    // ... other I/O definitions ...
);

// UART Parameters (modify as needed)
parameter CLK_FRE = 50;        // Clock frequency in MHz
parameter BAUD_RATE = 115200;  // UART baud rate

// UART RX Module
wire [7:0] rx_data;            // Received data
wire rx_data_valid;            // Data valid signal
wire rx_data_ready = 1'b1;     // Always ready to receive data

uart_rx #(
    .CLK_FRE(CLK_FRE),
    .BAUD_RATE(BAUD_RATE)
) uart_receiver (
    .clk(clk),
    .rst_n(rst_n),
    .rx_data(rx_data),
    .rx_data_valid(rx_data_valid),
    .rx_data_ready(rx_data_ready),
    .rx_pin(uart_rx)
);

// UART TX Module
wire [7:0] tx_data;            // Data to transmit
wire tx_data_valid;            // Data valid signal for transmission
wire tx_data_ready;            // Signal indicating ready to transmit next byte

uart_tx #(
    .CLK_FRE(CLK_FRE),
    .BAUD_RATE(BAUD_RATE)
) uart_transmitter (
    .clk(clk),
    .rst_n(rst_n),
    .tx_data(tx_data),
    .tx_data_valid(tx_data_valid),
    .tx_data_ready(tx_data_ready),
    .tx_pin(uart_tx)
);

// ... additional logic for handling UART data ...

endmodule

