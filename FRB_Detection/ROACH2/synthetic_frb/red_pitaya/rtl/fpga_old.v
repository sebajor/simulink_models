module fpga 
(  
    //typical zynq signals 
    inout wire [14:0]DDR_addr,
    inout wire[2:0]DDR_ba,
    inout wire DDR_cas_n,
    inout wire DDR_ck_n,
    inout wire DDR_ck_p,
    inout wire DDR_cke,
    inout wire DDR_cs_n,
    inout wire [3:0]DDR_dm,
    inout wire [31:0]DDR_dq,
    inout wire [3:0]DDR_dqs_n,
    inout wire [3:0]DDR_dqs_p,
    inout wire DDR_odt,
    inout wire DDR_ras_n,
    inout wire DDR_reset_n,
    inout wire DDR_we_n,
    inout wire FIXED_IO_ddr_vrn,
    inout wire FIXED_IO_ddr_vrp,
    inout wire [53:0]FIXED_IO_mio,
    inout wire FIXED_IO_ps_clk,
    inout wire FIXED_IO_ps_porb,
    inout wire FIXED_IO_ps_srstb,
     
    //leds
    output wire [7:0] led_o,
    //dac
    output wire dac_clk_o,    //iqclk --> clka/qclk
    output wire dac_rst_o,    //iqrst --> clkb/iqrst
    output wire dac_sel_o,    //iqsel --> wrtb/iqsel
    output wire dac_wrt_o,    //iqwrt --> wrta/iqwrt
    output wire [13:0] dac_dat_o

);

wire [31:0]M00_AXI_0_araddr;
wire [2:0]M00_AXI_0_arprot;
wire [0:0]M00_AXI_0_arready;
wire [0:0]M00_AXI_0_arvalid;
wire [31:0]M00_AXI_0_awaddr;
wire [2:0]M00_AXI_0_awprot;
wire [0:0]M00_AXI_0_awready;
wire [0:0]M00_AXI_0_awvalid;
wire [0:0]M00_AXI_0_bready;
wire [1:0]M00_AXI_0_bresp;
wire [0:0]M00_AXI_0_bvalid;
wire [31:0]M00_AXI_0_rdata;
wire [0:0]M00_AXI_0_rready;
wire [1:0]M00_AXI_0_rresp;
wire [0:0]M00_AXI_0_rvalid;
wire [31:0]M00_AXI_0_wdata;
wire [0:0]M00_AXI_0_wready;
wire [3:0]M00_AXI_0_wstrb;
wire [0:0]M00_AXI_0_wvalid;

wire [31:0] BRAM_PORTB_0_addr;        //input
//wire  BRAM_PORTB_0_clk;       //input 
wire [31:0] BRAM_PORTB_0_din;   //input
wire [31:0] BRAM_PORTB_0_dout;  //output
wire BRAM_PORTB_0_en;           //input
wire BRAM_PORTB_0_rst;          //input
wire BRAM_PORTB_0_we;           //input 

//clock wires
wire adc_clk_out;
wire axi_clock;

system_wrapper system_wrapper_inst(
    .DDR_addr(DDR_addr),
    .DDR_ba(DDR_ba),
    .DDR_cas_n(DDR_cas_n),
    .DDR_ck_n(DDR_ck_n),
    .DDR_ck_p(DDR_ck_p),
    .DDR_cke(DDR_cke),
    .DDR_cs_n(DDR_cs_n),
    .DDR_dm(DDR_dm),
    .DDR_dq(DDR_dq),
    .DDR_dqs_n(DDR_dqs_n),
    .DDR_dqs_p(DDR_dqs_p),
    .DDR_odt(DDR_odt),
    .DDR_ras_n(DDR_ras_n),
    .DDR_reset_n(DDR_reset_n),
    .DDR_we_n(DDR_we_n),
    .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
    .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
    .FIXED_IO_mio(FIXED_IO_mio),
    .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
    .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
    .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
    .BRAM_PORTB_0_addr(BRAM_PORTB_0_addr),
    .BRAM_PORTB_0_clk(axi_clock),
    .BRAM_PORTB_0_din(),
    .BRAM_PORTB_0_dout(BRAM_PORTB_0_dout),
    .BRAM_PORTB_0_en(1'b1),
    .BRAM_PORTB_0_rst(1'b0),
    .BRAM_PORTB_0_we(1'b0),
    .M00_AXI_0_araddr(M00_AXI_0_araddr),
    .M00_AXI_0_arprot(M00_AXI_0_arprot),
    .M00_AXI_0_arready(M00_AXI_0_arready),
    .M00_AXI_0_arvalid(M00_AXI_0_arvalid),
    .M00_AXI_0_awaddr(M00_AXI_0_awaddr),
    .M00_AXI_0_awprot(M00_AXI_0_awprot),
    .M00_AXI_0_awready(M00_AXI_0_awready),
    .M00_AXI_0_awvalid(M00_AXI_0_awvalid),
    .M00_AXI_0_bready(M00_AXI_0_bready),
    .M00_AXI_0_bresp(M00_AXI_0_bresp),
    .M00_AXI_0_bvalid(M00_AXI_0_bvalid),
    .M00_AXI_0_rdata(M00_AXI_0_rdata),
    .M00_AXI_0_rready(M00_AXI_0_rready),
    .M00_AXI_0_rresp(M00_AXI_0_rresp),
    .M00_AXI_0_rvalid(M00_AXI_0_rvalid),
    .M00_AXI_0_wdata(M00_AXI_0_wdata),
    .M00_AXI_0_wready(M00_AXI_0_wready),
    .M00_AXI_0_wstrb(M00_AXI_0_wstrb),
    .M00_AXI_0_wvalid(M00_AXI_0_wvalid),
    .axi_clock(axi_clock)
);


//wire [5:0] shift;
wire [31:0] bram_addr;
wire addr_valid, finish;
wire [31:0] default_val;

 
axil_reg_template #(
    .BRAM_ADDR(11),    //check!
    .C_S_AXI_DATA_WIDTH(32),
    .C_S_AXI_ADDR_WIDTH(5)
) axil_reg_inst (
    .bram_addr(bram_addr),   //31:0 //check!
    .addr_valid(addr_valid),
    .finish(finish),
    .default_val(default_val), //15:0
    //.shift(shift),   //5:0
    .S_AXI_ACLK(axi_clock),
    .S_AXI_ARESETN(1'b1),
    .S_AXI_AWADDR(M00_AXI_0_awaddr),
    .S_AXI_AWPROT(M00_AXI_0_awprot),
    .S_AXI_AWVALID(M00_AXI_0_awvalid),
    .S_AXI_AWREADY(M00_AXI_0_awready),
    .S_AXI_WDATA(M00_AXI_0_wdata),
    .S_AXI_WSTRB(M00_AXI_0_wstrb),
    .S_AXI_WVALID(M00_AXI_0_wvalid),
    .S_AXI_WREADY(M00_AXI_0_wready),
    .S_AXI_BRESP(M00_AXI_0_bresp),
    .S_AXI_BVALID(M00_AXI_0_bvalid),
    .S_AXI_BREADY(M00_AXI_0_bready),
    .S_AXI_ARADDR(M00_AXI_0_araddr),
    .S_AXI_ARPROT(M00_AXI_0_arprot),
    .S_AXI_ARVALID(M00_AXI_0_arvalid),
    .S_AXI_ARREADY(M00_AXI_0_arready),
    .S_AXI_RDATA(M00_AXI_0_rdata),
    .S_AXI_RRESP(M00_AXI_0_rresp),
    .S_AXI_RVALID(M00_AXI_0_rvalid),
    .S_AXI_RREADY(M00_AXI_0_rready)
);

assign BRAM_PORTB_0_addr = bram_addr<<2;
assign BRAM_PORTB_0_en = addr_valid;
reg [31:0] dac_val=0;

always@(posedge axi_clock)begin
    if(finish)
        dac_val <= default_val;
    else begin
        if(addr_valid)
            dac_val <= BRAM_PORTB_0_dout;
        else
            dac_val <= dac_val;
    end
end



//dac
dac_rp #(
    .DATA_WIDTH(14)
) dac_rp_inst (
    .clk(axi_clock),
    .dac0(dac_val[13:0]),
    .dac1(dac_val[31:16]),    
    .ce(1'b1),
    .dac_clk(dac_clk_o),
    .dac_rst(dac_rst_o),
    .dac_sel(dac_sel_o),
    .dac_wrt(dac_wrt_o),
    .dac_dat(dac_dat_o)
);

assign led_o[0] = finish;
assign led_o[7:1] = dac_val[6:0];



endmodule 
