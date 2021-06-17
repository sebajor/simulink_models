//`default_nettype none
//`include "includes.v"

module v_uesprit_la_top #(
    parameter DIN_WIDTH = 18,
    parameter DIN_POINT = 17,
    //correlation matrix parameters
    parameter VECTOR_LEN = 512,
    parameter CORR_WIDTH = 24,		//over 22 gives problems :(
    parameter CORR_POINT = 17,
    parameter CORR_DOUT_WIDTH = 32,
    //linear algebra parameters
    parameter LA_IN_WIDTH = 16,
    parameter LA_IN_POINT = 15,
    parameter SQRT_IN_WIDTH = 10,
    parameter SQRT_IN_POINT = 7,
    parameter DOUT_WIDTH = 16,
    parameter DOUT_POINT = 13,
    parameter SQRT_FILE = "sqrt.hex"
) (
    input wire clk,
    input wire ce,

    input wire signed [17:0] din1_re, din1_im,
    input wire signed [17:0] din2_re, din2_im,
    input wire din_valid,
    input wire new_acc,
    
    //for debugging
    input wire [4:0] shift,
    output wire signed [15:0] r11, r22, r12_re,
    output wire corr_valid,
    
    //linear algebra outputs
    output wire signed [15:0] lamb1, lamb2,
    output wire signed [15:0] eigen1_y, eigen2_y, eigen_x,
    output wire dout_valid
);



v_uesprit_la #(
    .DIN_WIDTH(DIN_WIDTH),
    .DIN_POINT(DIN_POINT),
    .VECTOR_LEN(VECTOR_LEN), 
    .CORR_WIDTH(CORR_WIDTH),
    .CORR_POINT(CORR_POINT),
    .CORR_DOUT_WIDTH(CORR_DOUT_WIDTH), 
    .LA_IN_WIDTH(LA_IN_WIDTH), 
    .LA_IN_POINT(LA_IN_POINT), 
    .SQRT_IN_WIDTH(SQRT_IN_WIDTH), 
    .SQRT_IN_POINT(SQRT_IN_POINT),
    .DOUT_WIDTH(DOUT_WIDTH), 
    .DOUT_POINT(DOUT_POINT),
    .SQRT_FILE(SQRT_FILE)
) v_uesprit_la_inst (
    .clk(clk),
    .din1_re(din1_re),
    .din1_im(din1_im),
    .din2_re(din2_re),
    .din2_im(din2_im),
    .din_valid(din_valid),
    .new_acc(new_acc),
    .shift(shift),
    .r11(r11),
    .r22(r22),
    .r12_re(r12_re),
    .r12_im(),
    .corr_valid(corr_valid),
    .lamb1(lamb1),
    .lamb2(lamb2),
    .eigen1_y(eigen1_y),
    .eigen2_y(eigen2_y),
    .eigen_x(eigen_x),
    .dout_valid(dout_valid)
);



endmodule 
