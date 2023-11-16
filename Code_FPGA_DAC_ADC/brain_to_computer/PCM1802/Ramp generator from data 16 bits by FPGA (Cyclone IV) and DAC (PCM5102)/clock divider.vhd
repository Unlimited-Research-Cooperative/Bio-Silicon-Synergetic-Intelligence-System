library ieee;
use ieee.std_logic_1164.all;

entity clock_divider is
	port (
		CLK_IN : in std_logic;
		CLK_OUT : out std_logic
	);
end clock_divider;

architecture behavioral of clock_divider is
	constant count_max : integer := 20; 
	shared variable count : integer range 0 to count_max+1 := 0;
	signal tmp : std_logic := '0';
	
	begin
		
		CLK_OUT <= tmp;
		
		process(CLK_IN)
			begin
				if (CLK_IN'event and CLK_IN = '1') then
					count := count + 1;
					
					if (count > count_max) then
						tmp <= not(tmp);
						count := 1;						
						
					end if;
				end if;
		end process;
end behavioral;