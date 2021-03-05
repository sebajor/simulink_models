module piso #(
    parameter INPUT_SIZE = 512,
    parameter OUTPUT_SIZE = 256
)
(
    input wire clk,
    input wire ce,
    input wire rst,
    //stupid matlab
    //input wire [INPUT_SIZE-1:0] i_parallel,
    //output wire [OUTPUT_SIZE-1:0] o_serial,
    input wire [511:0] i_parallel,
    output wire [255:0] o_serial,

    input wire      fifo_empty,
    output wire     fifo_re,

    output wire     valid
);

// module that interface a fifo that contains parallel data
//that we wish to serialize.
//note that for each value that we read from the fifo we need 
// INPUT_SIZE/OUTPUT_SIZE cycles until we could read the next val


//fucking sysgen
//parameter CYCLES_BTW = INPUT_SIZE/OUTPUT_SIZE; 

//parameter IDLE = 2'b0;
//parameter BUSY = 2'b1;
localparam CYCLES_BTW = INPUT_SIZE/OUTPUT_SIZE; 
localparam IDLE = 2'b0;
localparam BUSY = 2'b1;


reg [$clog2(CYCLES_BTW)-1:0] counter=0;
reg re=0, valid_r=0; //read enable and valid..
reg state=IDLE, next_state=IDLE;

reg counter_busy=0;

always@(posedge clk)begin
    if(rst)
        state <= IDLE;
    else
        state <= next_state;
end


always@(*)begin
    case(state)
        IDLE:   begin
            if(~fifo_empty)     next_state = BUSY;
            else                next_state = IDLE;
        end
        BUSY:   begin
            if(counter==1 && counter_busy==1) next_state = IDLE;
            else                        next_state = BUSY;
        end
    endcase 
end

always@(posedge clk)begin
    case(state)
        IDLE: begin
            counter<=0;
            valid_r <= 0;
            counter_busy <=0;
        end
        BUSY: begin
            counter_busy <= counter_busy+1;
            if(counter_busy==1)begin
                valid_r <= 1;
                counter <= counter +1;
            end
            else begin
                valid_r <=0;
            end
        end
    endcase
end


always@(posedge clk)begin
    re = ~state && next_state && ~rst;
end

//detect the transition of states
assign fifo_re = re; 


reg [OUTPUT_SIZE-1:0] serial_out=0;

always@(posedge clk)begin
    case(counter)
        1: serial_out = i_parallel[OUTPUT_SIZE-1:0];   
        0: serial_out = i_parallel[2*OUTPUT_SIZE-1:1*OUTPUT_SIZE];
    endcase
end


//just lookin at the traces, we need a delay in the valid signal
reg valid_delay=0;
always@(posedge clk)begin
    valid_delay = valid_r;
end


assign valid = valid_delay;//valid_r;
assign o_serial = serial_out; 
endmodule 
