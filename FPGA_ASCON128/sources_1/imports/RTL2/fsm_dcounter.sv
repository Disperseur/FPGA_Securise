`timescale 1ns / 1ps
//Description: counter for storing or flushing data to uart
module fsm_dcounter
  import uart_pkg::*;
(
    input  logic       clock_i,      //main clock
    input  logic       resetb_i,     //asynchronous reset active low
    input  logic       en_i,
    input  logic       init_c16_i,   //storing AD
    input  logic       init_c17_i,   //flushing tag
    input  logic       init_c32_i,   //storing key or nonce
    input  logic       init_c184_i,  //flushing cipher
    input  logic       init_c366_i,  //storing wave
    output logic [8:0] cpt_o
);
  logic [8:0] cpt_s;

  always_ff @(posedge clock_i or negedge resetb_i) begin : seq_0
    if (resetb_i == 1'b0) cpt_s <= '1;
    else begin
      if (en_i == 1'b1) begin
        if (init_c16_i == 1'b1) begin
          cpt_s <= 9'd8;  //16
        end else begin
          if (init_c17_i == 1'b1) begin
            cpt_s <= 9'd17;
          end else begin
            if (init_c32_i == 1'b1) begin
              cpt_s <= 9'd16;  //32
            end else begin
              if (init_c184_i == 1'b1) begin
                cpt_s <= 9'd185;
              end else begin
                if (init_c366_i == 1'b1) begin
                  cpt_s <= 9'd184;  //368
                end else begin
                  cpt_s <= cpt_s - 1;
                end
              end
            end
          end
        end
      end else begin
        cpt_s <= cpt_s;
      end
    end
  end : seq_0
  assign cpt_o = cpt_s;

endmodule : fsm_dcounter
