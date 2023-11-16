library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_signed.all;
use ieee.math_real.all;

entity generate_sin is
	port (
		BCK : in std_logic;
		DIN : out std_logic_vector(15 downto 0)
	);
end generate_sin;

architecture behavioral of generate_sin is
	constant bit_max : integer := 16;
	shared variable count : integer range 1 to bit_max := 1;
   shared variable data_16bit : integer := 0;
	shared variable  data_16bit_vector : std_logic_vector(15 downto 0) := "0000000000000000";
	shared variable t : integer := 0; -- for increase value
	shared variable i : integer := 1;
	constant k : real := real(32767);
	shared variable v_sine : real := 0.0;
	
	begin
		DIN <= data_16bit_vector;
		
		process(BCK)
			begin
				if (BCK'event and BCK = '0') then  -- falling edge
					count := count + 1;
					
					if (count > bit_max-1) then
						t := t+i;
						if (t > 320-1) then -- high value
							t := 320;
							i := -1;
						elsif (t < -320+1) then -- low value
							t := -320;
							i := 1;
						end if;
						
						v_sine := sine(MATH_2_PI * real(t));
						data_16bit := integer( k * v_sine );
						data_16bit_vector := std_logic_vector(to_signed(data_16bit, data_16bit_vector'length));
						count := 1;
					end if;
				end if;
		end process;
		
end behavioral;
