module music_hz
(
 input  [4:0]  hz_sel,
 output reg [19:0] cycle
) ;

parameter CLK_FRE = 50 ;

always @(*)
begin
  case(hz_sel)
    5'd0    : cycle <= CLK_FRE*1000000/261  ;  //low 1         261Hz
    5'd1    : cycle <= CLK_FRE*1000000/293  ;  //low 2         293Hz
    5'd2    : cycle <= CLK_FRE*1000000/329  ;  //low 3         329Hz
    5'd3    : cycle <= CLK_FRE*1000000/349  ;  //low 4         349Hz
    5'd4    : cycle <= CLK_FRE*1000000/392  ;  //low 5         392Hz
    5'd5    : cycle <= CLK_FRE*1000000/440  ;  //low 6         440Hz
    5'd6    : cycle <= CLK_FRE*1000000/499  ;  //low 7         499Hz
    5'd7    : cycle <= CLK_FRE*1000000/523  ;  //middle 1      523Hz
    5'd8    : cycle <= CLK_FRE*1000000/587  ;  //middle 2      587Hz
    5'd9    : cycle <= CLK_FRE*1000000/659  ;  //middle 3      659Hz
    5'd10   : cycle <= CLK_FRE*1000000/698  ;  //middle 4      698Hz
    5'd11   : cycle <= CLK_FRE*1000000/784  ;  //middle 5      784Hz
    5'd12   : cycle <= CLK_FRE*1000000/880  ;  //middle 6      880Hz
    5'd13   : cycle <= CLK_FRE*1000000/998  ;  //middle 7      998Hz
    5'd14   : cycle <= CLK_FRE*1000000/1046 ;  //high 1        1046Hz
    5'd15   : cycle <= CLK_FRE*1000000/1174 ;  //high 2        1174Hz
    5'd16   : cycle <= CLK_FRE*1000000/1318 ;  //high 3        1318Hz
    5'd17   : cycle <= CLK_FRE*1000000/1396 ;  //high 4        1396Hz
    5'd18   : cycle <= CLK_FRE*1000000/1568 ;  //high 5        1568Hz
    5'd19   : cycle <= CLK_FRE*1000000/1760 ;  //high 6        1760Hz
    5'd20   : cycle <= CLK_FRE*1000000/1976 ;  //high 7        1976Hz
	 5'd21   : cycle <= CLK_FRE*1000000/2093 ;  //super high 1  2093Hz
	 5'd22   : cycle <= CLK_FRE*1000000/2349 ;  //super high 2  2349Hz
	 5'd23   : cycle <= CLK_FRE*1000000/2637 ;  //super high 3  2637Hz
	 5'd24   : cycle <= CLK_FRE*1000000/2794 ;  //super high 4  2794Hz
	 5'd25   : cycle <= CLK_FRE*1000000/3136 ;  //super high 5  3136Hz
	 5'd26   : cycle <= CLK_FRE*1000000/3520 ;  //super high 6  3520Hz
	 5'd27   : cycle <= CLK_FRE*1000000/3951 ;  //super high 7  3951Hz
    default : cycle <= 20'd0 ;
  endcase
end

endmodule
