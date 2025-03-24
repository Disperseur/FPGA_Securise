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

        input logic [63:0] associate_data_i,
        input logic         end_associate_i,
        input logic         cipher_valid_i,
        input logic         end_tag_i,
        input logic         end_initialisation_i,
        input logic         end_cipher_i,

        // outputs
        output logic         init_o,
        output logic         associate_data_o, //0: plain text; 1: DA
        output logic         finalisation_o,
        output logic [ 63:0] data_o,
        output logic         data_valid_o,
        output logic         en_reg_ascon_for_cipher_o
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
        get_tag,
        wait_restart
    } State_t;

    // present and future states
    State_t state, next_state;
    
    
    
    
    
    
    
    

    // fsm internal signals
    logic [4:0] mux_ctrl_s; // signal de controle du mux de lecture de la trame ecg
    logic [63:0] mux_data_s; // signal de lecture de la trame ecg
    // Pour gerer le MUX   
    logic reset_counter_o; 
    logic enable_counter_o;
    


    // mux de lecture de la trame ecg
    // genvar i;
    // generate
    //     for (i = 0; i < 23; i = i + 1) begin : mux_gen
    //         always_comb begin
    //             if (mux_ctrl_s == i) begin
    //                 mux_data_s <= data_i[1471 - i*64 -: 64];
    //             end
    //         end
    //     end
    // endgenerate

    always_comb begin
        case(mux_ctrl_s)
            5'h00: mux_data_s  = data_i[1471:1408];
            5'h01: mux_data_s  = data_i[1407:1344];
            5'h02: mux_data_s  = data_i[1343:1280];
            5'h03: mux_data_s  = data_i[1279:1216];
            5'h04: mux_data_s  = data_i[1215:1152];
            5'h05: mux_data_s  = data_i[1151:1088];
            5'h06: mux_data_s  = data_i[1087:1024];
            5'h07: mux_data_s  = data_i[1023:960];
            5'h08: mux_data_s  = data_i[959:896];
            5'h09: mux_data_s = data_i[895:832];
            5'h0A: mux_data_s = data_i[831:768];
            5'h0B: mux_data_s = data_i[767:704];
            5'h0C: mux_data_s = data_i[703:640];
            5'h0D: mux_data_s = data_i[639:576];
            5'h0E: mux_data_s = data_i[575:512];
            5'h0F: mux_data_s = data_i[511:448];
            5'h10: mux_data_s = data_i[447:384];
            5'h11: mux_data_s = data_i[383:320];
            5'h12: mux_data_s = data_i[319:256];
            5'h13: mux_data_s = data_i[255:192];
            5'h14: mux_data_s = data_i[191:128];
            5'h15: mux_data_s = data_i[127:64];
            5'h16: mux_data_s = data_i[63:0];
            default: mux_data_s = 0;
        endcase
    end


    // fsm always_ff block
    always_ff @(posedge clock_i or posedge reset_i) begin
        if (reset_i == 1'b1) begin
            state <= idle;
        end else begin
            state <= next_state;

            if (enable_counter_o == 1'b1) begin
                if (reset_counter_o == 1'b1) begin
                    // compteur = 0
                    mux_ctrl_s = 5'b0;
                end else begin
                    // on incremente
                    mux_ctrl_s = mux_ctrl_s + 1;    
                end
            end else begin
                // compteur = compteur 
                mux_ctrl_s = mux_ctrl_s;
            end
        end
    end



    // fsm next_state logic
    always_comb begin
        // next_state = state;
        case(state)
            idle: begin
                if (start_i == 1'b1) begin
                    next_state = init;
                end else begin
                    next_state = idle;
                end
            end

            init: begin
                next_state = wait_end_init;
            end

            wait_end_init: begin
                if (end_initialisation_i == 1'b1) begin
                    next_state = associate_data;
                end else begin
                    next_state = wait_end_init;
                end
            end

            associate_data: begin
                next_state = end_associate_data;
            end

            end_associate_data: begin
                next_state = wait_end_associate;
            end

            wait_end_associate: begin
                if (end_associate_i == 1'b1) begin
                    next_state = pt_set_data;
                end else begin
                    next_state = wait_end_associate;
                end
                
                // mux_ctrl_s = 0;
            end



            pt_set_data: begin
                next_state = pt_wait_cipher_valid;
            end

            pt_wait_cipher_valid: begin
                if (cipher_valid_i == 1'b1) begin
                    next_state = pt_get_cipher;
                end else begin
                    next_state = pt_wait_cipher_valid;
                end
            end

            pt_get_cipher: begin
                next_state = pt_wait_end_cipher;
            end

            pt_wait_end_cipher: begin
                // soit on boucle soit on sort
                if (end_cipher_i == 1'b1) begin
                    if (mux_ctrl_s == 22) begin
                        // mux_ctrl_s = mux_ctrl_s + 1;
                        next_state = finalisation;
                    end else begin
                        // mux_ctrl_s = mux_ctrl_s + 1;
                        next_state = pt_set_data;
                    end
                end else begin
                    next_state = pt_wait_end_cipher;
                end
            end

            finalisation: begin
                if (cipher_valid_i == 1'b1) begin
                    next_state = pt_get_final_cipher;
                end else begin
                    next_state = finalisation;
                end
            end

            pt_get_final_cipher: begin
                next_state = wait_end_tag;
            end

            wait_end_tag: begin
                if (end_tag_i == 1'b1) begin
                    next_state = get_tag;
                end else begin
                    next_state = wait_end_tag;
                end
            end

            get_tag: begin
                next_state = wait_restart;
            end

            wait_restart: begin
                if (start_i == 1'b1) begin
                    next_state = wait_restart;
                end else begin
                    next_state = idle;
                end
            end
        endcase
    end



    always_comb begin
        case(state)
            idle: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            init: begin
                init_o = 1'b1;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b1; //
                enable_counter_o = 1'b1; //
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            wait_end_init: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            associate_data: begin
                init_o = 1'b0;
                associate_data_o = 1'b1;
                finalisation_o = 1'b0;
                data_o = associate_data_i; //64'h41_20_74_6F_20_42_80_00;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            end_associate_data: begin
                init_o = 1'b0;
                associate_data_o = 1'b1;
                finalisation_o = 1'b0;
                data_o = associate_data_i;//64'h41_20_74_6F_20_42_80_00;
                data_valid_o = 1'b1;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            wait_end_associate: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = associate_data_i; //64'h41_20_74_6F_20_42_80_00;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            // deb for
            pt_set_data: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b1; //
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            pt_wait_cipher_valid: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            pt_get_cipher: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b1; //
                en_reg_ascon_for_cipher_o = 1'b1; //
            end

            pt_wait_end_cipher: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = mux_data_s;
                data_valid_o = 1'b0;
                enable_counter_o = 1'b0;
                reset_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end
            // fin for

            finalisation: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1; //
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            pt_get_final_cipher: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1; //
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            wait_end_tag: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1; //
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end

            get_tag: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b1;
                data_o = mux_data_s;
                data_valid_o = 1'b1; //
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b1; //
            end


            wait_restart: begin
                init_o = 1'b0;
                associate_data_o = 1'b0;
                finalisation_o = 1'b0;
                data_o = 64'h0;
                data_valid_o = 1'b0;
                reset_counter_o = 1'b0;
                enable_counter_o = 1'b0;
                en_reg_ascon_for_cipher_o = 1'b0;
            end
        endcase
    end


endmodule
