//`include "includes.v"
/*
*   Author: Sebastian Jorquera
*   Interface for the arctan2 module. It receives multiple inputs
*   at the time, store them into a RAM and then read one by one and
*   insert it in the arctan2 module
*   
*   Be carefull of not fill the RAM fifo.
*/

module arctan2_multiplexed #(
    parameter DIN_WIDTH = 16,
    parameter DOUT_WIDTH = 16,
    parameter PARALLEL = 4,
    parameter ROM_FILE = "/home/Workspace/seba/cordic_test/atan_rom.mem",
    parameter MAX_SHIFT = 7,
    parameter FIFO_DEPTH = 8    //2**
) (
    input wire clk,
    input wire ce,
    input wire rst,
    input wire [PARALLEL*DIN_WIDTH-1:0] x,y,
    input wire din_valid,

    output wire [DOUT_WIDTH-1:0] dout, 
    output wire dout_valid,
    output wire fifo_full
);

wire signed [DIN_WIDTH-1:0] x_fifo, y_fifo;
wire fifo_valid, fifo_ready;

wire [1:0] fifo_full_aux;
assign fifo_full = fifo_full_aux[0];

wire [1:0] fifo_valid_aux;
assign fifo_valid = fifo_valid_aux[0];

piso #(
    .DIN_WIDTH(PARALLEL*DIN_WIDTH),
    .DOUT_WIDTH(DIN_WIDTH),
    .FIFO_DEPTH(2**FIFO_DEPTH)
) piso_inst [1:0] (
    .clk(clk),
    .rst(rst),
    .din({x,y}),
    .din_valid(din_valid),
    .dout({x_fifo, y_fifo}),
    .dout_valid(fifo_valid_aux),
    .dout_ready(fifo_ready),
    .fifo_full(fifo_full_aux)
);




arctan2 #(
    .DIN_WIDTH(DIN_WIDTH),
    .DOUT_WIDTH(DOUT_WIDTH),
    .ROM_FILE(ROM_FILE),
    .MAX_SHIFT(MAX_SHIFT)
) arctan2_inst (
    .clk(clk),
    .y(y_fifo),
    .x(x_fifo),
    .din_valid(fifo_valid),
    .sys_ready(fifo_ready),
    .dout(dout),
    .dout_valid(dout_valid)
);

endmodule
