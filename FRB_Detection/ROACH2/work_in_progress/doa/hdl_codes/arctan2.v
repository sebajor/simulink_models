module arctan2 #(
    parameter OUT_WIDTH = 16,
    parameter OUT_INT = 12,
    parameter IN_WIDTH = 18,
    parameter IN_INT = 18,
    parameter FILENAME = "/home/franco/Diego/Doa_ordenado/arctan_hex2.mem"
)(
    input clk,	
    input ce,
    input [17:0] din,
    input din_valid,
    output [15:0] dout,
    output dout_valid
);

    reg [17:0] mem [0:(2 ** 18 - 1)];
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
