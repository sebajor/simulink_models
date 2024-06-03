import numpy as np
import matplotlib.pyplot as plt
import calandigital as calan
from calandigital.instruments.visa_generator import visa_generator
import time, os, sys, casperfpga
import ipdb
import logging
from parameters import test_parameters


def read_crosscorrelation_brams(fpga, bram_list, awidth, dwidth, dtype='>i8'):
    corrdata = calan.read_interleave_data(fpga, bram_list,awidth+1, dwidth, dtype)
    corrdata = corrdata.reshape((-1,len(bram_list)))
    corrdata = (corrdata[::2,:]+1j*corrdata[1::2,:]).flatten()
    corrdata = np.hstack((corrdata[len(corrdata)//2:], corrdata[:len(corrdata)//2]))
    return corrdata


def read_autocorrelation_brams(fpga, bram_list, awidth, dwidth, dtype='>u8'):
    autodata = calan.read_interleave_data(fpga, bram_list,awidth, dwidth, dtype)
    autodata = np.hstack((autodata[len(autodata)//2:], autodata[:len(autodata)//2]))
    return autodata


def load_constants(fpga, constants, bitwidth,bit_pt, bram,canonical=False):
    """
    fpga:           CasperFpga object
    constants:      Constants to upload
    canonical:      If the data is in canonical order
    """
    if(not canonical):
        len_const = len(constants)
        constants = np.hstack((constants[len_const//2:], constants[:len_const//2]))
    const_real = calan.float2fixed(constants.real, bitwidth, bit_pt)
    const_imag = calan.float2fixed(constants.imag, bitwidth, bit_pt)
    re_brams = [x+str('_bram_re') for x in bram]
    im_brams = [x+str('_bram_im') for x in bram]
    calan.write_interleaved_data(fpga, re_brams, const_real)
    calan.write_interleaved_data(fpga, im_brams, const_imag)


def get_calibration_data(fpga, generator,test_parameters, sideband, dss, 
                         plot=None):
    """
    fpga:       casperfpga object
    generator:  RF generator
    rf_freq:    list with the test frequencies in mhz
    test_chnls: channels in the IF where the RF is mapped
    sideband:   either usb or lsb.
    dss:        either dss01 or dss23
    plot:       an object that contains fig, lines. if None skip the ploting
    """
    if(plot is not None):
        fig, lines = plot
    ##create folders if they dont exists
    if(test_parameters['debug_folder'] is not None):
        os.makedirs(test_parameters['debug_folder'], exist_ok=True)
        os.makedirs(os.path.join(test_parameters['debug_folder'],'usb'), exist_ok=True)
        os.makedirs(os.path.join(test_parameters['debug_folder'],'lsb'), exist_ok=True)

    rf_freq = test_parameters[dss]['rf_freqs'][sideband]
    test_channels = test_parameters['test_channels']
    aa=np.zeros(len(test_channels))
    bb=np.zeros(len(test_channels))
    ab=np.zeros(len(test_channels), dtype=complex)
    #generator.set_power_dbm(test_parameters[dss]['rf_power'])
    generator.set_freq_ghz(rf_freq[test_channels[0]])
    generator.turn_output_on()
    for i,ch  in enumerate(test_channels):
        rf = rf_freq[ch]
        generator.set_freq_ghz(rf)
        time.sleep(test_parameters['sleeping'])
        a2 = read_autocorrelation_brams(fpga=fpga,
                bram_list=test_parameters[dss]['aa_brams'],
                awidth=test_parameters['bram_addr_width'],
                dwidth=test_parameters['bram_data_width'],
                dtype=test_parameters['pow_dtype'])
        b2 = read_autocorrelation_brams(fpga=fpga,
                bram_list=test_parameters[dss]['bb_brams'],
                awidth=test_parameters['bram_addr_width'],
                dwidth=test_parameters['bram_data_width'],
                dtype=test_parameters['pow_dtype'])
        cross = read_crosscorrelation_brams(fpga=fpga,
                bram_list=test_parameters[dss]['ab_brams'],
                awidth=test_parameters['bram_addr_width'],
                dwidth=test_parameters['bram_data_width'],
                dtype=test_parameters['cross_dtype'])
        aa[i] = a2[ch]
        bb[i] = b2[ch]
        ab[i] = cross[ch]

        #save data
        if(test_parameters['debug_folder'] is not None):
            np.savez(os.path.join(test_parameters['debug_folder'], sideband, 'chnl_'+str(ch)),
                     aa = a2, bb=b2, ab=cross)
        if(plot is not None):
            #dont like this plot too much..
            a2_scale = calan.scale_and_dBFS_specdata(a2, test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            b2_scale = calan.scale_and_dBFS_specdata(b2, test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            aa_plot = calan.scale_and_dBFS_specdata(aa[:i], test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            bb_plot = calan.scale_and_dBFS_specdata(bb[:i], test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            calibration_plot_update(a2_scale, b2_scale, cross, aa_plot, bb_plot,
                                    ab[:i], test_parameters['if_freqs'], test_parameters['if_test_freqs'][:i],
                                    plot['fig'], plot['lines'])
    #interpolate the measured data
    aa_out = np.interp(test_parameters['if_freqs'], test_parameters['if_test_freqs'], aa)
    bb_out = np.interp(test_parameters['if_freqs'], test_parameters['if_test_freqs'], bb)
    ab_out = np.interp(test_parameters['if_freqs'], test_parameters['if_test_freqs'], ab)
    return aa_out, bb_out, ab_out


def create_debug_figure(bandwidth):
    fig, axes = plt.subplots(2,3)
    fig.set_tight_layout(True)
    fig.show()
    fig.canvas.draw()
    lines = []
    for i,ax in enumerate(axes.flatten()):
        line, = ax.plot([],[])
        lines.append(line)
        ax.grid()
        ax.set_xlabel('MHz')
        ax.set_xlim((0,bandwidth))
        if((i==2) or (i==5)):
            ax.set_ylim((-180,180))
            ax.set_ylabel('Phase deg')
        else:
            ax.set_ylim((-120,0))
            ax.set_ylabel('Power dBFS')
    plot = {}
    plot['fig'] = fig; plot['lines'] = lines
    return plot

        

def calibration_plot_update(a2_scale, b2_scale,cross, aa, bb,ab,if_freqs,if_test_freqs,
                            fig, lines):
    """
    """
    lines[0].set_data(if_freqs,a2_scale)
    lines[1].set_data(if_freqs,b2_scale)
        
    lines[3].set_data(if_test_freqs, aa)
    lines[4].set_data(if_test_freqs, bb)
    if(cross is not None):
        lines[2].set_data(if_freqs,np.angle(cross, deg=True))
        lines[5].set_data(if_test_freqs, np.angle(ab, deg=True))
    fig.canvas.draw()
    fig.canvas.flush_events()
    


    
def make_dss_calibration(fpga, test_parameters, dss, logger, plot=True, inverted=False):
    """
    fpga:               CasperFpga object
    test_parameters:    parameters of the measurement
    dss:                dss01, dss23
    inverted:           If True the LO is the one that sweeps
    """
    lo_gen, rf_gen = setup_generators(test_parameters, dss, logger, inverted=inverted)
    logger.info("Start tone sweeping in upper sideband")
    if(plot):
        plot = create_debug_figure(test_parameters['bandwidth'])
    else:
        plot = None

    if(inverted):
        aa_usb, bb_usb, ab_usb = get_calibration_data(fpga, lo_gen,
                test_parameters, 'usb', dss, plot=plot)
        
        time.sleep(0.3)
        logger.info("Start tone sweeping in lower sideband")
        aa_lsb, bb_lsb, ab_lsb = get_calibration_data(fpga, lo_gen,
                test_parameters, 'lsb', dss, plot=plot)
    
    else:
        aa_usb, bb_usb, ab_usb = get_calibration_data(fpga, rf_gen,
                test_parameters, 'usb', dss, plot=plot)
        
        time.sleep(0.3)
        logger.info("Start tone sweeping in lower sideband")
        aa_lsb, bb_lsb, ab_lsb = get_calibration_data(fpga, rf_gen,
                test_parameters, 'lsb', dss, plot=plot)
    
    rf_gen.turn_output_off()
    lo_gen.turn_output_off()

    rf_gen.instr.close()
    lo_gen.instr.close()
    
    if(test_parameters['debug_folder'] is not None):
        if(inverted):
            np.savez(os.path.join(test_parameters['debug_folder'], 'dds_calibration_inverted.npz'),
                     aa_lsb = aa_lsb, bb_lsb=bb_lsb, ab_lsb=ab_lsb,
                     aa_usb = aa_usb, bb_usb=bb_usb, ab_usb=ab_usb)
        else:
        np.savez(os.path.join(test_parameters['debug_folder'], 'dds_calibration.npz'),
                 aa_lsb = aa_lsb, bb_lsb=bb_lsb, ab_lsb=ab_lsb,
                 aa_usb = aa_usb, bb_usb=bb_usb, ab_usb=ab_usb)
    return aa_lsb, bb_lsb, ab_lsb, aa_usb, bb_usb, ab_usb, plot


def setup_generators(test_parameters,dss, logger):
    #connect to the instruments
    lo_gen = visa_generator(test_parameters[dss]['lo']['genname'])
    rf_gen = visa_generator(test_parameters[dss]['rf']['genname'])

    lo_gen.set_freq_ghz(test_parameters[dss]['lo']['freq'])
    lo_gen.set_power_dbm(test_parameters[dss]['lo']['power'])
    lo_power = lo_gen.get_power_dbm()[0]
    lo_freq = lo_gen.get_freq()[0]/1e9
    logger.debug("LO freq:{:.3f} GHz, LO power:{:.3f}".format(lo_freq, lo_power))
    lo_gen.turn_output_on()
    lo_status = lo_gen.get_output_status()[0]
    if(not lo_status):
        logger.error('LO generator did not turn on!')
    rf_gen.set_power_dbm(test_parameters[dss]['rf']['power'])
    rf_power = rf_gen.get_power_dbm()[0]
    logger.debug("RF power {:.3f}".format(rf_power))
    ##we set the rf at the lo freq in case we sweep with the lo
    rf_gen.set_freq_ghz(test_parameters[dss]['lo']['freq'])
    return lo_gen, rf_gen
    



def srr_measurement(fpga, test_parameters, constants,dss,logger, plot=None, inverted=False):
    """
    constants: [lsb_constants, usb_constants]
    """
    if(test_parameters['debug_folder'] is not None):
        os.makedirs(test_parameters['debug_folder'], exist_ok=True)
        folder_path = os.path.join(test_parameters['debug_folder'], 'srr')
        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(folder_path, 'lsb'), exist_ok=True)
        os.makedirs(os.path.join(folder_path, 'usb'), exist_ok=True)

    ###now the calibrated signals will be
    ## cal0 = usb_data = fft0+const_usb*fft1
    ## cal1 = lsb_data = fft1+const_lsb*fft0


    logger.info("Uploading usb constants")
    load_constants(fpga, constants[1], test_parameters['const_nbits'], 
            test_parameters['const_binpt'], test_parameters[dss]['cal0'])
    logger.info("Uploading lsb constants")
    load_constants(fpga, constants[0], test_parameters['const_nbits'], 
            test_parameters['const_binpt'], test_parameters[dss]['cal1'])
    lo_gen, rf_gen = setup_generators(test_parameters, dss, logger)
    if(inverted):
        lo_gen, rf_gen = rf_gen, lo_gen
    
    logger.info("Start lsb sweeping")
    test_channels = test_parameters['test_channels']
    

    rf_freq = test_parameters[dss]['rf_freqs']['lsb']
    lsbtone_lsb = np.zeros(len(test_channels))
    lsbtone_usb = np.zeros(len(test_channels))

    rf_gen.set_freq_ghz(rf_freq[test_channels[0]])
    rf_gen.turn_output_on()
    for i,ch  in enumerate(test_channels):
        rf = rf_freq[ch]
        rf_gen.set_freq_ghz(rf)
        time.sleep(test_parameters['sleeping'])
        usb = read_autocorrelation_brams(fpga, test_parameters[dss]['synth0'],
            test_parameters['bram_addr_width'],
            test_parameters['bram_data_width'],
            test_parameters['pow_dtype'])
        lsb = read_autocorrelation_brams(fpga, test_parameters[dss]['synth1'],
            test_parameters['bram_addr_width'],
            test_parameters['bram_data_width'],
            test_parameters['pow_dtype'])
        lsbtone_lsb[i] = lsb[ch]
        lsbtone_usb[i] = usb[ch]
        
        if(test_parameters['debug_folder'] is not None):
            np.savez( os.path.join(folder_path,'lsb', 'chnl_'+str(ch)),
                     lsb=lsb, usb=usb)

        if(plot is not None):
            lsb_scale = calan.scale_and_dBFS_specdata(lsb, test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            usb_scale = calan.scale_and_dBFS_specdata(usb, test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            lsb_plot = calan.scale_and_dBFS_specdata(lsbtone_lsb[:i], test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            usb_plot = calan.scale_and_dBFS_specdata(lsbtone_usb[:i], test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            calibration_plot_update(lsb_scale, usb_scale, None, lsb_plot, usb_plot,
                                    None, test_parameters['if_freqs'], test_parameters['if_test_freqs'][:i],
                                    plot['fig'], plot['lines'])
             

    rf_freq = test_parameters[dss]['rf_freqs']['usb']
    usbtone_lsb = np.zeros(len(test_channels))
    usbtone_usb = np.zeros(len(test_channels))
    for i,ch  in enumerate(test_channels):
        rf = rf_freq[ch]
        rf_gen.set_freq_ghz(rf)
        time.sleep(test_parameters['sleeping'])
        usb = read_autocorrelation_brams(fpga, test_parameters[dss]['synth0'],
            test_parameters['bram_addr_width'],
            test_parameters['bram_data_width'],
            test_parameters['pow_dtype'])
        lsb = read_autocorrelation_brams(fpga, test_parameters[dss]['synth1'],
            test_parameters['bram_addr_width'],
            test_parameters['bram_data_width'],
            test_parameters['pow_dtype'])
        usbtone_lsb[i] = lsb[ch]
        usbtone_usb[i] = usb[ch]
        
        if(test_parameters['debug_folder'] is not None):
            np.savez( os.path.join(folder_path,'usb', 'chnl_'+str(ch)),
                     lsb=lsb, usb=usb)
        if(plot is not None):
            lsb_scale = calan.scale_and_dBFS_specdata(lsb, test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            usb_scale = calan.scale_and_dBFS_specdata(usb, test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            lsb_plot = calan.scale_and_dBFS_specdata(usbtone_lsb[:i], test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            usb_plot = calan.scale_and_dBFS_specdata(usbtone_usb[:i], test_parameters['acc_len'],
                                                     test_parameters['dBFS'])
            calibration_plot_update(lsb_scale, usb_scale, None, lsb_plot, usb_plot,
                                    None, test_parameters['if_freqs'], test_parameters['if_test_freqs'][:i],
                                    plot['fig'], plot['lines'])
    return [lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb]

    
def plot_srr(lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb,  test_parameters, dss, show=False):
    srr_usb = usbtone_usb/usbtone_lsb
    srr_lsb = lsbtone_lsb/lsbtone_usb

    fig, ax = plt.subplots(1)
    ax.plot(test_parameters[dss]['rf_freqs']['lsb'][test_parameters['test_channels']]*1e3,
            10*np.log10(srr_lsb), color='darkblue')
    ax.plot(test_parameters[dss]['rf_freqs']['usb'][test_parameters['test_channels']]*1e3,
            10*np.log10(srr_usb), color='darkred')
    ax.grid()
    ax.set_xlabel('MHz')
    ax.set_ylabel('SRR [dB]')
    fig.savefig(os.path.join(test_parameters['debug_folder'], 'srr', 'srr.pdf'))
    if(show):
        plt.show()
    plt.close()


def program_fpga(test_parameters):
    ##connect to the fpga
    fpga = casperfpga.CasperFpga(test_parameters['fpga_ip'])
    #program it
    fpga.upload_to_ram_and_program(test_parameters['fpg_file'])
    time.sleep(1)
    ##program lmx and lmk
    fpga.adcs.rfdc.progpll('lmk', test_parameters['lmk_file'])
    fpga.adcs.rfdc.progpll('lmx', test_parameters['lmx_file'])
    time.sleep(0.5)
    
    #fpga setup
    fpga.write_int(test_parameters['cnt_rst'],1)
    fpga.write_int(test_parameters['cal_acc_len'], test_parameters['acc_len'])
    fpga.write_int(test_parameters['synth_acc_len'], test_parameters['acc_len'])
    fpga.write_int(test_parameters['cnt_rst'],0)
    return fpga



def main_measure(fpga, dss, test_parameters, log_file=None, log_level=logging.DEBUG, cal_plot=True,
                 inverted=False):
    """
    fpga:           fpga object
    dss:            which sideband separation we are testing (we have two sideband separation in the model: 
                    dss01 and dss23)
    test_paramters: Parameters of the measurement (from parameters.py)
    log_file:       
    log_level:
    cal_plot:       If plot the values while measuring

    """
    ##create logger object
    logging.basicConfig()
    logformat = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger("dss_logger")
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logformat)
    logger.addHandler(console_handler)
    #if we want to save the logs in a file
    if(log_file is not None):
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logformat)
        logger.addHandler(file_handler)

    ##First we are going to make the rf measurment
    debug_name = test_parameters['debug_folder']
    if(inverted):
        test_parameters['debug_folder'] = debug_name+'_lo'
    else:
        test_parameters['debug_folder'] = debug_name+'_rf'
    [aa_lsb, bb_lsb, ab_lsb,
     aa_usb, bb_usb, ab_usb, plot] = make_dss_calibration(fpga, test_parameters,dss,
             logger, plot=cal_plot, inverted=False)

    ##compute calibration constants   

    # consts usb are computed with tone in lsb, because you want to cancel out 
    # lsb, the same for consts lsb
    logger.info("Computing calibration constants")
    const_usb = -1*ab_lsb/bb_lsb            #ab*/bb*=a/b
    const_lsb = -1*np.conj(ab_usb)/aa_usb   #(ab*)*/aa* = a*b/aa*= b/a


    ###now the calibrated signals will be
    ## usb_data = fft0+const_usb*fft1
    ## lsb_data = fft1+const_lsb*fft0

    ##calibrator0 has fft0+fft1*const
    ##calibrator1 has fft1+fft0*const

    ##save calibration data
    name = 'cal_data_'+'{:.2f}'.format(test_parameters[dss]['lo']['freq'])+'_'+'{:.2f}'.format(test_parameters[dss]['lo']['power'])
    np.savez(os.path.join(test_parameters['debug_folder'],name),
            aa_lsb = aa_lsb, bb_lsb = bb_lsb, ab_lsb = ab_lsb,
            aa_usb = aa_usb, bb_usb = bb_usb, ab_usb = ab_usb,
            const_usb = const_usb, const_lsb = const_lsb,
            lo_frequency = test_parameters[dss]['lo']['freq'],
            lo_power = test_parameters[dss]['lo']['power'],
            rf_power = test_parameters[dss]['rf']['power']
        )
    
    ##srr measurement
    logger.info("Starting SRR measurement")
    if(test_parameters['load_constant']):
        logger.info("Calibrated constants measure")
        constants = [const_lsb, const_usb]
        [lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb] = srr_measurement(fpga, 
                test_parameters, constants,dss,logger, plot=plot)
        plot_srr(lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb,  
                test_parameters, dss)
        os.rename(os.path.join(test_parameters['debug_folder'], 'srr'),
                os.path.join(test_parameters['debug_folder'], 'srr_calibrated'))
        
        if(test_parameters['inverted']):
            logger.info("Calibrated constant measured inverse")
            [lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb] = srr_measurement(fpga, 
                    test_parameters, constants,dss,logger, plot=plot, inverted=True)
            plot_srr(lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb,  
                    test_parameters, dss)
            os.rename(os.path.join(test_parameters['debug_folder'], 'srr'),
                    os.path.join(test_parameters['debug_folder'], 'srr_calibrated_inverted'))


    if(test_parameters['load_ideal']):
        logger.info("Ideal constants measure")
        ideal = np.ones(test_parameters['nchannels'])*test_parameters['ideal_constant']
        constants = [ideal, ideal]
        [lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb] = srr_measurement(fpga, 
                test_parameters, constants,dss,logger, plot=plot)
        plot_srr(lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb,  
                test_parameters, dss)
        os.rename(os.path.join(test_parameters['debug_folder'], 'srr'),
                os.path.join(test_parameters['debug_folder'], 'srr_ideal'))
        
        if(test_parameters['inverted']):
            logger.info("Ideal constant measured inverse")
            [lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb] = srr_measurement(fpga, 
                    test_parameters, constants,dss,logger, plot=plot, inverted=True)
            plot_srr(lsbtone_lsb, lsbtone_usb, usbtone_lsb, usbtone_usb,  
                    test_parameters, dss)
            os.rename(os.path.join(test_parameters['debug_folder'], 'srr'),
                    os.path.join(test_parameters['debug_folder'], 'srr_ideal_inverted'))



if __name__ == '__main__':
    fpga = program_fpga(test_parameters)
    main_measure(fpga, 'dss23', test_parameters)
    main_measure(fpga, 'dss23', test_parameters, inverted=True)

