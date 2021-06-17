
module eigen_top #(
    parameter DIN_WIDTH = 16,
    parameter DIN_POINT = 15,
    parameter SQRT_IN_WIDTH = 10,
    parameter SQRT_IN_POINT = 7,
    parameter DOUT_WIDTH = 16,
    parameter DOUT_POINT = 13,
    parameter VEC_LEN = 512,
    parameter SQRT_FILE = "sqrt.hex"
) (
    input wire clk,
    input wire ce,
    
    input wire rst,
    input wire [15:0] r11, r22,
    input wire signed [15:0] r12,
    input wire din_valid,

    output wire signed [15:0] lamb1, lamb2,
    output wire signed [15:0] eigen1_y, eigen2_y, eigen_x,
    output wire [8:0] addr,
    output wire dout_valid
);


eigen #(
    .DIN_WIDTH(DIN_WIDTH),
    .DIN_POINT(DIN_POINT),
    .SQRT_IN_WIDTH(SQRT_IN_WIDTH), 
    .SQRT_IN_POINT(SQRT_IN_POINT),
    .DOUT_WIDTH(DOUT_WIDTH),
    .DOUT_POINT(DOUT_POINT),
    .SQRT_FILE(SQRT_FILE) 
) eigen_inst (
    .clk(clk),
    .r11(r11),
    .r22(r22),
    .r12(r12),
    .din_valid(din_valid),
    .lamb1(lamb1), 
    .lamb2(lamb2),
    .eigen1_y(eigen1_y),
    .eigen2_y(eigen2_y),
    .eigen_x(eigen_x),
    .dout_valid(dout_valid)
);

reg [$clog2(VEC_LEN)-1:0] counter=0;
reg [15*$clog2(VEC_LEN)-1:0] count_delay=0;
always@(posedge clk)begin
    if(rst)begin
        counter<=0;
        count_delay <= 0;
    end
    else if(din_valid)begin
        counter <= counter+1;
        count_delay <= {count_delay[14*$clog2(VEC_LEN)-1:0], counter};
    end
end

assign addr = count_delay[15*$clog2(VEC_LEN)-1:14*$clog2(VEC_LEN)];

endmodule 
