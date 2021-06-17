
function piso_config(this_block)

  % Revision History:
  %
  %   26-Mar-2021  (11:41 hours):
  %     Original code was machine generated by Xilinx's System Generator after parsing
  %     /home/franco/seba/tge_test/piso.v
  %
  %

  this_block.setTopLevelLanguage('Verilog');

  this_block.setEntityName('piso');

  % System Generator has to assume that your entity  has a combinational feed through; 
  %   if it  doesn't, then comment out the following line:
  %this_block.tagAsCombinational;

  this_block.addSimulinkInport('rst');
  this_block.addSimulinkInport('din');
  this_block.addSimulinkInport('din_valid');
  this_block.addSimulinkInport('dout_ready');

  this_block.addSimulinkOutport('dout');
  this_block.addSimulinkOutport('dout_valid');
  this_block.addSimulinkOutport('out_full');
  this_block.addSimulinkOutport('out_empty');

  dout_port = this_block.port('dout');
  dout_port.setType('UFix_64_0');
  dout_valid_port = this_block.port('dout_valid');
  dout_valid_port.setType('UFix_1_0');
  dout_valid_port.useHDLVector(false);
  out_full_port = this_block.port('out_full');
  out_full_port.setType('UFix_1_0');
  out_full_port.useHDLVector(false);
  out_empty_port = this_block.port('out_empty');
  out_empty_port.setType('UFix_1_0');
  out_empty_port.useHDLVector(false);

  % -----------------------------
  if (this_block.inputTypesKnown)
    % do input type checking, dynamic output type and generic setup in this code block.

    if (this_block.port('rst').width ~= 1);
      this_block.setError('Input data type for port "rst" must have width=1.');
    end

    this_block.port('rst').useHDLVector(false);

    if (this_block.port('din').width ~= 256);
      this_block.setError('Input data type for port "din" must have width=256.');
    end

    if (this_block.port('din_valid').width ~= 1);
      this_block.setError('Input data type for port "din_valid" must have width=1.');
    end

    this_block.port('din_valid').useHDLVector(false);

    if (this_block.port('dout_ready').width ~= 1);
      this_block.setError('Input data type for port "dout_ready" must have width=1.');
    end

    this_block.port('dout_ready').useHDLVector(false);

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
  this_block.addGeneric('DIN_WIDTH','integer','256');
  this_block.addGeneric('DOUT_WIDTH','integer','64');
  this_block.addGeneric('FIFO_DEPTH','integer','1024');

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

  dir = '/home/seba/Workspace/simulink_models/FRB_Detection/ROACH2/work_in_progress/doa/hdl_codes/';  
  this_block.addFile(strcat(dir,'bram_infer_piso.v'));
  this_block.addFile(strcat(dir,'piso.v'));


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

