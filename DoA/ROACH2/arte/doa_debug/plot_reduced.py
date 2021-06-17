import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import calandigital 


def reduced_plot(_fpga, freq=(0, 600),yim=(-80, 5)):
    global fpga, lines, frequencies
    frequecies = np.linspace(freq[0], freq[1], 2048, endpoint=False)
    brams = [['red0_0', 'red0_1', 'red0_2', 'red0_3'],
             ['red1_0', 'red1_1', 'red1_2', 'red1_3']
    
    
