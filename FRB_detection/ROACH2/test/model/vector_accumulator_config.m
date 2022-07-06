
function vector_accumulator_config(this_block)

  % Revision History:
  %
  %   18-Mar-2022  (08:16 hours):
  %     Original code was machine generated by Xilinx's System Generator after parsing
  %     /home/roach/Workspace/simulink_models/FRB_Detection/ROACH2/preliminar/v3/model/rtl/vector_accumulator.v
  %
  %

  this_block.setTopLevelLanguage('Verilog');

  this_block.setEntityName('vector_accumulator');

  %get the parameter of the top subsystem
  myname = this_block.blockName; %This is the name of the black box block
  bb_mask = get_param(myname,'Parent'); %This is the name of the black box subsystem
  din_width = str2num(get_param(bb_mask, 'din_width'));
  vec_len = str2num(get_param(bb_mask, 'vec_len'));
  dout_width = str2num(get_param(bb_mask, 'dout_width'));
  
  % System Generator has to assume that your entity  has a combinational feed through; 
  %   if it  doesn't, then comment out the following line:
  %this_block.tagAsCombinational;

  this_block.addSimulinkInport('new_acc');
  this_block.addSimulinkInport('din');
  this_block.addSimulinkInport('din_valid');

  this_block.addSimulinkOutport('dout');
  this_block.addSimulinkOutport('dout_valid');

  dout_port = this_block.port('dout');
  dout_port.setType(strcat('UFix_',num2str(dout_width),'_0'));
  
  dout_valid_port = this_block.port('dout_valid');
  dout_valid_port.setType('UFix_1_0');
  dout_valid_port.useHDLVector(false);

  % -----------------------------
  if (this_block.inputTypesKnown)
    % do input type checking, dynamic output type and generic setup in this code block.

    if (this_block.port('new_acc').width ~= 1);
      this_block.setError('Input data type for port "new_acc" must have width=1.');
    end

    this_block.port('new_acc').useHDLVector(false);

    % (!) Port 'din' appeared to have dynamic type in the HDL -- please add type checking as appropriate;

    if (this_block.port('din_valid').width ~= 1);
      this_block.setError('Input data type for port "din_valid" must have width=1.');
    end

    this_block.port('din_valid').useHDLVector(false);

  % (!) Port 'dout' appeared to have dynamic type in the HDL
  % --- you must add an appropriate type setting for this port
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
  % Grab HDL parameters from simulink mask
  
  
  
  this_block.addGeneric('DIN_WIDTH','integer',num2str(din_width));
  this_block.addGeneric('VECTOR_LEN','integer',num2str(vec_len));
  this_block.addGeneric('DOUT_WIDTH','integer',num2str(dout_width));
  this_block.addGeneric('DATA_TYPE','string','"unsigned"');

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
  this_block.addFile('includes.v');
  %this_block.addFile('rtl/vector_accumulator.v');

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

