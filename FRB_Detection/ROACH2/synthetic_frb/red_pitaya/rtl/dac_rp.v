
module dac_rp #(
    parameter DATA_WIDTH = 14
) (
    input wire clk,
    input wire [DATA_WIDTH-1:0] dac0,
    input wire [DATA_WIDTH-1:0] dac1,    
    input wire ce,
    input wire pll_rst,
    //DAC signals
    // the mode is hardcoded to interleaved
    output wire dac_clk,    //iqclk --> clka/qclk
    output wire dac_rst,    //iqrst --> clkb/iqrst
    output wire dac_sel,    //iqsel --> wrtb/iqsel
    output wire dac_wrt,    //iqwrt --> wrta/iqwrt
    output wire [DATA_WIDTH-1:0] dac_dat
);

wire pll_locked;
wire pll_clkfb;
wire ddr_clk;
/*generate the ddr clock
    fractional divide M = 8
    kintex vco range: (600-1200) mhz (this number comes from the datasheet)
    fvco = fin*M/D; fout=fin*M/(D*O)
    fin=100mhz, M=8, D=1 -> fvco=800
    O = 8 for clk1
*/

PLLE2_BASE #(
    .BANDWIDTH("OPTIMIZED"),  // OPTIMIZED, HIGH, LOW
    .CLKFBOUT_MULT(8),        // M (2-64)
    .DIVCLK_DIVIDE(1),        // D (1-56)
    .CLKFBOUT_PHASE(0.0),     // Phase offset in degrees of CLKFB, (-360.000-360.000).
    .CLKIN1_PERIOD(10.0),     // Input clock period in ns to ps resolution (i.e. 33.333 is 30 MHz).
    .REF_JITTER1(0.0),        // Reference input jitter in UI, (0.000-0.999).
    .STARTUP_WAIT("FALSE"),   // Delay DONE until PLL Locks, ("TRUE"/"FALSE")
            
    .CLKOUT0_DIVIDE(4),
    .CLKOUT0_DUTY_CYCLE(0.5),
    .CLKOUT0_PHASE(0.0),

    .CLKOUT1_DIVIDE(1),
    .CLKOUT1_DUTY_CYCLE(0.5),
    .CLKOUT1_PHASE(180.0),

    .CLKOUT2_DIVIDE(1),
    .CLKOUT2_DUTY_CYCLE(0.5),
    .CLKOUT2_PHASE(0.0),

    .CLKOUT3_DIVIDE(1),
    .CLKOUT3_DUTY_CYCLE(0.5),
    .CLKOUT3_PHASE(0.0),

    .CLKOUT4_DIVIDE(1),
    .CLKOUT4_DUTY_CYCLE(0.5),
    .CLKOUT4_PHASE(0.0),

    .CLKOUT5_DIVIDE(1),
    .CLKOUT5_DUTY_CYCLE(0.5),
    .CLKOUT5_PHASE(0.0)
) PLLE2_BASE_inst (
    .PWRDWN(1'b0),
    .RST(pll_rst),      
    .LOCKED(pll_locked),
    .CLKFBIN(pll_clkfb),    //Feedback clock
    .CLKFBOUT(pll_clkfb),   //Feedback clock
    .CLKIN1(clk),    
    .CLKOUT0(ddr_clk),
    .CLKOUT1(),
    .CLKOUT2(),
    .CLKOUT3(),
    .CLKOUT4(),
    .CLKOUT5()
); 

//dac_sel: 0--> interleave mode, just one line
//dac_sel: 1--> dual port mode: data input line at the same freq, but 2 lines
reg [DATA_WIDTH-1:0] reg_dac0=0, reg_dac1=0;
always@(posedge clk)begin
    if(ce & pll_locked)begin
        reg_dac0 <= dac0; reg_dac1 <= dac1;
    end
    else begin 
        reg_dac0 <= {(DATA_WIDTH){1'b0}};
        reg_dac1 <= {(DATA_WIDTH){1'b0}};
    end 
end





ODDR ODDR_rst(.Q(dac_rst), .D1(ce), .D2(ce), .C(clk), .CE(1'b1), .R(1'b0), .S(1'b0));
ODDR ODDR_sel(.Q(dac_sel), .D1(1'b0), .D2(1'b1), .C(clk), .CE(1'b1), .R(1'b0), .S(1'b0));
ODDR ODDR_wrt(.Q(dac_wrt), .D1(1'b0), .D2(1'b1), .C(ddr_clk), .CE(1'b1), .R(1'b0), .S(1'b0));
ODDR ODDR_clk(.Q(dac_clk), .D1(1'b0), .D2(1'b1), .C(ddr_clk), .CE(1'b1), .R(1'b0), .S(1'b0));


ODDR ODDR_inst [DATA_WIDTH-1:0] (
        .Q(dac_dat),
        .D1(reg_dac0),
        .D2(reg_dac1),
        .C(clk),
        .CE(1'b1),
        .R(1'b0),
        .S(1'b0)
      );

endmodule
