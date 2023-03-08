
`include "/home/Workspace/seba/frb_actual/includes.v"
module packetizer_top 
 (
    input wire clk,
    input wire ce,
    input wire rst,
    input wire [127:0] din,
    input wire din_valid,
    
    //configuration signals
    input wire [31:0] pkt_len,
    input wire [31:0] sleep_cycles,
    input wire [31:0] config_tx_dest_ip,
    input wire [31:0] config_tx_dest_port,

    //to the TGE 
    output wire [63:0] tx_data,
    output wire tx_valid,
    output wire [31:0] tx_dest_ip,
    output wire [15:0] tx_dest_port,
    output wire tx_eof,

    output wire fifo_full
);


tge_write_packetizer #(
    .DIN_WIDTH(128),
    .FIFO_DEPTH(512)
) tge_write_inst (
    .clk(clk),
    .rst(rst),
    .din(din),
    .din_valid(din_valid),
    .pkt_len(pkt_len),
    .sleep_cycles(sleep_cycles),
    .config_tx_dest_ip(config_tx_dest_ip),
    .config_tx_dest_port(config_tx_dest_port),
    .tx_data(tx_data),
    .tx_valid(tx_valid),
    .tx_dest_ip(tx_dest_ip),
    .tx_dest_port(tx_dest_port),
    .tx_eof(tx_eof),
    .fifo_full(fifo_full)
);

endmodule
