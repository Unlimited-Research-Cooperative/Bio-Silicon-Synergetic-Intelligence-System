library ieee;
use ieee.std_logic_1164.all;

entity Parallel_Serial_Converter is
	port (
		CLK : in std_logic;
		parallel_in : in std_logic_vector(15 downto 0); -- 16 bit
		serial_out : out std_logic := '0'
	);
end Parallel_Serial_Converter;

architecture behavioral of Parallel_Serial_Converter is
	constant max : integer := 15; --
	begin
		process(CLK)
			variable count : integer range 0 to max+1 := 0;
			begin
				if (CLK'event and CLK = '0') then
					serial_out <= parallel_in(15-count); --
					count := count + 1;
						
					if (count > max) then
						count := 0;
						
					end if;
				end if;
		end process;
end behavioral;