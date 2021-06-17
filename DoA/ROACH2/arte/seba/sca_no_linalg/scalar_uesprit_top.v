
module scalar_uesprit_top #(
    parameter DIN_WIDTH = 18,
    parameter DIN_POINT = 17,
    parameter ACC_WIDTH = 18,
    parameter ACC_POINT = 17,
    parameter DOUT_WIDTH = 32
) (
    input wire clk,
    input wire ce,

    input wire signed [17:0] din1_re, din1_im,
    input wire signed [17:0] din2_re, din2_im,
    input wire din_valid,
    
    input wire new_acc,
    
    output wire [31:0] r11, r22, r12,
    output wire dout_valid
);


scalar_uesprit #(
    .DIN_WIDTH(DIN_WIDTH),
    .DIN_POINT(DIN_POINT),
    .ACC_WIDTH(ACC_WIDTH),
    .ACC_POINT(ACC_POINT),
    .DOUT_WIDTH(DOUT_WIDTH),
) scalar_uesprit_inst (
    .clk(clk),
    .new_acc(new_acc),
    .din1_re(din1_re),
    .din1_im(din1_im),
    .din2_re(din2_re),
    .din2_im(din2_im),
    .din_valid(din_valid),
    .r11(r11),
    .r22(r22),
    .r12_re(r12),
    .r12_im(),
    .dout_valid(dout_valid)
);


endmodule
