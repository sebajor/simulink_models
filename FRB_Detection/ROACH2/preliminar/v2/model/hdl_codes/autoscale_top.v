
module autoscale_top (
    input wire clk,
    input wire ce,
    input wire [31:0] din1, din2,
    input wire din_valid,
    output wire [31:0] dout1, dout2,
    output wire dout_valid,
    output wire [5:0] shift_val
);

autoscale #(
    .MAX_SHIFT(14),
    .MIN_SHIFT(4),
    .DIN_WIDTH(32)
) autoscale_inst (
    .clk(clk),
    .din1(din1), 
    .din2(din2),
    .din_valid(din_valid),
    .dout1(dout1),
    .dout2(dout2),
    .dout_valid(dout_valid),
    .shift_value(shift_val)
);


endmodule
