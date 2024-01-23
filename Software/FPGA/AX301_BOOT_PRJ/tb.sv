module tb;
   // Declare input and output ports
   logic clk;
   logic rst;
   logic [7:0] data_in;
   logic [7:0] data_out;

   // Instantiate your FPGA design module
   my_design my_instance (
      .clk(clk),
      .rst(rst),
      .data_in(data_in),
      .data_out(data_out)
   );

   // Clock Generation
   initial begin
      clk = 0;
      forever #5 clk = ~clk; // 100Hz clock (Toggle every 5 time units)
   end

   // Reset Generation
   initial begin
      rst = 1;
      #10 rst = 0; // Assert reset for 10 time units
   end

   // Stimulus Generation
   initial begin
      // Initialize your test vectors here
      // Example: Send 32 channels of 8-bit data every clock cycle
      repeat (100) begin // Simulate for 100 clock cycles
         data_in = $random % 256; // Generate random 8-bit data
         #1; // Wait one clock cycle
      end
      // Finish simulation gracefully
      $finish;
   end

   // Assertions (Optional)
   // Add assertions to check design behavior here

   // Coverage Analysis (Optional)
   // Add coverage analysis code here

   // Logging and Reporting (Optional)
   // Use $display, $write, or other methods for logs and reports

endmodule