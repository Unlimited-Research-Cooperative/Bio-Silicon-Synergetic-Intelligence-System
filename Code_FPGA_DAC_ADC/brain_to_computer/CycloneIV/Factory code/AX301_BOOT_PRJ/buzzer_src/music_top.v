module music_top
(
 input clk,
 input rst_n,
 output reg buzzer
) ;

parameter music_len = 32'd136 ;

wire [19:0] cycle ;
reg [31:0] play_cnt ;
reg [31:0] music_cnt ;
reg [19:0] hz_cnt ;
wire [4:0] hz_sel ;

parameter IDLE      = 2'd0 ;
parameter PLAY      = 2'd1 ;
parameter PLAY_WAIT = 2'd2 ;
parameter PLAY_END  = 2'd3 ;

reg [1:0]  state ;
reg [1:0]  next_state ;

always @(posedge clk or negedge rst_n)
begin
  if (~rst_n)
    state <= IDLE ;
  else
    state <= next_state ;
end

always @(*)
begin
  case(state)
  IDLE      : begin
                 next_state <= PLAY ;
		        end
  PLAY      : begin
              if (play_cnt == 32'd12_499_999)  //play 0.5s every music step
				    next_state <= PLAY_WAIT  ;
				  else
				    next_state <= PLAY  ;
			     end
  PLAY_WAIT : begin
               if (music_cnt == music_len - 1)
				     next_state <= PLAY_END  ;
				   else
				     next_state <= PLAY  ;
			     end
  PLAY_END  : next_state <= PLAY_END ;
  default   : next_state <= IDLE ;
  endcase
end
  
   
//counter in every step, maximum value is cycle
always @(posedge clk or negedge rst_n)
begin
  if (~rst_n)
    hz_cnt <= 20'd0 ;  
  else if (state == PLAY || state == PLAY_WAIT)
  begin
    if (hz_cnt == cycle - 1)
	   hz_cnt <= 20'd0 ;
	 else
      hz_cnt <= hz_cnt + 1'b1 ;
  end
  else 
    hz_cnt <= 20'd0 ;
end	
//buzzer out
always @(posedge clk or negedge rst_n)
begin
  if (~rst_n)
    buzzer <= 1'b1 ;  
  else if (state == PLAY || state == PLAY_WAIT)
  begin
    if (hz_cnt < cycle/64)                     //duty cycle to adjust buzzer volume
      buzzer <= 1'b0	;
	 else
	   buzzer <= 1'b1	;
  end
  else if (state == IDLE || state == PLAY_END)
    buzzer <= 1'b1 ;
end

//play counter
always @(posedge clk or negedge rst_n)
begin
  if (~rst_n)
    play_cnt <= 32'd0 ;  
  else if (state == PLAY)
    play_cnt <= play_cnt + 1'b1 ;
  else 
    play_cnt <= 32'd0 ;
end
//music step counter
always @(posedge clk or negedge rst_n)
begin
  if (~rst_n)
    music_cnt <= 32'd0 ;  
  else if (state == PLAY_WAIT)
    music_cnt <= music_cnt + 1'b1 ;
  else if (state == IDLE || state == PLAY_END)
    music_cnt <= 32'd0 ;
end
//select cycle value with each music value
music_hz hz0
(
 .hz_sel(hz_sel),
 .cycle(cycle) 
) ;
//music step value rom
music_rom rom0
(
	.address(music_cnt[8:0]),
	.clock(clk),
	.q(hz_sel[4:0])
	);
	

endmodule
