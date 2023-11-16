library ieee;
use ieee.std_logic_1164.all;

entity generator is
	port (
		CLK : in std_logic;
		BCK : out std_logic;
		DIN : out std_logic;
		LCK : out std_logic
	);
end generator;

architecture stractural of generator is
	component Parallel_Serial_Converter is
		port (
			CLK : in std_logic;
			parallel_in : in std_logic_vector(15 downto 0); -- 16 bit
			serial_out : out std_logic := '0'
		);
	end component;
	
	component generate_ramp is
	port (
			BCK : in std_logic;
			DIN : out std_logic_vector(15 downto 0)
		);
	end component;
	
	component generate_sin is
	port (
		BCK : in std_logic;
		DIN : out std_logic_vector(15 downto 0)
	);
	end component;

	component clock_divider is
		port (
			CLK_IN : in std_logic;
			CLK_OUT : out std_logic
		);
	end component;
	
	component clock_ws is
		port (
			BCK : in std_logic; -- clock input
			LCK : out std_logic := '0' -- Audio data world clock input
		);
	end component;
	
	signal audio_data : std_logic_vector(15 downto 0) := "1000000000000000";
	signal CLK_divider : std_logic := '0';
	signal WS : std_logic := '0';
	
begin
	U0 : clock_divider
		port map (CLK, CLK_divider);
	U3 : clock_ws
		port map (CLK_divider, LCK);
	U1 : generate_ramp
		port map (CLK_divider, audio_data); 
	--U4 : generate_sin
		--port map (CLK_divider, audio_data);
	U2 : Parallel_Serial_Converter
		port map (CLK_divider, audio_data, DIN);
		
	BCK <= CLK_divider;

end stractural;
