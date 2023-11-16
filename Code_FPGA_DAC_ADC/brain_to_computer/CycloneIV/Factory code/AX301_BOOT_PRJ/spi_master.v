//*************************************************************************\
//Copyright (c) 2017,ALINX(shanghai) Technology Co.,Ltd,All rights reserved
//
//                   File Name  :  spi_master.v
//                Project Name  :  
//                      Author  :  meisq
//                       Email  :  msq@qq.com
//                     Company  :  ALINX(shanghai) Technology Co.,Ltd
//                         WEB  :  http://www.alinx.cn/
//==========================================================================
//   Description:   
//
//   
//==========================================================================
//  Revision History:
//  Date          By            Revision    Change Description
//--------------------------------------------------------------------------
//  2017/6/19     meisq         1.0         Original
//*************************************************************************/
module spi_master
(
    input       sys_clk,
    input       rst,
    output      nCS,
    output      DCLK,
    output      MOSI,
    input       MISO,
    input       CPOL,
    input       CPHA,
    input       nCS_ctrl,
	 input[15:0] clk_div,
    input       wr_req,
    output      wr_ack,
    input[7:0]  data_in,
    output[7:0] data_out
);
localparam IDLE = 0;
localparam DCLK_EDGE = 1;
localparam DCLK_IDLE = 2;
localparam ACK = 3;
localparam LAST_HALF_CYCLE = 4;
localparam ACK_WAIT = 5;
reg DCLK_reg;
reg[7:0] MOSI_shift;
(* keep *) reg[7:0] MISO_shift;
reg[3:0] state,next_state;
reg [15:0] clk_cnt;
reg[4:0] clk_edge_cnt;
assign MOSI = MOSI_shift[7];
assign DCLK = DCLK_reg;
assign data_out = MISO_shift;
assign wr_ack = (state == ACK);
assign nCS = nCS_ctrl;

//下面三个always块是一个完整的逻辑状态，且要注意的是第二个always块是根据第一个always块的时钟跑起来的，这里的clk_div设置的值是0，在第二个always块里的首先进入空闲状态的if（wr_req）的判断，消耗一个时钟周期，
//然后进入DCLK_IDLE状态的clk_div，消耗一个时钟周期，已经消耗两个时钟周期，而一个完整数据传送需要进行一次主机命令发送，一次从机数据的回传，每次消耗两个时钟周期，一共消耗四个时钟周期；所以当clk_div=1的时候，
//又在clk_cnt累加的时候消耗了一个时钟就至少需要消耗6个时钟周期才能完成一次数据传输
always@(posedge sys_clk or posedge rst)
begin
    if(rst==1)
        state <= IDLE;
    else
        state <= next_state;
end
always@(*)
begin
    case(state)
        IDLE:
            if(wr_req)
                next_state <= DCLK_IDLE;
            else
                next_state <= IDLE;
        DCLK_IDLE:
            if(clk_cnt == clk_div)
                next_state <= DCLK_EDGE;
            else
                next_state <= DCLK_IDLE;
        DCLK_EDGE:
            if(clk_edge_cnt == 5'd15)
                next_state <= LAST_HALF_CYCLE;
            else
                next_state <= DCLK_IDLE;
        LAST_HALF_CYCLE:
            if(clk_cnt == clk_div)
                next_state <= ACK;
            else
                next_state <= LAST_HALF_CYCLE;          
        ACK:
            next_state <= ACK_WAIT;
        ACK_WAIT:
            next_state <= IDLE;
        default:
            next_state <= IDLE;
    endcase
end
//模拟出一个DCLK时钟
always@(posedge sys_clk or posedge rst)
begin
    if(rst==1)
        DCLK_reg <= 1'b0;
    else if(state == IDLE)
        DCLK_reg <= CPOL;
    else if(state == DCLK_EDGE)
        DCLK_reg <= ~DCLK_reg;
end

always@(posedge sys_clk or posedge rst)
begin
    if(rst==1)
        clk_cnt <= 16'd0;
    else if(state == DCLK_IDLE || state == LAST_HALF_CYCLE) 
        clk_cnt <= clk_cnt + 16'd1;
    else
        clk_cnt <= 16'd0;
end

always@(posedge sys_clk or posedge rst)
begin
    if(rst==1)
        clk_edge_cnt <= 5'd0;
    else if(state == DCLK_EDGE)
        clk_edge_cnt <= clk_edge_cnt + 5'd1;
    else if(state == IDLE)
        clk_edge_cnt <= 5'd0;
end

always@(posedge sys_clk or posedge rst)
begin
    if(rst==1)
        MOSI_shift <= 8'd0;
    else if(state == IDLE && wr_req)
        MOSI_shift <= data_in;
    else if(state == DCLK_EDGE)
        if(CPHA == 1'b0 && clk_edge_cnt[0] == 1'b1) //第一个边沿的下降沿将数据发送给从机
            MOSI_shift <= {MOSI_shift[6:0],MOSI_shift[7]};
		  else if(CPHA == 1'b1 && (clk_edge_cnt != 5'd0 && clk_edge_cnt[0] == 1'b0))//第二个边沿的上升沿采样
            MOSI_shift <= {MOSI_shift[6:0],MOSI_shift[7]};
end

always@(posedge sys_clk or posedge rst)
begin
    if(rst==1)
        MISO_shift <= 8'd0;
    else if(state == IDLE && wr_req)
        MISO_shift <= 8'h00;
    else if(state == DCLK_EDGE)
	 if(CPHA == 1'b0 && clk_edge_cnt[0] == 1'b0) //第一个边沿的上升沿从机将数据回传给主机，也就是在第一个模拟的时钟内主机是收不到从机发的数据的
            MISO_shift <= {MISO_shift[6:0],MISO};
        else if(CPHA == 1'b1 && (clk_edge_cnt[0] == 1'b1))//从机在下降沿将数据回传给主机
            MISO_shift <= {MISO_shift[6:0],MISO};
end
endmodule 