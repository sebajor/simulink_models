
function dedisp_top_config(this_block)

  % Revision History:
  %
  %   12-Mar-2021  (22:40 hours):
  %     Original code was machine generated by Xilinx's System Generator after parsing
  %     /home/franco/seba/frb_beam/v2/dedisp_top.v
  %
  %

  this_block.setTopLevelLanguage('Verilog');

  this_block.setEntityName('dedisp_top');

  % System Generator has to assume that your entity  has a combinational feed through; 
  %   if it  doesn't, then comment out the following line:
  %this_block.tagAsCombinational;

  this_block.addSimulinkInport('rst');
  this_block.addSimulinkInport('din');
  this_block.addSimulinkInport('din_valid');

  this_block.addSimulinkOutport('dout');
  this_block.addSimulinkOutport('dout_valid');
  this_block.addSimulinkOutport('dout_sof');
  this_block.addSimulinkOutport('dout_eof');
  this_block.addSimulinkOutport('integ_pow');
  this_block.addSimulinkOutport('integ_valid');

  dout_port = this_block.port('dout');
  dout_port.setType('UFix_26_0');
  dout_valid_port = this_block.port('dout_valid');
  dout_valid_port.setType('UFix_1_0');
  dout_valid_port.useHDLVector(false);
  dout_sof_port = this_block.port('dout_sof');
  dout_sof_port.setType('UFix_1_0');
  dout_sof_port.useHDLVector(false);
  dout_eof_port = this_block.port('dout_eof');
  dout_eof_port.setType('UFix_1_0');
  dout_eof_port.useHDLVector(false);
  integ_pow_port = this_block.port('integ_pow');
  integ_pow_port.setType('UFix_32_0');
  integ_valid_port = this_block.port('integ_valid');
  integ_valid_port.setType('UFix_1_0');
  integ_valid_port.useHDLVector(false);

  % -----------------------------
  if (this_block.inputTypesKnown)
    % do input type checking, dynamic output type and generic setup in this code block.

    if (this_block.port('rst').width ~= 1);
      this_block.setError('Input data type for port "rst" must have width=1.');
    end

    this_block.port('rst').useHDLVector(false);

    if (this_block.port('din').width ~= 26);
      this_block.setError('Input data type for port "din" must have width=26.');
    end

    if (this_block.port('din_valid').width ~= 1);
      this_block.setError('Input data type for port "din_valid" must have width=1.');
    end

    this_block.port('din_valid').useHDLVector(false);

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

  % (!) Custimize the following generic settings as appropriate. If any settings depend
  %      on input types, make the settings in the "inputTypesKnown" code block.
  %      The addGeneric function takes  3 parameters, generic name, type and constant value.
  %      Supported types are boolean, real, integer and string.
  this_block.addGeneric('N_CHANNELS','integer','64');
  this_block.addGeneric('DIN_WIDTH','integer','26');
  %this_block.addGeneric('DELAY_ARRAY','','');

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
  dir = '/home/seba/Workspace/simulink_models/FRB_Detection/ROACH2/stable/hdl_codes/';  
  this_block.addFile(strcat(dir,'bram_infer.v'));
  this_block.addFile(strcat(dir,'dedispersor_block.v'));
  this_block.addFile(strcat(dir,'dedispersor.v'));
  this_block.addFile(strcat(dir,'dedisp_top.v'));
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

