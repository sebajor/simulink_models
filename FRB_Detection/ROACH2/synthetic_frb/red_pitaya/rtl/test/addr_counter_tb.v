`default_nettype none
`include "addr_counter.v"

module addr_counter_tb #(
    parameter ADDR_SIZE = 8
) (
    input wire clk,
    input wire en,
    input wire [31:0] decimate,
    output wire [ADDR_SIZE-1:0] addr,
    output wire addr_valid,
    output wire finish
);



addr_counter #(
    .ADDR_SIZE(ADDR_SIZE) 
) addr_counter_inst (
    .clk(clk),
    .en(en),
    .decimate(decimate),
    .addr(addr),
    .addr_valid(addr_valid),
    .finish(finish)
);

initial begin
    $dumpfile("traces.vcd");
    $dumpvars();
end

endmodule
