`default_nettype none

module addr_counter #(
    parameter ADDR_SIZE = 8
) (
    input wire clk,
    input wire en,
    input wire [31:0] decimate,

    output wire [ADDR_SIZE-1:0] addr,
    output wire addr_valid,
    output wire finish
);

reg en_r = 0, addr_valid_r=0;
reg [ADDR_SIZE-1:0] counter=0;
reg [31:0] dec_counter =0;
reg [31:0] dec_factor=0;
reg stop=0;


always@(posedge clk) begin
    en_r <=en;
    dec_factor<= decimate;
end

always@(posedge clk)begin
    if(en_r & ~en)begin
        //falling edge rst everything
        dec_counter <=0;
        counter <=0;
        addr_valid_r <=0;
    end
    else if(en_r & en & ~stop)begin
        //rising edge start count
        if(dec_counter == dec_factor)begin
            dec_counter <= 0;
            counter <= counter+1;
            addr_valid_r <= 1;
        end
        else begin
            dec_counter <= dec_counter +1;
            addr_valid_r <= 0; 
        end
    end
    else begin
        dec_counter <= dec_counter;
        counter <= counter;
        addr_valid_r<= 0;
    end
end

always@(posedge clk)begin
    if(en_r & ~en)
        stop <=0;
    else if(&counter)begin
        stop <=1;
    end
    else
        stop <=stop; 
end

assign addr = counter;
assign addr_valid = addr_valid_r;
assign finish = stop;

endmodule
