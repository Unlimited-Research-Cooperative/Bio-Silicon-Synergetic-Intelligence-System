module top(
    input                      clk,
    input                      rst_n,
    input                      key2,
	output [3:0]               led,

	   //rtc ds1302 port
       output                     rtc_sclk,
       output                     rtc_ce,
       inout                      rtc_data,
       input                      uart_rx,
       output                     uart_tx,	
       //i2c eeprom port
       input                      key3,
       inout                      i2c_sda,
       inout                      i2c_scl,
	


       //sd audio port
	    input                      key4,		 
		 output reg [5:0]           seg_sel,
       output reg [7:0]           seg_data,
		 //buzzer port
		 output                     buzzer,		
		 //SD card port
	    output                     SD_nCS,
	    output                     SD_DCLK,
	    output                     SD_MOSI,
	    input                      SD_MISO,                              
	    //ov5640 and sdram port
	    inout                      cmos_scl,          //cmos i2c clock
	    inout                      cmos_sda,          //cmos i2c data
	    input                      cmos_vsync,        //cmos vsync
	    input                      cmos_href,         //cmos hsync refrence,data valid
	    input                      cmos_pclk,         //cmos pxiel clock
	    output                     cmos_xclk,         //cmos externl clock
	    input   [7:0]              cmos_db,           //cmos data 
		output                     cmos_rst_n,        //cmos reset
	    output                     cmos_pwdn,         //cmos power down
	  
       //sdram port
	    output                     sdram_clk,         //sdram clock
	    output                     sdram_cke,         //sdram clock enable
	    output                     sdram_cs_n,        //sdram chip select
	    output                     sdram_we_n,        //sdram write enable
	    output                     sdram_cas_n,       //sdram column address strobe
	    output                     sdram_ras_n,       //sdram row address strobe
	    output  [1:0]              sdram_dqm,         //sdram data enable
	    output  [1:0]              sdram_ba,          //sdram bank address
	    output  [12:0]             sdram_addr,        //sdram address
	    inout   [15:0]             sdram_dq           //sdram data  
	 
);

// Declare uart_rx to i2s_tx interface signals
wire [7:0] audio_data[31:0];  // Unpacked array of 32 channels (8 bits each)
wire uart_data_ready;         // UART data ready signal
reg i2s_data_acknowledge;     // I2S data acknowledge signal

// Instance of uart_rx
uart_rx uart_receiver_inst (
    .clk(clk),
    .rst_n(rst_n),
    .rx_pin(uart_rx),
    .out_channel_data(audio_data),  // 32 channels of audio data
    .data_ready(uart_data_ready),   // Data ready signal from uart_rx
    .data_acknowledge(i2s_data_acknowledge)  // Acknowledge signal to uart_rx
);


// I2S Transmitter instance
i2s_tx i2s_transmitter_inst (
    .clk(clk),
    .reset(~rst_n),
    .audio_data(audio_data),   // Audio data from uart_rx
    .bclk(i2s_bclk),
    .lrclk(i2s_lrclk),
    .sdata(i2s_sdata)
);
    
localparam    idle           = 2'd0 ;
localparam    ledflash_mode  = 2'd1 ;
localparam    eeprom_mode    = 2'd2 ;
localparam    sd_mode        = 2'd3 ;

reg [1:0]       current_state     ;
reg [1:0]       next_state        ;

wire            button_negedge2   ;
wire            button_negedge3   ;
wire            button_negedge4   ;
  
reg  [24:0]     blinking_cnt ;

wire [5:0]      rtc_seg_sel ; 
wire [7:0]      rtc_seg_data ; 
wire [5:0]      eeprom_seg_sel ; 
wire [7:0]      eeprom_seg_data ; 
wire [5:0]      sd_seg_sel ; 
wire [7:0]      sd_seg_data ;

reg             sdbmp_rst_n ;
reg             ov_rst_n ;
reg             buzzer_rst_n ;
reg             sdram_rst_n ;

reg [3:0]       sdram_rst_cnt ;

reg  [3:0]      led_reg           ;

reg             button_negedge4_d0 ;
reg             button_negedge3_d0 ;

wire            sd_card_clk ;
wire            ext_mem_clk ;
wire            video_clk   ;

wire            color_hs  ;
wire            color_vs  ;
wire [4:0]      color_r   ;
wire [5:0]      color_g   ;
wire [4:0]      color_b   ;

wire            wr_burst_data_req;
wire            wr_burst_finish;
wire            rd_burst_finish;
reg             rd_burst_req;
reg             wr_burst_req;
reg   [9:0]     rd_burst_len;
reg   [9:0]     wr_burst_len;
reg   [23:0]    rd_burst_addr;
reg   [23:0]    wr_burst_addr;
wire            rd_burst_data_valid;
wire  [15: 0]   rd_burst_data;
reg   [15: 0]   wr_burst_data;  

wire            sd_rd_burst_req;
wire            sd_wr_burst_req;
wire  [9:0]     sd_rd_burst_len;
wire  [9:0]     sd_wr_burst_len;
wire  [23:0]    sd_rd_burst_addr;
wire  [23:0]    sd_wr_burst_addr; 
wire  [15: 0]   sd_wr_burst_data;  

wire            ov_rd_burst_req;
wire            ov_wr_burst_req;
wire  [9:0]     ov_rd_burst_len;
wire  [9:0]     ov_wr_burst_len;
wire  [23:0]    ov_rd_burst_addr;
wire  [23:0]    ov_wr_burst_addr; 
wire  [15: 0]   ov_wr_burst_data;    

//assign rd_burst_req  = (current_state == sd_mode)? sd_rd_burst_req  : ov_rd_burst_req  ; 
//assign wr_burst_req  = (current_state == sd_mode)? sd_wr_burst_req  : ov_wr_burst_req  ; 
//assign rd_burst_len  = (current_state == sd_mode)? sd_rd_burst_len  : ov_rd_burst_len  ; 
//assign wr_burst_len  = (current_state == sd_mode)? sd_wr_burst_len  : ov_wr_burst_len  ; 
//assign rd_burst_addr = (current_state == sd_mode)? sd_rd_burst_addr : ov_rd_burst_addr ;
//assign wr_burst_addr = (current_state == sd_mode)? sd_wr_burst_addr : ov_wr_burst_addr ;
//assign wr_burst_data = (current_state == sd_mode)? sd_wr_burst_data : ov_wr_burst_data ;
//                 


// Data processing logic
always @(posedge clk or negedge rst_n) begin
  if (!rst_n) begin
    i2s_data_acknowledge <= 0;
  end else if (uart_data_ready) begin
    // Handle new data: set acknowledgment
    i2s_data_acknowledge <= 1;
    // ... [other processing logic]
  end else begin
    // Clear acknowledgment once data is processed
  i2s_data_acknowledge <= 0;
  end
end

    
always @(posedge ext_mem_clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
  begin
    rd_burst_req  <= 1'b0 ;
	 wr_burst_req  <= 1'b0 ;
	 rd_burst_len  <= 10'd0 ;
	 wr_burst_len  <= 10'd0 ;
	 rd_burst_addr <= 24'd0 ;
	 wr_burst_addr <= 24'd0 ;
	 wr_burst_data <= 16'd0 ;
  end
  else if (current_state == sd_mode)
  begin
    rd_burst_req  <= sd_rd_burst_req  ;
	 wr_burst_req  <= sd_wr_burst_req  ;
	 rd_burst_len  <= sd_rd_burst_len  ;
	 wr_burst_len  <= sd_wr_burst_len  ;
	 rd_burst_addr <= sd_rd_burst_addr ;
	 wr_burst_addr <= sd_wr_burst_addr ;
	 wr_burst_data <= sd_wr_burst_data ;	 
  end
  else
  begin
    rd_burst_req  <= ov_rd_burst_req  ;
	 wr_burst_req  <= ov_wr_burst_req  ;
	 rd_burst_len  <= ov_rd_burst_len  ;
	 wr_burst_len  <= ov_wr_burst_len  ;
	 rd_burst_addr <= ov_rd_burst_addr ;
	 wr_burst_addr <= ov_wr_burst_addr ;
	 wr_burst_data <= ov_wr_burst_data ;	 
  end 
end  

   
assign led = led_reg ;

assign sdram_clk = ext_mem_clk ;
assign cmos_xclk = sd_card_clk ;


ax_debounce ax_debounce_a0
(
    .clk             (clk),
    .rst             (~rst_n),
    .button_in       (key2),
    .button_posedge  (),
    .button_negedge  (button_negedge2),
    .button_out      ()
);

ax_debounce ax_debounce_a1
(
    .clk             (clk),
    .rst             (~rst_n),
    .button_in       (key3),
    .button_posedge  (),
    .button_negedge  (button_negedge3),
    .button_out      ()
);

ax_debounce ax_debounce_a2
(
    .clk             (sd_card_clk),
    .rst             (~rst_n),
    .button_in       (key4),
    .button_posedge  (),
    .button_negedge  (button_negedge4),
    .button_out      ()
);

always@(posedge clk or negedge rst_n)
begin
    if(rst_n == 1'b0)
		  current_state  <= idle ;
	 else
	     current_state  <= next_state ;
end
	 

always @(*)
begin
  case(current_state)
    idle           : begin
	                    if (button_negedge2)
			          	    next_state <= ledflash_mode ;
			          	  else if (button_negedge3)
			          	    next_state <= eeprom_mode ;
			          	  else if (button_negedge4)
			          	    next_state <= sd_mode ;
			          	  else
			          	    next_state <= idle ;
			          	 end
	 ledflash_mode  :  begin
			          	  if (button_negedge3)
			          	    next_state <= eeprom_mode ;
			          	  else if (button_negedge4)
			          	    next_state <= sd_mode ;
			          	  else
			          	    next_state <= ledflash_mode ;
			          	 end
	 eeprom_mode    :  begin
	                    if (button_negedge2)
			          	    next_state <= ledflash_mode ;
			          	  else if (button_negedge4)
			          	    next_state <= sd_mode ;
			          	  else
			          	    next_state <= eeprom_mode ;
			          	 end	
	 sd_mode       : begin
	                    if (button_negedge2)
			          	    next_state <= ledflash_mode ;
			          	  else if (button_negedge3)
			          	    next_state <= eeprom_mode ;
							  else
							    next_state <= sd_mode ;
			          	 end	
				 
	 default        :  next_state <= idle ;
	endcase
end

    
always @(posedge clk or negedge rst_n)
begin
    if (rst_n == 1'b0)
        led_reg <= 4'b0000; // Reset condition, all LEDs off
    else
        led_reg <= 4'b0000; // Keep LEDs off in all states
end
		
			
always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
    blinking_cnt <= 0 ;
  else
    blinking_cnt <= blinking_cnt + 1 ;
end	

always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
  begin
    button_negedge4_d0 <= 1'b1 ;
	 button_negedge3_d0 <= 1'b1 ;
  end  
  else
  begin
    button_negedge4_d0 <= button_negedge4 ;
	 button_negedge3_d0 <= button_negedge3 ;
  end  
end	
 

always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
  begin
    seg_sel  <= rtc_seg_sel ;
	 seg_data <= rtc_seg_data ;
  end
  else if (current_state == eeprom_mode)
  begin
    seg_sel  <= eeprom_seg_sel ;
	 seg_data <= eeprom_seg_data ;
  end
  else if (current_state == sd_mode)
  begin
    seg_sel  <= sd_seg_sel ;
	 seg_data <= sd_seg_data ;
  end
  else
  begin
    seg_sel  <= rtc_seg_sel ;
	 seg_data <= rtc_seg_data ;
  end
end


always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
    sdbmp_rst_n <= 1'b0 ;
  else if (current_state == sd_mode)
    sdbmp_rst_n <= 1'b1 ;
  else
    sdbmp_rst_n <= 1'b0 ;
end	

always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
    ov_rst_n <= 1'b0 ;
  else if (current_state == sd_mode)
    ov_rst_n <= 1'b0 ;
  else
    ov_rst_n <= 1'b1 ;
end

always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
    buzzer_rst_n <= 1'b0 ;
  else if (current_state == ledflash_mode)
    buzzer_rst_n <= 1'b1 ;
  else
    buzzer_rst_n <= 1'b0 ;
end  


always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
    sdram_rst_n <= 1'b0 ;
  else if (current_state == sd_mode && (button_negedge2 | button_negedge3))
    sdram_rst_n <= 1'b0 ;
  else if (current_state != sd_mode && button_negedge4)
    sdram_rst_n <= 1'b0 ;
  else if (sdram_rst_cnt == 4'd15)
    sdram_rst_n <= 1'b1 ;
  else if (current_state == idle)
    sdram_rst_n <= 1'b1 ;
end

always @(posedge clk or negedge rst_n)
begin
  if(rst_n == 1'b0)
    sdram_rst_cnt <= 4'd0 ;
  else if (sdram_rst_n == 1'b1)
    sdram_rst_cnt <= 4'd0 ;
  else
    sdram_rst_cnt <= sdram_rst_cnt + 1'b1 ;
end

endmodule