module piso #(
    parameter INPUT_SIZE = 1024,
    parameter OUTPUT_SIZE = 64
)
(
    input wire clk,
    input wire ce,
    input wire rst,
    //stupid matlab
    //input wire [INPUT_SIZE-1:0] i_parallel,
    //output wire [OUTPUT_SIZE-1:0] o_serial,
    input wire [1023:0] i_parallel,
    output wire [63:0] o_serial,

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
            if(counter==(CYCLES_BTW)-1) next_state = IDLE;
            else                        next_state = BUSY;
        end
    endcase 
end

always@(posedge clk)begin
    case(state)
        IDLE: begin
            counter<=0;
            valid_r <= 0;
        end
        BUSY: begin
            valid_r<= 1;
            counter <= counter +1;
        end
    endcase
end


always@(posedge clk)begin
    re = ~state && next_state && ~rst;
end

//detect the transition of states
assign fifo_re = re; 


reg [OUTPUT_SIZE-1:0] serial_out=0;

/*
always@(*)begin
    case(counter)
        1: serial_out = i_parallel[OUTPUT_SIZE-1:0];
        2: serial_out = i_parallel[2*OUTPUT_SIZE-1:1*OUTPUT_SIZE];
        3: serial_out = i_parallel[3*OUTPUT_SIZE-1:2*OUTPUT_SIZE];
        0: serial_out = i_parallel[4*OUTPUT_SIZE-1:3*OUTPUT_SIZE];
    endcase
end
*/


always@(posedge clk)begin
    case(counter)
        1: serial_out = i_parallel[OUTPUT_SIZE-1:0];   
        2: serial_out = i_parallel[2*OUTPUT_SIZE-1:1*OUTPUT_SIZE];
        3: serial_out = i_parallel[3*OUTPUT_SIZE-1:2*OUTPUT_SIZE];
        4: serial_out = i_parallel[4*OUTPUT_SIZE-1:3*OUTPUT_SIZE];
        5: serial_out = i_parallel[5*OUTPUT_SIZE-1:4*OUTPUT_SIZE];
        6: serial_out = i_parallel[6*OUTPUT_SIZE-1:5*OUTPUT_SIZE];
        7: serial_out = i_parallel[7*OUTPUT_SIZE-1:6*OUTPUT_SIZE];
        8: serial_out = i_parallel[8*OUTPUT_SIZE-1:7*OUTPUT_SIZE];
        9: serial_out = i_parallel[9*OUTPUT_SIZE-1:8*OUTPUT_SIZE];
        10: serial_out = i_parallel[10*OUTPUT_SIZE-1:9*OUTPUT_SIZE];
        11: serial_out = i_parallel[11*OUTPUT_SIZE-1:10*OUTPUT_SIZE];
        12: serial_out = i_parallel[12*OUTPUT_SIZE-1:11*OUTPUT_SIZE];
        13: serial_out = i_parallel[13*OUTPUT_SIZE-1:12*OUTPUT_SIZE];
        14: serial_out = i_parallel[14*OUTPUT_SIZE-1:13*OUTPUT_SIZE];
        15: serial_out = i_parallel[15*OUTPUT_SIZE-1:14*OUTPUT_SIZE];
        0: serial_out = i_parallel[16*OUTPUT_SIZE-1:15*OUTPUT_SIZE];
    endcase
end

/*
always@(*)begin
    integer i;
    for(i=0; i<CYCLES_BTW;i=i+1)begin: loop
        if(counter==i)begin
            serial_out = i_parallel[(i+1)*OUTPUT_SIZE-1:i*OUTPUT_SIZE];
        end
    end
end
*/

//just lookin at the traces, we need a delay in the valid signal
reg valid_delay=0;
always@(posedge clk)begin
    valid_delay = valid_r;
end


assign valid = valid_delay;//valid_r;
assign o_serial = serial_out; 
endmodule 
