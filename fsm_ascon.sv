`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 07.03.2025 13:59:31
// Design Name: 
// Module Name: fsm_ascon
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


module fsm_ascon(
        // inputs
        input logic         clock_i,
        input logic         reset_i,
        input logic         start_i,
        input logic [1471:0] data_i,

        input logic         end_associate_i,
        input logic [ 63:0] cipher_i,
        input logic         cipher_valid_i,
        input logic [127:0] tag_i,
        input logic         end_tag_i,
        input logic         end_initialisation_i,
        input logic         end_cipher_i,

        // outputs
        output logic         init_o,
        output logic         associate_data_o, //0: plain text; 1: DA
        output logic         finalisation_o,
        output logic [ 63:0] data_o,
        output logic         data_valid_o,
        output logic [127:0] key_o,
        output logic [127:0] nonce_o      
    );

    // fsm states
    typedef enum {
        idle,
        init,
        wait_end_init,
        associate_data,
        end_associate_data,
        wait_end_associate,
        pt_set_data,
        pt_wait_cipher_valid,
        pt_get_cipher,
        pt_wait_end_cipher,
        finalisation,
        pt_get_final_cipher,
        wait_end_tag,
        get_tag
    } State_t;

    // present and future states
    State_t state, next_state;

    // fsm internal signals
    logic [4:0] mux_ctrl_s; // signal de controle du mux de lecture de la trame ecg
    logic [63:0] mux_data_s; // signal de lecture de la trame ecg

    // mux de lecture de la trame ecg
    genvar i;
    generate
        for (i = 0; i < 23; i = i + 1) begin : mux_gen
            always_comb begin
                if (mux_ctrl_s == i) begin
                    mux_data_s <= data_i[1471 - i*64 -: 64];
                end
            end
        end
    endgenerate


    // fsm always_ff block
    always_ff @(posedge clock_i or posedge reset_i) begin
        if (reset_i == 1'b1) begin
            state <= idle;
        end else begin
            state <= next_state;
        end
    end

    // fsm next_state logic
    always_comb begin
        next_state = state;
        case(state)
            idle: begin
                if (start_i == 1'b1) begin
                    next_state = init;
                end
            end

            init: begin
                next_state = wait_end_init;
            end

            wait_end_init: begin
                if (end_initialisation_i == 1'b1) begin
                    next_state = associate_data;
                end
            end

            // 
            associate_data: begin
                next_state = end_associate_data;
            end

            end_associate_data: begin
                next_state = wait_end_associate;
            end

            wait_end_associate: begin
                if (end_associate_i == 1'b1) begin
                    next_state = pt_set_data;
                end
            end



            pt_set_data: begin
                next_state = pt_wait_cipher_valid;
            end

            pt_wait_cipher_valid: begin
                if (cipher_valid_i == 1'b1) begin
                    next_state = pt_get_cipher;
                end
            end

            pt_get_cipher: begin
                next_state = pt_wait_end_cipher;
            end

            pt_wait_end_cipher: begin
                // soit on boucle soit on sort
                if (end_cipher_i == 1'b1) begin
                    if (mux_ctrl_s == 21) begin
                        mux_ctrl_s = mux_ctrl_s + 1;
                        next_state = finalisation;
                    end else begin
                        mux_ctrl_s = mux_ctrl_s + 1;
                        next_state = pt_set_data;
                    end
                end
            end

            finalisation: begin
                if (cipher_valid_i == 1'b1) begin
                    next_state = pt_get_final_cipher;
                end
            end

            pt_get_final_cipher: begin
                next_state = wait_end_tag;
            end

            wait_end_tag: begin
                if (end_tag_i == 1'b1) begin
                    next_state = get_tag;
                end
            end

            get_tag: begin
                next_state = idle;
            end
        endcase
    end






    // fsm outputs
    assign key_o = 128'h8A_55_11_4D_1C_B6_A9_A2_BE_26_3D_4D_7A_EC_AA_FF;
    assign nonce_o = 128'h4E_D0_EC_0B_98_C5_29_B7_C8_CD_DF_37_BC_D0_28_4A;

    always_comb begin
        case(state)
            idle: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                mux_ctrl_s = 0;
            end

            init: begin
                init_o = 1'b1;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                mux_ctrl_s = 0;
            end

            wait_end_init: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                mux_ctrl_s = 0;
            end

            associate_data: begin
                init_o = 1'b0;
                associate_data_o = 1'b1;
                finalisation_o = 1'b0;
                data_o = 64'h41_20_74_6F_20_42_80_00;
                data_valid_o = 1'b0;
                mux_ctrl_s = 0;
            end

            end_associate_data: begin
                init_o = 1'b0;
                associate_data_o = 1'b1;
                finalisation_o = 1'b0;
                data_o = 64'h41_20_74_6F_20_42_80_00;
                data_valid_o = 1'b1;
                mux_ctrl_s = 0;
            end

            wait_end_associate: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h41_20_74_6F_20_42_80_00;
                data_valid_o = 1'b0;
                mux_ctrl_s = 0;
            end

            // deb for
            pt_set_data: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b1;
            end

            pt_wait_cipher_valid: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b0; //
            end

            pt_get_cipher: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b0;
            end

            pt_wait_end_cipher: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b0;
            end
            // fin for

            finalisation: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1;
            end

            pt_get_final_cipher: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1;
            end

            wait_end_tag: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1;
            end

            get_tag: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1;
            end
        endcase
    end


endmodule
