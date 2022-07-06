
function fft_chann_flag_top_config(this_block)

  % Revision History:
  %
  %   02-Aug-2021  (15:01 hours):
  %     Original code was machine generated by Xilinx's System Generator after parsing
  %     /home/seba/Workspace/simulink_models/FRB_Detection/ROACH2/preliminar/v2/hdl_codes/fft_channel_flag_top.v
  %
  %

  this_block.setTopLevelLanguage('Verilog');

  this_block.setEntityName('fft_chann_flag_top');

  % System Generator has to assume that your entity  has a combinational feed through; 
  %   if it  doesn't, then comment out the following line:
  this_block.tagAsCombinational;

  this_block.addSimulinkInport('sync_in');
  this_block.addSimulinkInport('din');
  this_block.addSimulinkInport('config_flag');
  this_block.addSimulinkInport('config_num');
  this_block.addSimulinkInport('config_en');

  this_block.addSimulinkOutport('sync_out');
  this_block.addSimulinkOutport('dout');

  sync_out_port = this_block.port('sync_out');
  sync_out_port.setType('UFix_1_0');
  sync_out_port.useHDLVector(false);
  dout_port = this_block.port('dout');
  dout_port.setType('UFix_144_0');

  % -----------------------------
  if (this_block.inputTypesKnown)
    % do input type checking, dynamic output type and generic setup in this code block.

    if (this_block.port('sync_in').width ~= 1);
      this_block.setError('Input data type for port "sync_in" must have width=1.');
    end

    this_block.port('sync_in').useHDLVector(false);

    if (this_block.port('din').width ~= 144);
      this_block.setError('Input data type for port "din" must have width=144.');
    end

    if (this_block.port('config_flag').width ~= 32);
      this_block.setError('Input data type for port "config_flag" must have width=32.');
    end

    if (this_block.port('config_num').width ~= 32);
      this_block.setError('Input data type for port "config_num" must have width=32.');
    end

    if (this_block.port('config_en').width ~= 1);
      this_block.setError('Input data type for port "config_en" must have width=1.');
    end

    this_block.port('config_en').useHDLVector(false);

  end  % if(inputTypesKnown)
  % -----------------------------

  % -----------------------------
   if (this_block.inputRatesKnown)
     setup_as_single_rate(this_block,'clk','ce')
   end  % if(inputRatesKnown)
  % -----------------------------

    % (!) Set the inout port rate to be the same as the first input 
    %     rate. Change the following code if this is untrue.
    uniqueInputRates = unique(this_block.getInputRates);


  % Add addtional source files as needed.
  %  |-------------
  %  | Add files in the order in which they should be compiled.
  %  | If two files "a.vhd" and "b.vhd" contain the entities
  %  | entity_a and entity_b, and entity_a contains a
  %  | component of type entity_b, the correct sequence of
  %  | addFile() calls would be:
  %  |    this_block.addFile('b.vhd');
  %  |    this_block.addFile('a.vhd');
  %  |-------------

  %    this_block.addFile('');
  %    this_block.addFile('');
  %this_block.addFile('rtl/fft_chann_flag.v');
  this_block.addFile('includes.v');
  this_block.addFile('rtl/fft_channel_flag_top.v');
  
return;


% ------------------------------------------------------------

function setup_as_single_rate(block,clkname,cename) 
  inputRates = block.inputRates; 
  uniqueInputRates = unique(inputRates); 
  if (length(uniqueInputRates)==1 & uniqueInputRates(1)==Inf) 
    block.addError('The inputs to this block cannot all be constant.'); 
    return; 
  end 
  if (uniqueInputRates(end) == Inf) 
     hasConstantInput = true; 
     uniqueInputRates = uniqueInputRates(1:end-1); 
  end 
  if (length(uniqueInputRates) ~= 1) 
    block.addError('The inputs to this block must run at a single rate.'); 
    return; 
  end 
  theInputRate = uniqueInputRates(1); 
  for i = 1:block.numSimulinkOutports 
     block.outport(i).setRate(theInputRate); 
  end 
  block.addClkCEPair(clkname,cename,theInputRate); 
  return; 

% ------------------------------------------------------------

