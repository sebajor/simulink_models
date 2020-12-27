`default_nettype none
`include "cic.v"

module cic_tb #(
    parameter DIN_WIDTH = 16,
    parameter STAGES = 3,     //M  
    parameter DECIMATION = 8, //R
    parameter DIFF_DELAY = 1,  //N=D/R
    parameter DOUT_WIDTH = DIN_WIDTH + STAGES*$clog2(DECIMATION*DIFF_DELAY)
) (
    input wire clk_in,
    input wire rst,
    input wire signed [DIN_WIDTH-1:0] din,
    output wire signed [DOUT_WIDTH-1:0] dout,
    output wire clk_out
);



cic #(
    .DIN_WIDTH(16),
    .STAGES(3),     //M  
    .DECIMATION(8), //R
    .DIFF_DELAY(1)  //N=D/R
) cic_inst (
    .clk_in(clk_in),
    .rst(rst),
    .din(din),
    .dout(dout),
    .clk_out(clk_out)
);

initial begin
    $dumpfile("traces.vcd");
    $dumpvars();
end

endmodule
