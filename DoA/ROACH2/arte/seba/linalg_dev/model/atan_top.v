//`include "rtl/fifo_sync.v"
//`include "rtl/bram_infer.v"
//`include "rtl/arctan2.v"
//`include "rtl/arctan.v"
//`include "rtl/rom.v"
//`include "rtl/autoscale.v"
//`include "rtl/first_one_finder.v"


module atan2_top #(
    parameter DIN_WIDTH = 16,
    parameter VECTOR_LEN = 512,
    parameter ATAN_FILE = "atan_rom.hex"
) (
    input wire clk,
    input wire ce,
    input wire rst,

    input wire [8:0] addr_in,
    input wire signed [15:0] eigen1_y, eigen_x,
    input wire w_valid,

    output wire [8:0] addr_out,
    output wire [15:0] phase1,
    output wire phase_valid 
);


reg en_save =0, w_valid_r=0;
always@(posedge clk)begin
    w_valid_r <= w_valid;
    //detect rising edge
    if(rst)
        en_save <=0;
    else if(~w_valid_r & w_valid)
        en_save <=1;
    else
        en_save <= en_save;
end

//delay the la output to match en_save
reg [DIN_WIDTH-1:0] eig1=0, eig_frac=0;
reg [$clog2(VECTOR_LEN)-1:0] addr_r=0;
always@(posedge clk)begin
    eig1 <= eigen1_y; eig_frac <= eigen_x;
    addr_r <= addr_in;
end


//fifo to multiplex the arctan
wire fifo_full, fifo_empty;
wire read_valid;
reg read_req=0, read_req_r=0;

wire [DIN_WIDTH-1:0] e1, e_frac;
wire [$clog2(VECTOR_LEN)-1:0] addr_fifo;

fifo_sync #(
    .DIN_WIDTH(2*DIN_WIDTH+$clog2(VECTOR_LEN)),
    .FIFO_DEPTH(VECTOR_LEN)
) fifo_sync_inst (
    .clk(clk),
    .rst(rst),
    .wdata({eig1,eig_frac, addr_r}),
    .w_valid(en_save & w_valid_r),
    .empty(fifo_empty),
    .full(fifo_full),
    .rdata({e1, e_frac, addr_fifo}),
    .r_valid(read_valid),
    .read_req(read_req)
);

assign addr_out = addr_fifo;
//cordic atan2
always@(posedge clk)begin
    read_req_r <= read_req;
    if(~fifo_empty & atan_read_req & (~read_req_r & ~read_req) )
        read_req <= 1;
    else
        read_req <=0;
end

wire atan_read_req;

arctan2 #(
    .DIN_WIDTH(DIN_WIDTH),
    .DOUT_WIDTH(DIN_WIDTH),
    .ROM_FILE(ATAN_FILE),
    .MAX_SHIFT(7)
) arctan2_inst (
    .clk(clk),
    .y(e1),
    .x(e_frac),
    .din_valid(read_valid),
    .sys_ready(atan_read_req),
    .dout(phase1),
    .dout_valid(phase_valid)
);

endmodule
