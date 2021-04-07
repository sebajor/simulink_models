In the hdl_codes there is a Automatic Gain Control module that works in the time
domain. The module allows simultaneous inputs and has a parametrizable widths.

The algoithm works as follows:
1) Calculate the square of the input data.
2) Calculate average values using a moving average module of window size equals to 
   the parameter DELAY_LINE
3) Multiply the average power by a weight coeficient.
4) Calculate the difference between the weighted power with a reference. 
   This is going to be our error.
5) Multiply the error by the error coef (this is our learning rate).
6) Adjust the weight setting weight_new = weight_old+error_coef*error.
   This step only occurs when 2 condtions are met:
    i)  We use a counter wich count until is equal to the parameter UPDATE_CYCLES
    ii) The weigh_new is lower than the GAIN_HIGH and higher than GAIN_LOW.
   If one of those conditions is false, then weight_new = weight_old

7) Multiply the input data by the weight_new.


