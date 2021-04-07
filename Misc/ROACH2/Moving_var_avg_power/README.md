The codes in the folder hdl_codes have a module that calculates moving average and
moving variance of a signal. 
So you have a window of parametrizable size where you calculate the avg and var,
when one sample enters to that window the oldest one is dropped of the math.


If you want to use it in a model take a look on the range of values that your
signal has (ie study the bit range that your signal has, and set the parameters
of the moving avg/var accordingly)
