
function piso_config(this_block)

  % Revision History:
  %
  %   14-Jan-2021  (16:50 hours):
  %     Original code was machine generated by Xilinx's System Generator after parsing
  %     /home/seba/Workspace/simulink_models/Ten_Gbe/spec_tge_4in_gps/piso_tge.v
  %
  %

  this_block.setTopLevelLanguage('Verilog');

  this_block.setEntityName('piso');

  % System Generator has to assume that your entity  has a combinational feed through; 
  %   if it  doesn't, then comment out the following line:
  this_block.tagAsCombinational;

  this_block.addSimulinkInport('rst');
  this_block.addSimulinkInport('i_parallel');
  this_block.addSimulinkInport('fifo_empty');

  this_block.addSimulinkOutport('o_serial');
  this_block.addSimulinkOutport('fifo_re');
  this_block.addSimulinkOutport('valid');

  o_serial_port = this_block.port('o_serial');
  o_serial_port.setType('UFix_64_0');
  fifo_re_port = this_block.port('fifo_re');
  fifo_re_port.setType('UFix_1_0');
  fifo_re_port.useHDLVector(false);
  valid_port = this_block.port('valid');
  valid_port.setType('UFix_1_0');
  valid_port.useHDLVector(false);

  % -----------------------------
  if (this_block.inputTypesKnown)
    % do input type checking, dynamic output type and generic setup in this code block.

    if (this_block.port('rst').width ~= 1);
      this_block.setError('Input data type for port "rst" must have width=1.');
    end

    this_block.port('rst').useHDLVector(false);

    if (this_block.port('i_parallel').width ~= 256);
      this_block.setError('Input data type for port "i_parallel" must have width=512.');
    end

    if (this_block.port('fifo_empty').width ~= 1);
      this_block.setError('Input data type for port "fifo_empty" must have width=1.');
    end

    this_block.port('fifo_empty').useHDLVector(false);

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
  this_block.addGeneric('INPUT_SIZE','integer','256');
  this_block.addGeneric('OUTPUT_SIZE','integer','64');

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
  this_block.addFile('piso_tge.v');

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

