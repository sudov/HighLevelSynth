-- ==============================================================
-- RTL generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC
-- Version: 2014.2
-- Copyright (C) 2014 Xilinx Inc. All rights reserved.
-- 
-- ===========================================================

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity nearest_neighbor is
port (
    ap_clk : IN STD_LOGIC;
    ap_rst : IN STD_LOGIC;
    ap_start : IN STD_LOGIC;
    ap_done : OUT STD_LOGIC;
    ap_idle : OUT STD_LOGIC;
    ap_ready : OUT STD_LOGIC;
    input_V : IN STD_LOGIC_VECTOR (48 downto 0);
    nearest_V : OUT STD_LOGIC_VECTOR (3 downto 0);
    nearest_V_ap_vld : OUT STD_LOGIC );
end;


architecture behav of nearest_neighbor is 
    attribute CORE_GENERATION_INFO : STRING;
    attribute CORE_GENERATION_INFO of behav : architecture is
    "nearest_neighbor,hls_ip_2014_2,{HLS_INPUT_TYPE=cxx,HLS_INPUT_FLOAT=0,HLS_INPUT_FIXED=1,HLS_INPUT_PART=xc7z020clg484-1,HLS_INPUT_CLOCK=10.000000,HLS_INPUT_ARCH=others,HLS_SYN_CLOCK=5.332875,HLS_SYN_LAT=1044001,HLS_SYN_TPT=none,HLS_SYN_MEM=0,HLS_SYN_DSP=0,HLS_SYN_FF=0,HLS_SYN_LUT=0}";
    constant ap_const_logic_1 : STD_LOGIC := '1';
    constant ap_const_logic_0 : STD_LOGIC := '0';
    constant ap_ST_st1_fsm_0 : STD_LOGIC_VECTOR (2 downto 0) := "000";
    constant ap_ST_st2_fsm_1 : STD_LOGIC_VECTOR (2 downto 0) := "001";
    constant ap_ST_st3_fsm_2 : STD_LOGIC_VECTOR (2 downto 0) := "010";
    constant ap_ST_st4_fsm_3 : STD_LOGIC_VECTOR (2 downto 0) := "011";
    constant ap_ST_st5_fsm_4 : STD_LOGIC_VECTOR (2 downto 0) := "100";
    constant ap_const_lv1_0 : STD_LOGIC_VECTOR (0 downto 0) := "0";
    constant ap_const_lv11_0 : STD_LOGIC_VECTOR (10 downto 0) := "00000000000";
    constant ap_const_lv4_0 : STD_LOGIC_VECTOR (3 downto 0) := "0000";
    constant ap_const_lv15_0 : STD_LOGIC_VECTOR (14 downto 0) := "000000000000000";
    constant ap_const_lv49_0 : STD_LOGIC_VECTOR (48 downto 0) := "0000000000000000000000000000000000000000000000000";
    constant ap_const_lv6_0 : STD_LOGIC_VECTOR (5 downto 0) := "000000";
    constant ap_const_lv49_7D0 : STD_LOGIC_VECTOR (48 downto 0) := "0000000000000000000000000000000000000011111010000";
    constant ap_const_lv11_7D0 : STD_LOGIC_VECTOR (10 downto 0) := "11111010000";
    constant ap_const_lv11_1 : STD_LOGIC_VECTOR (10 downto 0) := "00000000001";
    constant ap_const_lv15_7D0 : STD_LOGIC_VECTOR (14 downto 0) := "000011111010000";
    constant ap_const_lv4_A : STD_LOGIC_VECTOR (3 downto 0) := "1010";
    constant ap_const_lv4_1 : STD_LOGIC_VECTOR (3 downto 0) := "0001";
    constant ap_const_lv6_31 : STD_LOGIC_VECTOR (5 downto 0) := "110001";
    constant ap_const_lv6_1 : STD_LOGIC_VECTOR (5 downto 0) := "000001";
    constant ap_const_lv49_1FFFFFFFFFFFF : STD_LOGIC_VECTOR (48 downto 0) := "1111111111111111111111111111111111111111111111111";
    constant ap_const_lv49_1 : STD_LOGIC_VECTOR (48 downto 0) := "0000000000000000000000000000000000000000000000001";

    signal ap_CS_fsm : STD_LOGIC_VECTOR (2 downto 0) := "000";
    signal training_data_address0 : STD_LOGIC_VECTOR (14 downto 0);
    signal training_data_ce0 : STD_LOGIC;
    signal training_data_q0 : STD_LOGIC_VECTOR (47 downto 0);
    signal data_1_fu_166_p2 : STD_LOGIC_VECTOR (10 downto 0);
    signal data_1_reg_291 : STD_LOGIC_VECTOR (10 downto 0);
    signal next_mul_fu_172_p2 : STD_LOGIC_VECTOR (14 downto 0);
    signal next_mul_reg_296 : STD_LOGIC_VECTOR (14 downto 0);
    signal possible_result_fu_184_p2 : STD_LOGIC_VECTOR (3 downto 0);
    signal possible_result_reg_304 : STD_LOGIC_VECTOR (3 downto 0);
    signal exitcond_fu_178_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal r_V_fu_209_p2 : STD_LOGIC_VECTOR (48 downto 0);
    signal i_fu_221_p2 : STD_LOGIC_VECTOR (5 downto 0);
    signal diff_V_1_fu_239_p2 : STD_LOGIC_VECTOR (48 downto 0);
    signal exitcond_i_fu_215_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal counter_V_1_fu_251_p3 : STD_LOGIC_VECTOR (48 downto 0);
    signal data_reg_87 : STD_LOGIC_VECTOR (10 downto 0);
    signal val_assign_reg_99 : STD_LOGIC_VECTOR (3 downto 0);
    signal exitcond1_fu_160_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal phi_mul_reg_112 : STD_LOGIC_VECTOR (14 downto 0);
    signal p_i_reg_123 : STD_LOGIC_VECTOR (48 downto 0);
    signal p_1_i_reg_132 : STD_LOGIC_VECTOR (48 downto 0);
    signal i_i_reg_143 : STD_LOGIC_VECTOR (5 downto 0);
    signal tmp_fu_200_p1 : STD_LOGIC_VECTOR (63 downto 0);
    signal max_difference_V_1_fu_58 : STD_LOGIC_VECTOR (48 downto 0);
    signal max_difference_V_fu_266_p1 : STD_LOGIC_VECTOR (48 downto 0);
    signal tmp_4_fu_270_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal tmp_trn_cast_fu_190_p1 : STD_LOGIC_VECTOR (14 downto 0);
    signal training_data_addr2_fu_194_p2 : STD_LOGIC_VECTOR (14 downto 0);
    signal rhs_V_cast_fu_205_p1 : STD_LOGIC_VECTOR (48 downto 0);
    signal tmp_8_i_fu_233_p2 : STD_LOGIC_VECTOR (48 downto 0);
    signal tmp_7_i_fu_227_p2 : STD_LOGIC_VECTOR (0 downto 0);
    signal counter_V_fu_245_p2 : STD_LOGIC_VECTOR (48 downto 0);
    signal difference_V_fu_262_p1 : STD_LOGIC_VECTOR (5 downto 0);
    signal ap_NS_fsm : STD_LOGIC_VECTOR (2 downto 0);

    component nearest_neighbor_training_data IS
    generic (
        DataWidth : INTEGER;
        AddressRange : INTEGER;
        AddressWidth : INTEGER );
    port (
        clk : IN STD_LOGIC;
        reset : IN STD_LOGIC;
        address0 : IN STD_LOGIC_VECTOR (14 downto 0);
        ce0 : IN STD_LOGIC;
        q0 : OUT STD_LOGIC_VECTOR (47 downto 0) );
    end component;



begin
    training_data_U : component nearest_neighbor_training_data
    generic map (
        DataWidth => 48,
        AddressRange => 20000,
        AddressWidth => 15)
    port map (
        clk => ap_clk,
        reset => ap_rst,
        address0 => training_data_address0,
        ce0 => training_data_ce0,
        q0 => training_data_q0);





    -- the current state (ap_CS_fsm) of the state machine. --
    ap_CS_fsm_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst = '1') then
                ap_CS_fsm <= ap_ST_st1_fsm_0;
            else
                ap_CS_fsm <= ap_NS_fsm;
            end if;
        end if;
    end process;


    -- data_reg_87 assign process. --
    data_reg_87_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st3_fsm_2 = ap_CS_fsm) and not((exitcond_fu_178_p2 = ap_const_lv1_0)))) then 
                data_reg_87 <= data_1_reg_291;
            elsif (((ap_ST_st1_fsm_0 = ap_CS_fsm) and not((ap_start = ap_const_logic_0)))) then 
                data_reg_87 <= ap_const_lv11_0;
            end if; 
        end if;
    end process;

    -- i_i_reg_143 assign process. --
    i_i_reg_143_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st5_fsm_4 = ap_CS_fsm) and (ap_const_lv1_0 = exitcond_i_fu_215_p2))) then 
                i_i_reg_143 <= i_fu_221_p2;
            elsif ((ap_ST_st4_fsm_3 = ap_CS_fsm)) then 
                i_i_reg_143 <= ap_const_lv6_0;
            end if; 
        end if;
    end process;

    -- max_difference_V_1_fu_58 assign process. --
    max_difference_V_1_fu_58_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st5_fsm_4 = ap_CS_fsm) and not((ap_const_lv1_0 = exitcond_i_fu_215_p2)) and not((ap_const_lv1_0 = tmp_4_fu_270_p2)))) then 
                max_difference_V_1_fu_58(0) <= max_difference_V_fu_266_p1(0);
                max_difference_V_1_fu_58(1) <= max_difference_V_fu_266_p1(1);
                max_difference_V_1_fu_58(2) <= max_difference_V_fu_266_p1(2);
                max_difference_V_1_fu_58(3) <= max_difference_V_fu_266_p1(3);
                max_difference_V_1_fu_58(4) <= max_difference_V_fu_266_p1(4);
                max_difference_V_1_fu_58(5) <= max_difference_V_fu_266_p1(5);
                max_difference_V_1_fu_58(6) <= max_difference_V_fu_266_p1(6);
                max_difference_V_1_fu_58(7) <= max_difference_V_fu_266_p1(7);
                max_difference_V_1_fu_58(8) <= max_difference_V_fu_266_p1(8);
                max_difference_V_1_fu_58(9) <= max_difference_V_fu_266_p1(9);
                max_difference_V_1_fu_58(10) <= max_difference_V_fu_266_p1(10);
            elsif (((ap_ST_st1_fsm_0 = ap_CS_fsm) and not((ap_start = ap_const_logic_0)))) then 
                max_difference_V_1_fu_58(0) <= '0';
                max_difference_V_1_fu_58(1) <= '0';
                max_difference_V_1_fu_58(2) <= '0';
                max_difference_V_1_fu_58(3) <= '0';
                max_difference_V_1_fu_58(4) <= '1';
                max_difference_V_1_fu_58(5) <= '0';
                max_difference_V_1_fu_58(6) <= '1';
                max_difference_V_1_fu_58(7) <= '1';
                max_difference_V_1_fu_58(8) <= '1';
                max_difference_V_1_fu_58(9) <= '1';
                max_difference_V_1_fu_58(10) <= '1';
            end if; 
        end if;
    end process;

    -- p_1_i_reg_132 assign process. --
    p_1_i_reg_132_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st5_fsm_4 = ap_CS_fsm) and (ap_const_lv1_0 = exitcond_i_fu_215_p2))) then 
                p_1_i_reg_132 <= counter_V_1_fu_251_p3;
            elsif ((ap_ST_st4_fsm_3 = ap_CS_fsm)) then 
                p_1_i_reg_132 <= ap_const_lv49_0;
            end if; 
        end if;
    end process;

    -- p_i_reg_123 assign process. --
    p_i_reg_123_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st5_fsm_4 = ap_CS_fsm) and (ap_const_lv1_0 = exitcond_i_fu_215_p2))) then 
                p_i_reg_123 <= diff_V_1_fu_239_p2;
            elsif ((ap_ST_st4_fsm_3 = ap_CS_fsm)) then 
                p_i_reg_123 <= r_V_fu_209_p2;
            end if; 
        end if;
    end process;

    -- phi_mul_reg_112 assign process. --
    phi_mul_reg_112_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st2_fsm_1 = ap_CS_fsm) and (ap_const_lv1_0 = exitcond1_fu_160_p2))) then 
                phi_mul_reg_112 <= ap_const_lv15_0;
            elsif (((ap_ST_st5_fsm_4 = ap_CS_fsm) and not((ap_const_lv1_0 = exitcond_i_fu_215_p2)))) then 
                phi_mul_reg_112 <= next_mul_reg_296;
            end if; 
        end if;
    end process;

    -- val_assign_reg_99 assign process. --
    val_assign_reg_99_assign_proc : process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if (((ap_ST_st2_fsm_1 = ap_CS_fsm) and (ap_const_lv1_0 = exitcond1_fu_160_p2))) then 
                val_assign_reg_99 <= ap_const_lv4_0;
            elsif (((ap_ST_st5_fsm_4 = ap_CS_fsm) and not((ap_const_lv1_0 = exitcond_i_fu_215_p2)))) then 
                val_assign_reg_99 <= possible_result_reg_304;
            end if; 
        end if;
    end process;

    -- assign process. --
    process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if ((ap_ST_st2_fsm_1 = ap_CS_fsm)) then
                data_1_reg_291 <= data_1_fu_166_p2;
            end if;
        end if;
    end process;

    -- assign process. --
    process (ap_clk)
    begin
        if (ap_clk'event and ap_clk = '1') then
            if ((ap_ST_st3_fsm_2 = ap_CS_fsm)) then
                next_mul_reg_296 <= next_mul_fu_172_p2;
                possible_result_reg_304 <= possible_result_fu_184_p2;
            end if;
        end if;
    end process;
    max_difference_V_1_fu_58(48 downto 11) <= "00000000000000000000000000000000000000";

    -- the next state (ap_NS_fsm) of the state machine. --
    ap_NS_fsm_assign_proc : process (ap_start, ap_CS_fsm, exitcond_fu_178_p2, exitcond_i_fu_215_p2, exitcond1_fu_160_p2)
    begin
        case ap_CS_fsm is
            when ap_ST_st1_fsm_0 => 
                if (not((ap_start = ap_const_logic_0))) then
                    ap_NS_fsm <= ap_ST_st2_fsm_1;
                else
                    ap_NS_fsm <= ap_ST_st1_fsm_0;
                end if;
            when ap_ST_st2_fsm_1 => 
                if (not((ap_const_lv1_0 = exitcond1_fu_160_p2))) then
                    ap_NS_fsm <= ap_ST_st1_fsm_0;
                else
                    ap_NS_fsm <= ap_ST_st3_fsm_2;
                end if;
            when ap_ST_st3_fsm_2 => 
                if ((exitcond_fu_178_p2 = ap_const_lv1_0)) then
                    ap_NS_fsm <= ap_ST_st4_fsm_3;
                else
                    ap_NS_fsm <= ap_ST_st2_fsm_1;
                end if;
            when ap_ST_st4_fsm_3 => 
                ap_NS_fsm <= ap_ST_st5_fsm_4;
            when ap_ST_st5_fsm_4 => 
                if (not((ap_const_lv1_0 = exitcond_i_fu_215_p2))) then
                    ap_NS_fsm <= ap_ST_st3_fsm_2;
                else
                    ap_NS_fsm <= ap_ST_st5_fsm_4;
                end if;
            when others =>  
                ap_NS_fsm <= "XXX";
        end case;
    end process;

    -- ap_done assign process. --
    ap_done_assign_proc : process(ap_CS_fsm, exitcond1_fu_160_p2)
    begin
        if (((ap_ST_st2_fsm_1 = ap_CS_fsm) and not((ap_const_lv1_0 = exitcond1_fu_160_p2)))) then 
            ap_done <= ap_const_logic_1;
        else 
            ap_done <= ap_const_logic_0;
        end if; 
    end process;


    -- ap_idle assign process. --
    ap_idle_assign_proc : process(ap_start, ap_CS_fsm)
    begin
        if ((not((ap_const_logic_1 = ap_start)) and (ap_ST_st1_fsm_0 = ap_CS_fsm))) then 
            ap_idle <= ap_const_logic_1;
        else 
            ap_idle <= ap_const_logic_0;
        end if; 
    end process;


    -- ap_ready assign process. --
    ap_ready_assign_proc : process(ap_CS_fsm, exitcond1_fu_160_p2)
    begin
        if (((ap_ST_st2_fsm_1 = ap_CS_fsm) and not((ap_const_lv1_0 = exitcond1_fu_160_p2)))) then 
            ap_ready <= ap_const_logic_1;
        else 
            ap_ready <= ap_const_logic_0;
        end if; 
    end process;

    counter_V_1_fu_251_p3 <= 
        p_1_i_reg_132 when (tmp_7_i_fu_227_p2(0) = '1') else 
        counter_V_fu_245_p2;
    counter_V_fu_245_p2 <= std_logic_vector(unsigned(p_1_i_reg_132) + unsigned(ap_const_lv49_1));
    data_1_fu_166_p2 <= std_logic_vector(unsigned(data_reg_87) + unsigned(ap_const_lv11_1));
    diff_V_1_fu_239_p2 <= (tmp_8_i_fu_233_p2 and p_i_reg_123);
    difference_V_fu_262_p1 <= p_1_i_reg_132(6 - 1 downto 0);
    exitcond1_fu_160_p2 <= "1" when (data_reg_87 = ap_const_lv11_7D0) else "0";
    exitcond_fu_178_p2 <= "1" when (val_assign_reg_99 = ap_const_lv4_A) else "0";
    exitcond_i_fu_215_p2 <= "1" when (i_i_reg_143 = ap_const_lv6_31) else "0";
    i_fu_221_p2 <= std_logic_vector(unsigned(i_i_reg_143) + unsigned(ap_const_lv6_1));
    max_difference_V_fu_266_p1 <= std_logic_vector(resize(unsigned(difference_V_fu_262_p1),49));
    nearest_V <= val_assign_reg_99;

    -- nearest_V_ap_vld assign process. --
    nearest_V_ap_vld_assign_proc : process(ap_CS_fsm, exitcond_i_fu_215_p2, tmp_4_fu_270_p2)
    begin
        if (((ap_ST_st5_fsm_4 = ap_CS_fsm) and not((ap_const_lv1_0 = exitcond_i_fu_215_p2)) and not((ap_const_lv1_0 = tmp_4_fu_270_p2)))) then 
            nearest_V_ap_vld <= ap_const_logic_1;
        else 
            nearest_V_ap_vld <= ap_const_logic_0;
        end if; 
    end process;

    next_mul_fu_172_p2 <= std_logic_vector(unsigned(phi_mul_reg_112) + unsigned(ap_const_lv15_7D0));
    possible_result_fu_184_p2 <= std_logic_vector(unsigned(val_assign_reg_99) + unsigned(ap_const_lv4_1));
    r_V_fu_209_p2 <= (rhs_V_cast_fu_205_p1 xor input_V);
    rhs_V_cast_fu_205_p1 <= std_logic_vector(resize(unsigned(training_data_q0),49));
    tmp_4_fu_270_p2 <= "1" when (unsigned(max_difference_V_fu_266_p1) < unsigned(max_difference_V_1_fu_58)) else "0";
    tmp_7_i_fu_227_p2 <= "1" when (p_i_reg_123 = ap_const_lv49_0) else "0";
    tmp_8_i_fu_233_p2 <= std_logic_vector(unsigned(p_i_reg_123) + unsigned(ap_const_lv49_1FFFFFFFFFFFF));
    tmp_fu_200_p1 <= std_logic_vector(resize(unsigned(training_data_addr2_fu_194_p2),64));
    tmp_trn_cast_fu_190_p1 <= std_logic_vector(resize(unsigned(data_reg_87),15));
    training_data_addr2_fu_194_p2 <= std_logic_vector(unsigned(phi_mul_reg_112) + unsigned(tmp_trn_cast_fu_190_p1));
    training_data_address0 <= tmp_fu_200_p1(15 - 1 downto 0);

    -- training_data_ce0 assign process. --
    training_data_ce0_assign_proc : process(ap_CS_fsm)
    begin
        if ((ap_ST_st3_fsm_2 = ap_CS_fsm)) then 
            training_data_ce0 <= ap_const_logic_1;
        else 
            training_data_ce0 <= ap_const_logic_0;
        end if; 
    end process;

end behav;
