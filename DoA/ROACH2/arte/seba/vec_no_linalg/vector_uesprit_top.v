
module vector_uesprit_top #(
    parameter DIN_WIDTH = 18,
    parameter DIN_POINT = 17,
    //correlation matrix parameters
    parameter VECTOR_LEN = 512,
    parameter ACC_WIDTH = 24,
    parameter ACC_POINT = 17,
    parameter DOUT_WIDTH = 32
) (
    input wire clk,
    input wire ce,

    input wire signed [17:0] din1_re, din1_im,
    input wire signed [17:0] din2_re, din2_im,
    input wire din_valid,
    
    input wire new_acc,
    output wire signed [31:0] r11, r22, r12_re,
    output wire dout_valid 
);

vector_uesprit #(
    .DIN_WIDTH(DIN_WIDTH),
    .DIN_POINT(DIN_POINT),
    .VECTOR_LEN(VECTOR_LEN),
    .ACC_WIDTH(ACC_WIDTH),
    .ACC_POINT(ACC_POINT),
    .DOUT_WIDTH(DOUT_WIDTH)
) vector_uesprit_inst (
    .clk(clk),
    .din1_re(din1_re),
    .din1_im(din1_im),
    .din2_re(din2_re),
    .din2_im(din2_im),
    .din_valid(din_valid),
    .new_acc(new_acc),
    .r11(r11),
    .r22(r22),
    .r12_re(r12_re),
    .r12_im(),
    .dout_valid(dout_valid)
);


endmodule
