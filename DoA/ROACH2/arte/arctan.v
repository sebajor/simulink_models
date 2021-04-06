// `default_nettype none

// `include "/home/franco/Diego/Doa_ordenado/sqrt_hex.mem"

module arctan #(
    parameter OUT_WIDTH = 16,
    parameter OUT_INT = 10,
    parameter IN_WIDTH = 16,
    parameter IN_INT = 16,
    parameter FILENAME = "/home/franco/Diego/Doa_ordenado/arctan_hex.mem"
)(
    input clk,	
    input ce,
    input [15:0] din,
    input din_valid,
    output [15:0] dout,
    output dout_valid
);

    reg [15:0] mem [0:(2 ** 16 - 1)];
    reg [15:0] dout_r = 0;
    reg valid_r = 0;

    initial begin
        $readmemh(FILENAME, mem);
    end
    
    always@(posedge clk) begin
        if(din_valid) begin
            dout_r <= mem[din];     
        end
    end

    always@(posedge clk) begin
        if(din_valid)
            valid_r <= 1;
        else
            valid_r <=0;
    end
    
    assign dout = dout_r;
    assign dout_valid = valid_r;

endmodule 
