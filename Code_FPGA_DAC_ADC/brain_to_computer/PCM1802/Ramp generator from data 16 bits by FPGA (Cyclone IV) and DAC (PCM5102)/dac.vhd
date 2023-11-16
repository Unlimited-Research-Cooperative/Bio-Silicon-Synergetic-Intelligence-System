library ieee;
use ieee.std_logic_1164.all;

entity clock_ws is
	port (
		BCK : in std_logic; -- clock input
		LCK : out std_logic := '0' -- Audio data world clock input
	);
end clock_ws;

architecture behavioral of clock_ws is
	constant bit_max : integer := 16;
	shared variable count : integer range 0 to bit_max := 0;
	signal lr : std_logic := '0';
	
	begin
		LCK <= lr;
		
		process(BCK)
			begin
				if (BCK'event and BCK = '0') then  -- falling edge
					count := count + 1;
					
					if (count > bit_max-1) then
						lr <= not(lr); -- left or right channel
						count := 0;
						
					end if;
				end if;
		end process;
end behavioral;