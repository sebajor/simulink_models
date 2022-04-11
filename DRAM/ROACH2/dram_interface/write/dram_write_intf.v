
module roach_dram_write_tb
(
    input wire clk,
    input wire ce,
    input wire rst,
    input wire en_write,

    input wire [31:0] din,
    input wire din_valid,

    //to the DRAM module
    output wire dram_rst, 
    output wire [24:0] dram_addr,   //check!
    output wire [287:0] dram_data,

    output wire [35:0] wr_be,       //byte enable
    output wire rwn,                //1:read, 0:write
    output wire [31:0] cmd_tag,
    output wire cmd_valid
);


roach_dram_write #(
    .DIN_WIDTH(32),
    .DRAM_ADDR(25)
) roach_dram_write_inst (
    .clk(clk),
    .rst(rst),
    .en_write(en_write),
    .din(din),
    .din_valid(din_valid),
    .dram_rst(dram_rst), 
    .dram_addr(dram_addr),
    .dram_data(dram_data),
    .wr_be(wr_be),
    .rwn(rwn),
    .cmd_tag(cmd_tag),
    .cmd_valid(cmd_valid)
);

endmodule
