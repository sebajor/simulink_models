
module pkt_gen_top
 (
    input wire clk,
    input wire ce,
    input wire en,
    input wire rst,

    input wire [31:0] burst_len,
    input wire [31:0] sleep_write,

    output wire [127:0] dout,
    output wire dout_valid
);

pkt_gen #(
    .DOUT_WIDTH(8),
    .PARALLEL(16)
) pkt_gen_inst (
    .clk(clk),
    .en(en),
    .rst(rst),
    .burst_len(burst_len),
    .sleep_write(sleep_write),
    .dout(dout),
    .dout_valid(dout_valid)
);

endmodule
