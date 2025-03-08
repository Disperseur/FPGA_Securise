`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 07.03.2025 15:24:09
// Design Name: 
// Module Name: fsm_ascon_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module fsm_ascon_tb();
    // ascon inputs
    logic         clock_s;
    logic         reset_s;
    logic         init_s;
    logic         associate_data_s; //0: plain text; 1: DA
    logic         finalisation_s;
    logic [ 63:0] data_s;
    logic         data_valid_s;
    logic [127:0] key_s;
    logic [127:0] nonce_s;
    // ascon outputs
    logic         end_associate_s;
    logic [ 63:0] cipher_s;
    logic         cipher_valid_s;
    logic [127:0] tag_s;
    logic         end_tag_s;
    logic         end_initialisation_s;
    logic         end_cipher_s;

    // other signals
    logic [1471:0] data_i_s;
    logic          start_s;


    ascon ascon_DUT
    (
        // inputs
        .clock_i(clock_s),
        .reset_i(reset_s),
        .init_i(init_s),
        .associate_data_i(associate_data_s),
        .finalisation_i(finalisation_s),
        .data_i(data_s),
        .data_valid_i(data_valid_s),
        .key_i(key_s),
        .nonce_i(nonce_s),
        // outputs
        .end_associate_o(end_associate_s),
        .cipher_o(cipher_s),
        .cipher_valid_o(cipher_valid_s),
        .tag_o(tag_s),
        .end_tag_o(end_tag_s),
        .end_initialisation_o(end_initialisation_s),
        .end_cipher_o(end_cipher_s)
    );

    fsm_ascon fsm_ascon_DUT
    (
        // inputs
        .clock_i(clock_s),
        .reset_i(reset_s),
        .start_i(start_s),
        .data_i(data_i_s),
        .end_associate_i(end_associate_s),
        .cipher_i(cipher_s),
        .cipher_valid_i(cipher_valid_s),
        .tag_i(tag_s),
        .end_tag_i(end_tag_s),
        .end_initialisation_i(end_initialisation_s),
        .end_cipher_i(end_cipher_s),
        // outputs
        .init_o(init_s),
        .associate_data_o(associate_data_s),
        .finalisation_o(finalisation_s),
        .data_o(data_s),
        .data_valid_o(data_valid_s),
        .key_o(key_s),
        .nonce_o(nonce_s)
    );

    //clock
    initial begin
        clock_s = 1'b0;
        forever #5 clock_s = ~clock_s;
    end


    // testbench
    initial begin
        // reset
        reset_s = 1'b1;
        #100;
        reset_s = 1'b0;
        start_s = 1'b0;
        data_i_s = 1472'h5A_5B_5B_5A_5A_5A_5A_5A_59_55_4E_4A_4C_4F_54_55_53_51_53_54_56_57_58_57_5A_5A_59_57_56_59_5B_5A_55_54_54_52_52_50_4F_4F_4C_4C_4D_4D_4A_49_44_44_47_47_46_44_42_43_41_40_3B_36_38_3E_44_49_49_47_47_46_46_44_43_42_43_45_47_45_44_45_46_47_4A_49_47_45_48_4F_58_69_7C_92_AE_CE_ED_FF_FF_E3_B4_7C_47_16_00_04_17_29_36_3C_3F_3E_40_41_41_41_40_3F_3F_40_3F_3E_3B_3A_3B_3E_3D_3E_3C_39_3C_41_46_46_46_45_44_47_46_4A_4C_4F_4C_50_55_55_52_4F_51_55_59_5C_5A_59_5A_5C_5C_5B_59_59_57_53_51_50_4F_4F_53_57_5A_5C_5A_5B_5D_5E_60_60_61_5F_60_5F_5E_5A_58_57_54_52_52_80_00_00;

        #20;

        start_s = 1'b1;

    end


endmodule
